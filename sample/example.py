import heatequation
import matplotlib.pyplot as plt
import matplotlib.cm
import numpy as np

import warnings
warnings.filterwarnings("error")

##### Configure ######
FIELD_WIDTH = 0.5 #meters
ELEMENTS = 100 #Number of elements in each array, per dimension.
ELEMENTS_ROD = int(round(ELEMENTS/10))
INITIAL_TEMP_SAND = 50.0 #Celsius
INITIAL_TEMP_WOOD = 0.0
INITIAL_TEMP_STEEL = 100.0
MAX_TIME = 600 #seconds
######################

SAND_DENSITY = 1400.0 #kg/m3
SAND_THERMAL_CONDUCTIVITY = 2.0 #W/(m*K)
SAND_SPECIFIC_HEAT_CAPACITY = 830.0 #J/(kg*K)

STEEL_DENSITY = 2600.0
STEEL_THERMAL_CONDUCTIVITY = 17.0
STEEL_SPECIFIC_HEAT_CAPACITY = 500.0

WOOD_DENSITY = 600.0
WOOD_THERMAL_CONDUCTIVITY = 0.12
WOOD_SPECIFIC_HEAT_CAPACITY = 2000.0

cmap=matplotlib.cm.get_cmap("hot")

def plot_column():
    fig = plt.figure()
    subplot = plt.subplot(111)
    im = subplot.imshow(temperature_array, cmap=cmap, vmin=0.0, vmax=100.0, interpolation='nearest', origin='lower')
    im.figure = fig
    fig.colorbar(im)
    plt.title("{0} seconds".format(round(second)))
    plt.show()
    last_plot = second

GRANULARITY = FIELD_WIDTH / ELEMENTS #meters
MIDDLE = int(round(ELEMENTS/2))
RANGE_STEEL = range(MIDDLE - ELEMENTS_ROD, MIDDLE)
RANGE_WOOD = range(MIDDLE, MIDDLE + ELEMENTS_ROD)
temperature_array = np.full([ELEMENTS, ELEMENTS], INITIAL_TEMP_SAND)
density_array = np.full([ELEMENTS, ELEMENTS], SAND_DENSITY)
thermal_conductivity_array = np.full([ELEMENTS, ELEMENTS], SAND_THERMAL_CONDUCTIVITY)
specific_heat_capacity_array = np.full([ELEMENTS, ELEMENTS], SAND_SPECIFIC_HEAT_CAPACITY)

for n in RANGE_STEEL:
    for m in RANGE_STEEL:
        temperature_array[n, m] = INITIAL_TEMP_STEEL
        density_array[n, m] = STEEL_DENSITY
        thermal_conductivity_array[n, m] = STEEL_THERMAL_CONDUCTIVITY
        specific_heat_capacity_array[n, m] = STEEL_SPECIFIC_HEAT_CAPACITY

for n in RANGE_WOOD:
    for m in RANGE_WOOD:
        temperature_array[n, m] = INITIAL_TEMP_WOOD
        density_array[n, m] = WOOD_DENSITY
        thermal_conductivity_array[n, m] = WOOD_THERMAL_CONDUCTIVITY
        specific_heat_capacity_array[n, m] = WOOD_SPECIFIC_HEAT_CAPACITY

he = heatequation.HeatEquation(temperature_array, GRANULARITY, density_array, thermal_conductivity_array, specific_heat_capacity_array)
print("time interval (he.dt): {0}".format(he.dt))

tick = 0
second = 0.0
while second <= MAX_TIME:
    try:
        if tick % 100 == 0:
            print("second {0}".format(round(second)))
            plot_column()
        he.evolve_ts()
        second = second + he.dt
        tick += 1
    except:
        print("Error at {0} seconds".format(round(second)))
        plot_column()
        quit = input("Exit now? [y/N]: ")
        if quit == "y":
            raise
