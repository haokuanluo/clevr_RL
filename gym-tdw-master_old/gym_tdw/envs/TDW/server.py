import zmq
import argparse
from multiprocessing import Process, Manager, freeze_support
# Prefix for all addresses.
address_prefix = "tcp://*:"

parser = argparse.ArgumentParser()

# The port used by the server to communicate with the remote client.
parser.add_argument('-B', dest='send_to_build_port', default=1337, type=int, metavar='Send to build port',
                    help="Default=1337")
# The port used by the client to communicate with the remote client.
parser.add_argument('-b', type=int, dest='recv_from_build_port', default=1341,
                    metavar='Receive from builds port', help="Default=1341")
# The port for receiving input from the controller.
parser.add_argument('-c', dest='recv_from_controller_port', default='1339', type=str,
                    metavar='Receive from controller port', help="Default=1339")
# The port for sending output from the controller.
parser.add_argument('-C', dest='send_to_controller_port', default='1340', type=str,
                    metavar='Send to controller port',help="Default=1340")
# Toggle for quiet mode.
parser.add_argument('-q', dest='quiet_mode', default=False, action='store_true', help='Quiet')
# Toggle for verbose mode.
parser.add_argument('-v', dest='verbose_mode', default=False, action='store_true', help='Verbose')
# Parse the arguments.
args = parser.parse_args()

verbose_mode = args.verbose_mode
quiet_mode = args.quiet_mode


# Receive messages from controller(s).
def recv_from_controller(ids):

    # Create the zmq context.
    context = zmq.Context()

    # Socket for receiving messages from controller.
    recv_from_controller_sock = context.socket(zmq.ROUTER)
    recv_from_controller_sock.bind(address_prefix + args.recv_from_controller_port)

    # Socket for sending messages to build.
    send_to_build_sock = context.socket(zmq.ROUTER)
    send_to_build_sock.bind(address_prefix + str(args.send_to_build_port))

    poller = zmq.Poller()
    poller.register(recv_from_controller_sock, zmq.POLLIN)
    poller.register(send_to_build_sock, zmq.POLLIN)

    # Dictionary used to manage messages received from the controller.
    # Key=build_id of destination. Value=list of messages
    from_controller_messages = dict()

    while True:
        # Poll for sockets.
        sockets = dict(poller.poll())
        # Receive new messages from controller
        if recv_from_controller_sock in sockets:
            # Receive the payload from the controller.
            payload = recv_from_controller_sock.recv_multipart()

            build_id = payload[1]
            controller_id = payload[0]

            # Debug received payload.
            if not quiet_mode:
                debug_msg = "Received from controller " + str(controller_id) + " to send to build " + str(build_id)
                if verbose_mode:
                    debug_msg += ": " + str(payload[2:])
                print(debug_msg)

            # Is this a new build_id in the ID dictionary?  If so, add a new key-value pair.

            if build_id not in ids.keys():
                ids.update({build_id: []})
            # Is the controller ID not in the ID dictionary? If so, append it.
            if controller_id not in ids[build_id]:
                # This needs to be done this way to work with shared state Manager.
                ids[build_id] = ids[build_id] + [controller_id]

            # Does from_controller_messages have build_id as a key? If not, add a new key-value pair.
            if build_id not in from_controller_messages.keys():
                from_controller_messages.update({build_id: []})

            # Add the payload to the message dictionary.
            from_controller_messages[build_id].extend(payload[2:])

        # Send new messages to build.
        if send_to_build_sock in sockets:
            build_id = send_to_build_sock.recv_multipart()[0]
            if build_id not in from_controller_messages.keys():
                send_to_build_sock.send_multipart([build_id])
                continue
            payload = from_controller_messages[build_id]
            # Ignore empty messages.
            if len(payload) == 0:
                continue
            # Add build ID so this message goes to the correct build.
            payload.insert(0, build_id)

            # Send.
            send_to_build_sock.send_multipart(payload)

            # Debug sent payload.
            if not quiet_mode:
                debug_msg = "sent to build " + str(build_id)
                if verbose_mode:
                    debug_msg += ": " + str(payload)
                print(debug_msg)

            # Remove the messages.
            del from_controller_messages[build_id][:]


# Receive messages from build(s).
def recv_from_build(ids):
    # Create the zmq context.
    context = zmq.Context()
    
    # Socket for receiving messages from build.
    recv_from_build_sock = context.socket(zmq.ROUTER)
    recv_from_build_sock.bind(address_prefix + str(args.recv_from_build_port))

    # Socket for sending messages to controller.
    send_to_controller_sock = context.socket(zmq.ROUTER)
    send_to_controller_sock.bind(address_prefix + args.send_to_controller_port)

    while True:
        # Receive the payload from the build.
        payload = recv_from_build_sock.recv_multipart()
        build_id = payload[0]

        # Debug received payload.
        if not quiet_mode:
            debug_msg = "Received from build " + str(build_id)
            if verbose_mode:
                debug_msg += ": " + str(payload[1:])
            print(debug_msg)

        # Is this a new build_id in the ID dictionary?  If so, add a new key-value pair.
        if build_id not in ids.keys():
            ids.update({build_id: []})

        # Create the payload to send to the controller.
        payload = payload[1:]
        # Prepare to send the message to each controller associated with the build.
        for controller_id in ids[build_id]:
            # Assemble the payload for this controller.
            controller_payload = [controller_id]
            controller_payload.extend(payload)
            # Send.
            send_to_controller_sock.send_multipart(controller_payload)

            # Debug sent payload.
            if not quiet_mode:
                debug_msg = "Sent to controller " + str(controller_id)
                if verbose_mode:
                    debug_msg += ": " + payload
                print(debug_msg)


if __name__ == '__main__':
    freeze_support()
    # Controller/build ID dictionary. Key=build ID. Value=list of associated controller IDs.
    manager = Manager()
    ID_LIST = manager.dict()

    # Launch the processes
    p1 = Process(target=recv_from_build, args=(ID_LIST,))
    p2 = Process(target=recv_from_controller, args=(ID_LIST,))
    p1.start()
    p2.start()
    while True:
        pass
