# 1. Randomly generate a matrix of spins
# 2. Choose a random atom and consider flipping the orientation of its spin
# 3. Calculate the probablility of accepting the change based on the formula given
#     - For each neighboring atom calculate dE then add them to get total dE
# 4. Randomly accept or reject the flipping of the atom based on calculated probability
#     - Generate a random number and compare to the probability
#     - Actually flip if accepted
# 5. Go back to 2 and repeat some fixed finite number of times
#     - Could consider stopping based on reaching some "equilibrium probability" but may be difficult to be consistent across a wide range of temperatures.
# 6. Calculate magnetization
#     - Sum all spin values in the lattice then take absolute value
#     - "Normalize" by dividing by number of atoms in the lattice
# 7. Go back to 1 and repeat for different temperatures
#     - Going from 0.1 --> 1000 for T


import matplotlib.pyplot as plt
import numpy as np


SIZE = 30


def createLattice(size):
  return (2 * np.random.randint(0,2, size=(size, size))) - 1

def chooseRandomAtom(size):
  return (np.random.randint(0, size), np.random.randint(0, size))

def calculateEnergyChange(lattice, position):
  energyChange = 0
  curOrientation = lattice[position[0]][position[1]]
  for direction in [(1,0),(0,1),(-1,0),(0,-1)]:
    adjacentAtom = np.add(curOrientation, direction)
    if adjacentAtom[0] < 0 or adjacentAtom[1] < 0 or \
        adjacentAtom[0] >= SIZE or adjacentAtom[1] >= SIZE:
      continue
    adjacentOrientation = lattice[adjacentAtom[0]][adjacentAtom[1]]
    energyChange += (2 * curOrientation * adjacentOrientation)
  return energyChange

def calculateProbability(dE, temperature):
  if dE < 0:
    return 1.0
  else:
    p = np.exp(-dE/temperature)
    return p

def acceptChange(probability):
  return np.random.random() < probability


