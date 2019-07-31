import time
import zmq
import json
from secrets import token_bytes
import base64
from TDW.db_server import get_models_collection
from threading import Thread
import os

# The ID of the build we are communicating with.
build_id = b'build_0'
# The ID of this controller. Must be unique.
controller_id = b'controller_0'

context = zmq.Context()
# This socket is used to send messages to the server.
socket_to_server = context.socket(zmq.DEALER)
socket_to_server.setsockopt(zmq.IDENTITY, controller_id)

# This socket is used to receive messages from the controller.
socket_from_server = context.socket(zmq.DEALER)
socket_from_server.setsockopt(zmq.IDENTITY, controller_id)
socket_from_server.setsockopt(zmq.LINGER, 0)
socket_from_server.setsockopt(zmq.RCVTIMEO, 500)

# If true, tdw.py will stop listening to messages from the server.
done = False
local_done = False
# Messages we want to send to the build.
to_send_messages = []

poller = zmq.Poller()
poller.register(socket_from_server, zmq.POLLIN)
# For every message sent update this
global_frame_count = 0
# Every time a message is received update this
global_message_count = 0

def get_unique_id():
    """s
    Returns a unique ID. This is useful for naming avatars, objects, etc.

    :return: A unique ID.
    """

    return int.from_bytes(token_bytes(3), byteorder="big")


def set_build_id(new_id):
    """
    Sets the build ID (which should correspond to the ID of the build we want to communicate with).

    :param new_id: The new ID.
    """

    global build_id
    build_id = new_id


def set_controller_id(new_id):
    """
    Sets the ID of this controller.

    :param new_id: The new ID.
    """

    global controller_id
    controller_id = str(new_id).encode('utf-8')
    socket_to_server.setsockopt(zmq.IDENTITY, controller_id)
    socket_from_server.setsockopt(zmq.IDENTITY, controller_id)


def connect_send_to_server_socket(address, port):
    """
    Connects the socket responsible for sending messages to the server.
    You must call this before sending any messages to the server.

    :param address: The server address.
    :param port: The port to send messages through.
    """

    socket_to_server.connect(address + str(port))


def connect_recv_from_server_socket(address, port):
    """
    Connects the socket responsible for receiving messages from the server.
    You must call this before receiving any messages to the server.

    :param address: The server address.
    :param port: The port to receive messages through.
    """

    socket_from_server.connect(address + str(port))


def send_to_server(message):
    """
    Sends a multipart message to the server.

    :param message: The message to send. This may be 1 message or a list of messages.
    """
    global global_frame_count
    if type(message) == "list":
        global_frame_count += len(message)
    else:
        global_frame_count += 1
    # Make sure the message is a list.
    if not isinstance(message, list):
        message = [message]
    to_send_messages.append(message)


def receive_from_server():
    """
    Returns a message received from the server.
    """

    return socket_from_server.recv_multipart()


def get_time(t):
    """
    Parses a UNIX Epoch long to a human-readable string.

    :param t: Time, in UNIX Epoch, in C# ticks.
    :return: A human-readable time string.
    """

    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t / 10000000.0))


def save_img(base64_string, path):
    """
    Save out an image.

    :param base64_string: The base64 string encoding of the image byte data.
    :param path: The destination directory+filename of the image.
    """

    # Try to decode the image.
    try:
        image_bytes = base64.decodebytes(base64_string.encode('utf-8'))
    except:
        print("Failed to decode image")
        return

    # Open a file to write to.
    with open(path, 'wb') as f:
        # Write out the stream.
        f.write(image_bytes)


def get_substructure(model_name):
    """
    Given the model name, return its substructure from the record database.
    :param model_name: The name of the model.
    """

    record = get_models_collection().find_one(filter={"model_name": model_name})
    return json.loads(record["substructure"])


def run(on_send, on_recv):
    """
    This is a basic main loop for a controller.

    :param on_send: Callback method with no parameters upon sending a message. Can be null.
    :param on_recv: Callback method with one parameter (the list of output data) upon receiving a message. Can be null.
    """
    global local_done
    number_of_frames = 300
    need_to_register = True
    while not local_done:

        if need_to_register and len(to_send_messages) > 0:
            need_to_register = False
            poller.register(socket_to_server, zmq.POLLOUT)
        # if os.path.isdir(os.path.join(directory)):
        #     if len(os.listdir(os.path.join(directory))) >= 1000:
        #         local_done = True

        for s, e in poller.poll(timeout=1000):

            if s is socket_to_server:
                # Always send the build ID as the first part of the multipart message.
                ab = to_send_messages.pop(0)
                s.send_multipart([build_id, json.dumps(ab).encode('utf-8')])

                # Stop listening to this socket, for now.
                if len(to_send_messages) == 0:
                    poller.unregister(socket_to_server)
                    need_to_register = True
                # Invoke the callback.
                if on_send is not None:
                    on_send()
            if s is socket_from_server:
                output_data = s.recv_multipart()
                # Invoke the callback.
                if on_recv is not None:
                    on_recv(output_data)


def quit():
    """
    ALWAYS call this before qutting!
    """

    socket_to_server.close()
    global done
    done = True



def thread(target, args=None):
    """
    Starts a method on a thread.

    :param target: The target method to thread.
    :param args: A list of arguments.
    """
    print("Starting Thread")
    if args is None:
        t = Thread(target=target)
    else:
        t = Thread(target=target, args=args)
    t.setDaemon(True)
    t.start()
    print("Started run on thread")
    return t