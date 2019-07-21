from gym.envs.registration import register

register(
    id='tdw_puzzle_1-v0',
    entry_point='gym_tdw.envs:TdwEnv'
)

register(
    id='tdw_puzzle_2-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_2'
)

register(
    id='tdw_puzzle_3-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_3'
)


register(
    id='tdw_puzzle_4-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_4'
)

register(
    id='tdw_puzzle_5-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_5'
)

register(
    id='tdw_puzzle_6-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_6'
)

register(
    id='tdw_puzzle_7-v0',
    entry_point='gym_tdw.envs:TdwEnv_puzzle_7'
)