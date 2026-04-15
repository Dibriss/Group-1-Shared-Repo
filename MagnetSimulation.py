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
from matplotlib.animation import FuncAnimation
import numpy as np


SIZE = 25
SIMULATED_CHANGES = 3000
TEMPERATURES = 100
RANDOM_START = False


def createLattice(size, random_start):
  if random_start:
    return (2 * np.random.randint(0,2, size=(size, size))) - 1
  else:
    return np.ones((size, size))

def chooseRandomAtom(size):
  return (np.random.randint(0, size), np.random.randint(0, size))

def calculateEnergyChange(lattice, position):
  energy_change = 0
  cur_orientation = lattice[position[0], position[1]]
  for direction in [(1,0),(0,1),(-1,0),(0,-1)]:
    adjacent_atom = np.add(position, direction)
    if adjacent_atom[0] < 0 or adjacent_atom[1] < 0 or \
        adjacent_atom[0] >= SIZE or adjacent_atom[1] >= SIZE:
      continue
    adjacent_orientation = lattice[adjacent_atom[0], adjacent_atom[1]]
    energy_change += (2 * cur_orientation * adjacent_orientation)
  return energy_change

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

def simulateFixedTemperature(temperature, random_start):
  lattice = createLattice(SIZE, random_start)
  for n in range(SIMULATED_CHANGES):
    atom = chooseRandomAtom(SIZE)
    energy_change = calculateEnergyChange(lattice, atom)
    probability = calculateProbability(energy_change, temperature)
    if(acceptChange(probability)):
      lattice[atom[0], atom[1]] *= -1
  magnetization = calculateMagnetization(lattice)
  return magnetization, lattice



temperature = 10 ** np.linspace(0,1, TEMPERATURES) # np.linspace(-1, 3, TEMPERATURES)
magentization = np.zeros(TEMPERATURES)
lattice_frames = []
for n, temp in enumerate(temperature):
  test_magnetizations = []
  for i in range(3):
    mag, lattice = simulateFixedTemperature(temp, RANDOM_START)
    test_magnetizations.append(mag)
    lattice_frames.append(lattice)
  magentization[n] = np.average(test_magnetizations)


fig, ax = plt.subplots(1, 2)

ax[0].plot(temperature, magentization)
ax[0].set_xlabel('Temperature')
ax[0].set_ylabel('Magnetization')
ax[0].set_xscale('log')
ax[0].grid(True)

plt.rcParams["animation.html"] = "jshtml" 
plt.rcParams['figure.dpi'] = 60
plt.ioff()

ax[1].set_xticks([])
ax[1].set_yticks([])

# initialize the object being animated
L = 10
FRAMES = 100

image = ax[1].imshow(np.zeros((L,L)), vmin=-1, vmax=1, cmap='turbo')

def animate(frame):
    # make a small change to the object
    image.set_data(frame)
    return image,

animation = FuncAnimation(fig, animate, frames=lattice_frames, blit=True)

plt.show()
