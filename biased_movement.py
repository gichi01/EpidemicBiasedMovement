# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 22:18:04 2017

@author: yoshimura
S,R:
x(t+1) = x(t) + N(0, noize_level) + bias_level
y(t+1) = y(t) + N(0, noize_level)
I:
x(t+1) = x(t) + N(0, noize_level_of_i) + bias_level_of_i
y(t+1) = y(t) + N(0, noize_level_of_i)
"""

from random import choice, gauss, random, seed, shuffle, uniform
seed()

if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    import pylab

width = 100
height = 100
populationSize = 500
noiseLevel = 1
biasLevel = 1

collisionDistance = 2
CDsquared = collisionDistance ** 2
CDsquared = 0.5

beta = 1
gamma = 0.1
noize_level_of_i = 0.1
bias_level_of_i = 0.1

time = 0
agents = []
pop_history = {'S': [], 'I': [], 'R': []}

def init(**kwargs):
    global noizeLevel, beta, gamma, noize_level_of_i, bias_level_of_i
    noizeLevel = kwargs.get('noize_level', 1)
    biasLevel = kwargs.get('bias_level', 1)
    beta = kwargs.get('beta', 1)
    gamma = kwargs.get('gamma', gamma)
    noize_level_of_i = kwargs.get('noize_level_of_i', noize_level_of_i)
    bias_level_of_i = kwargs.get('bias_level_of_i', bias_level_of_i)

    global time, agents, pop_history

    time = 0
    agents = [{
        'x': uniform(0, width),
        'y': uniform(0, height),
        'state': 'S'
    } for i in range(populationSize)]
    # infect 2 agents
    agents[-1]['state'] = 'I'
    agents[-2]['state'] = 'I'

    pop_history = {'S': [], 'I': [], 'R': []}
    pop_history['S'].append(populationSize-2)
    pop_history['I'].append(2)
    pop_history['R'].append(0)

def draw():
    global agents, time, pop_history

    pylab.subplot(1, 2, 1)
    pylab.cla()

    Xs = [a['x'] for a in agents]
    Ys = [a['y'] for a in agents]
    Cs = ['blue' if a['state'] == 'S' else\
          'red' if a['state'] == 'I' else\
          'orange' for a in agents]
    pylab.scatter(Xs, Ys, color=Cs)

    pylab.axis('scaled')
    pylab.axis([0, width, 0, height])
    pylab.title('t = {}'.format(time))

    pylab.subplot(1, 2, 2)
    pylab.cla()

    pylab.plot(pop_history['I'], color = 'red')
    pylab.plot(pop_history['S'], color = 'blue')
    pylab.plot(pop_history['R'], color = 'orange')

    pylab.ylim(0, populationSize)
    pylab.title('populationSize S,I,R')

def step():
    global time, agents

    time += 1

    # simulate random motion and state update
    shuffle(agents)
    for ag in agents:
        # move one-directionally (along x)
        if ag['state'] == 'I':
            x = ag['x'] + gauss(0, noize_level_of_i) + bias_level_of_i
            y = ag['y'] + gauss(0, noize_level_of_i)
        else:
            x = ag['x'] + gauss(0, noizeLevel) + biasLevel
            y = ag['y'] + gauss(0, noizeLevel)
        ag['x'] = x - width if x > width else\
                  width + x if x < 0 else\
                  x
        ag['y'] = y - height if y > height else\
                  height + y if y < 0 else\
                  y

        if ag['state'] == 'S':
            n_nei_i = len([
                a for a in agents
                if a is not ag and\
                a['state'] == 'I' and\
                (a['x']-ag['x'])**2 + (a['y']-ag['y'])**2 < CDsquared
            ])
            if random() < 1 - (1 - beta) ** n_nei_i:
                ag['state'] = 'I'
        elif ag['state'] == 'I':
            if random() < gamma: # recovery rate
                ag['state'] = 'R'
        else: # if ag['state'] == 'R':
            pass

    pop_history['S'].append(len([a for a in agents if a['state'] == 'S']))
    pop_history['I'].append(len([a for a in agents if a['state'] == 'I']))
    pop_history['R'].append(len([a for a in agents if a['state'] == 'R']))


# parameter setters
class BetaSetter(object):
    __name__ = 'beta'
    def __call__(self, var=1):
        global beta
        beta = var
        return beta
class GammaSetter(object):
    __name__ = 'gamma'
    def __call__(self, var=0.01):
        global gamma
        gamma = var
        return gamma
class NoizeLevelSetter(object):
    __name__ = 'noize level of I'
    def __call__(self, var=0.1):
        global noize_level_of_i
        noize_level_of_i = var
        return noize_level_of_i
class BiasLevelSetter(object):
    __name__ = 'bias level of I'
    def __call__(self, var=0.1):
        global bias_level_of_i
        bias_level_of_i = var
        return bias_level_of_i
class CollisionDistanceSetter(object):
    __name__ = 'collision distance'
    def __call__(self, var=0.7):
        global collisionDistance, CDsquared
        collisionDistance = var
        CDsquared = collisionDistance ** 2
        return collisionDistance

if __name__ == '__main__':
    import pycxsimulator
    pycxsimulator.GUI(parameterSetters=[
        BetaSetter(),
        GammaSetter(),
        NoizeLevelSetter(),
        BiasLevelSetter(),
        CollisionDistanceSetter(),
    ]).start(func=[init,draw,step])
