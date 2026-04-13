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
SIMULATED_CHANGES = 10000
TEMPERATURES = 20


def createLattice(size):
  return (2 * np.random.randint(0,2, size=(size, size))) - 1

def chooseRandomAtom(size):
  return (np.random.randint(0, size), np.random.randint(0, size))

def calculateEnergyChange(lattice, position):
  energyChange = 0
  curOrientation = lattice[position[0], position[1]]
  for direction in [(1,0),(0,1),(-1,0),(0,-1)]:
    adjacentAtom = np.add(curOrientation, direction)
    if adjacentAtom[0] < 0 or adjacentAtom[1] < 0 or \
        adjacentAtom[0] >= SIZE or adjacentAtom[1] >= SIZE:
      continue
    adjacentOrientation = lattice[adjacentAtom[0], adjacentAtom[1]]
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

def calculateMagnetization(lattice):
  rows, cols = lattice.shape
  totalMagnetization = np.sum(lattice)
  return np.abs(totalMagnetization) / (rows * cols)

def simulateFixedTemperature(temperature):
  lattice = createLattice(SIZE)
  for n in range(SIMULATED_CHANGES):
    atom = chooseRandomAtom(SIZE)
    energy_change = calculateEnergyChange(lattice, atom)
    probability = calculateProbability(energy_change, temperature)
    if(acceptChange(probability)):
      lattice[atom[0], atom[1]] *= -1
  return calculateMagnetization(lattice)



temperature = 10 ** np.linspace(-1, 3, TEMPERATURES)
magentization = np.zeros(TEMPERATURES)
for n, temp in enumerate(temperature):
  test_magnetizations = [simulateFixedTemperature(temp) for i in range(10)]
  magentization[n] = np.average(test_magnetizations)


plt.plot(temperature, magentization)
plt.xlabel('Temperature')
plt.ylabel('Magnetization')
plt.xscale('log')
plt.grid(True)
plt.show()
