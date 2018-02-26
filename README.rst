heatequation provides a single class HeatEquation to calculate heat transfer in a matrix of heterogeneous materials. It implements an incremental, arithmetic solution to the heat equation [#1]_ . This solution allows you calculate the system state at any point in time by calculating the system state at all increments up to that point.  It only implements a two dimensional solution of the heat equation, though someone could relatively easily extend it to one or three dimensions.

The HeatEquation class is initialized with arrays corresponding to physical properties in the physical space of the simulated materials. The required arrays are initial temperature, mass density, thermal conductivity, and specific heat capacity.

The source repository at github [#2]_ includes a sample script to help you get started.

.. [#1] https://en.wikipedia.org/wiki/Heat_equation
.. [#2] https://github.com/worden341/heatequation
