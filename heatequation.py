import numpy as np

class HeatEquation(object):
    """
    Implements a numerical solution of the 2d heat equation, allowing heterogenous materials.
    """
    def __init__(self, temperature, dx, density, thermal_conductivity, specific_heat_capacity, dt=None):
        """
        :param temperature: (eg. Kelvin) numpy array of float with two dimensions. The starting temperature array.
        :param dx: float spatial interval (eg. meters) between row elements.
        :param density: (eg. kg/m**3) numpy.ndarray with same shape as temperature array
        :param thermal_conductivity: (eg. W/m*K) numpy.ndarray with same shape as temperature array
        :param specific_heat_capacity: (eg. J/kg*K) numpy.ndarray with same shape as temperature array
        :param dt: float time interval (eg. seconds). Recommend None, to let instance calculate maximum stable value.
        """
        self.temperature = temperature
        self.nx = self.temperature.shape[0]
        self.ny = self.temperature.shape[1]
        self.dx = float(dx)
        self.dy = self.dx
        if isinstance(density, np.ndarray) and density.shape == self.temperature.shape:
            self.density = density
        else:
            raise Exception("parameter density must be a numpy.ndarray of same size as temperature array")
        if isinstance(thermal_conductivity, np.ndarray) and thermal_conductivity.shape == self.temperature.shape:
            self.thermal_conductivity = thermal_conductivity
        else:
            raise Exception("parameter thermal_conductivity must be a numpy.ndarray of same size as temperature array")
        if isinstance(specific_heat_capacity, np.ndarray) and specific_heat_capacity.shape == self.temperature.shape:
            self.specific_heat_capacity = specific_heat_capacity
        else:
            raise Exception("parameter specific_heat_capacity must be a numpy.ndarray of same size as temperature array")
        self.diffusivity = self.thermal_conductivity / (self.density * self.specific_heat_capacity)
        self.thermal_conductivity_middle = self.thermal_conductivity[1:-1, 1:-1]
        self.thermal_conductivity_dx_minus = np.minimum(self.thermal_conductivity[2:, 1:-1], self.thermal_conductivity_middle)
        self.thermal_conductivity_dx_plus = np.minimum(self.thermal_conductivity[:-2, 1:-1], self.thermal_conductivity_middle)
        self.thermal_conductivity_dy_minus = np.minimum(self.thermal_conductivity[1:-1, 2:], self.thermal_conductivity_middle)
        self.thermal_conductivity_dy_plus = np.minimum(self.thermal_conductivity[1:-1, :-2], self.thermal_conductivity_middle)
        self.density_middle = self.density[1:-1, 1:-1]
        self.specific_heat_capacity_middle = self.specific_heat_capacity[1:-1, 1:-1]
        self.dx2 = self.dx**2
        self.dy2 = self.dy**2
        # For stability, this is the largest time interval possible:
        max_dt = self.dx2 / np.amax(self.diffusivity) / 12
        if dt:
            _dt = float(dt)
            if _dt > max_dt:
                raise Warning("Value of parameter dt {0} exceeds calculated stable maximum value {1}.".format(_dt, max_dt))
            self.dt = _dt
        else:
            self.dt = max_dt

    @property
    def boundary_temp(self):
        """
        The arithmetic mean temperature of the boundary. Only useful for highly symmetrical arrays.
        :return: the arithmetic mean temperature of the boundary
        """
        stats = [(float(len(_)), sum(_)) for _ in [self.temperature[0,:], self.temperature[-1,:], self.temperature[1:-1,0], self.temperature[1:-1,-1]]]
        _count = sum([_[0] for _ in stats])
        _sum = sum([_[1] for _ in stats])
        return _sum / _count

    @boundary_temp.setter
    def boundary_temp(self, temp):
        """
        The boundary of the matrix serves as a source of background heat.
        If the temp is lower than the interior, it will be a heat sink, or oppositely, a source.
        :param temp float temperature, or np.array of size matching self.temperature.
            If a float, all boundary values are set to the float.
            If an np.array, then the boundary values are set equal to adjacent values immediately towards the interior.
        """
        if isinstance(temp, float):
            ftemp = float(temp)
            self.temperature[0, :] = ftemp
            self.temperature[self.nx-1, :] = ftemp
            self.temperature[:, 0] = ftemp
            self.temperature[:, self.ny-1] = ftemp
        elif temp is self.temperature:
            self.temperature[0, :] = temp[1, :]
            self.temperature[self.nx-1, :] = temp[self.nx-2, :]
            self.temperature[:, 0] = temp[:, 1]
            self.temperature[:, self.ny-1] = temp[:, self.ny-2]

    def boundary_temp_adjust(self):
        self.boundary_temp = self.temperature

    def evolve_ts(self, dt=None):
        """
        Run the heat equation for one time interval (dt). Modify the temperature array.
        :param dt: float time interval
        """
        _dt = dt if dt else self.dt
        self.temperature[1:-1, 1:-1] = \
            self.temperature[1:-1, 1:-1] \
            + _dt*(
                (
                    (self.temperature[2:, 1:-1] - self.temperature[1:-1, 1:-1]) * self.thermal_conductivity_dx_minus / (self.density_middle * self.specific_heat_capacity_middle)\
                    + (self.temperature[:-2, 1:-1] - self.temperature[1:-1, 1:-1]) * self.thermal_conductivity_dx_plus / (self.density_middle * self.specific_heat_capacity_middle)
                )\
                /self.dx2 \
                + (
                    (self.temperature[1:-1, 2:] - self.temperature[1:-1, 1:-1]) * self.thermal_conductivity_dy_minus / (self.density_middle * self.specific_heat_capacity_middle) \
                    + (self.temperature[1:-1, :-2] - self.temperature[1:-1, 1:-1]) * self.thermal_conductivity_dy_plus / (self.density_middle * self.specific_heat_capacity_middle)
                )\
                /self.dy2
            )
        self.boundary_temp_adjust()
