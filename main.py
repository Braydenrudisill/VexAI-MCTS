import time
from memory import *
from funcs import *
from settings import run_folder, run_archive_folder
from model import Residual_CNN
from gameEnvironment import VexEnv
import config
import loggers as lg
from agent import Agent
from keras.utils import plot_model
from importlib import reload
import random
from shutil import copyfile
import gym
import numpy as np
np.set_printoptions(suppress=True)


lg.logger_main.info('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
lg.logger_main.info('=*=*=*=*=*=       NEW LOG       =*=*=*=*=*')
lg.logger_main.info('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')

# Set up environment

env = VexEnv()

memory = Memory(config.MEMORY_SIZE)

# Create an untrained neural network objects from the config file
current_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE,
                          (2,) + env.grid_shape,   env.action_size, config.HIDDEN_CNN_LAYERS)
best_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE,
                       (2,) + env.grid_shape,   env.action_size, config.HIDDEN_CNN_LAYERS)

best_player_version = 0
best_NN.model.set_weights(current_NN.model.get_weights())

# copy the config file to the run folder
copyfile('./config.py', run_folder + 'config.py')
plot_model(current_NN.model, to_file=run_folder +
           'models/model.png', show_shapes=True)

print('\n')

######## CREATE THE PLAYERS ########

current_player = Agent(1, 'current_player', env.state_size,
                       env.action_size, config.MCTS_SIMS, config.CPUCT, current_NN)
best_player = Agent(-1, 'best_player', env.state_size,
                    env.action_size, config.MCTS_SIMS, config.CPUCT, best_NN)
#user_player = User('player1', env.state_size, env.action_size)
iteration = 0

while 1:

    iteration += 1
    reload(lg)
    reload(config)

    print('ITERATION NUMBER ' + str(iteration))

    lg.logger_main.info('BEST PLAYER VERSION: %d', best_player_version)
    print('BEST PLAYER VERSION ' + str(best_player_version))

    ######## SELF PLAY ########
    print('SELF PLAYING ' + str(config.EPISODES) + ' EPISODES...')
    _, memory, _, _ = playMatches(best_player, best_player, config.EPISODES,
                                  lg.logger_main, turns_until_tau0=config.TURNS_UNTIL_TAU0, memory=memory)
    print('\n')

    memory.clear_stmemory()

    if len(memory.ltmemory) >= config.MEMORY_SIZE:

        ######## RETRAINING ########
        print('RETRAINING...')
        current_player.replay(memory.ltmemory)
        print('')

        if iteration % 5 == 0:
            pickle.dump(memory, open(run_folder + "memory/memory" +
                                     str(iteration).zfill(4) + ".p", "wb"))

        lg.logger_memory.info('====================')
        lg.logger_memory.info('NEW MEMORIES')
        lg.logger_memory.info('====================')

        memory_samp = random.sample(
            memory.ltmemory, min(1000, len(memory.ltmemory)))

        for s in memory_samp:
            current_value, current_probs, _ = current_player.get_preds(
                s['state'])
            best_value, best_probs, _ = best_player.get_preds(s['state'])

            lg.logger_memory.info('MCTS VALUE FOR %s: %f',
                                  s['playerTurn'], s['value'])
            lg.logger_memory.info(
                'CUR PRED VALUE FOR %s: %f', s['playerTurn'], current_value)
            lg.logger_memory.info(
                'BES PRED VALUE FOR %s: %f', s['playerTurn'], best_value)
            lg.logger_memory.info('THE MCTS ACTION VALUES: %s', [
                                  '%.2f' % elem for elem in s['AV']])
            lg.logger_memory.info('CUR PRED ACTION VALUES: %s', [
                                  '%.2f' % elem for elem in current_probs])
            lg.logger_memory.info('BES PRED ACTION VALUES: %s', [
                                  '%.2f' % elem for elem in best_probs])
            lg.logger_memory.info('ID: %s', s['state'].id)
            lg.logger_memory.info(
                'INPUT TO MODEL: %s', current_player.model.convertToModelInput(s['state']))

            s['state'].render(lg.logger_memory)

        ######## TOURNAMENT ########
        print('TOURNAMENT...')
        scores, _, points, sp_scores = playMatches(
            best_player, current_player, config.EVAL_EPISODES, lg.logger_tourney, turns_until_tau0=0, memory=None)
        print('\nSCORES')
        print(scores)
        print('\nSTARTING PLAYER / NON-STARTING PLAYER SCORES')
        print(sp_scores)
        # print(points)

        print('\n\n')

        if scores['current_player'] > scores['best_player'] * config.SCORING_THRESHOLD:
            best_player_version = best_player_version + 1
            best_NN.model.set_weights(current_NN.model.get_weights())
            best_NN.write(env.name, best_player_version)

    else:
        print('MEMORY SIZE: ' + str(len(memory.ltmemory)))


# OLD CODE ARCHIVE ----------------------------------------------

#print("Observation Space: ", env.observation_space)
#print("Action Space: ",env.action_space)

# # Start agent and reset env
# agent = Agent(env)
# agent2 = Agent(env)
# state = env.reset()
# print("starting")
# done = False
# while not done:
#     # print("turn: ",env.gameState.turn)
#     action = agent.get_action(state)
#     action2 = agent.get_action(state)
#     # print("p1 action: ", env.action_names[action])
#     # print("p2 action: ", env.action_names[action2])
#     next_state, value, done, info = env.step((action,action2))
#     env.render(lg.logger_main)
#
# print(env.gameState.board)
# print(value)


lg.logger_main.info('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
lg.logger_main.info('=*=*=*=*=*=         DONE        =*=*=*=*=*')
lg.logger_main.info('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
