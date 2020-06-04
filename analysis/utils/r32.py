import numpy as np
import unyt as u

class R32:

    @property
    def param_names(self):
        """Return the adjustable parameter names"""

        param_names = (
            "sigma_C",
            "sigma_F",
            "sigma_H",
            "epsilon_C",
            "epsilon_F",
            "epsilon_H",
        )

        return param_names

    @property
    def param_bounds(self):
        """Return the bounds on sigma and epsilon in units of nm and kJ/mol"""

        bounds_sigma = (
            (
                np.asarray([[3.0, 4.0], [2.5, 3.5], [1.7, 2.7],]) * u.Angstrom
            )  # C  # F  # H
            .in_units(u.nm)
            .value
        )

        bounds_epsilon = (
            (
                np.asarray(
                    [[20.0, 60.0], [15.0, 40.0], [2.0, 10.0],]
                )  # C  # F  # H
                * u.K
                * u.kb
            )
            .in_units("kJ/mol")
            .value
        )

        bounds = np.vstack((bounds_sigma, bounds_epsilon))

        return bounds

    @property
    def expt_liq_density(self):
        """Return a dictionary with experimental liquid density

        Temperature units K
        Density units kg/m**3
        """

        expt_liq_density = {
            243: 1151.0,
            263: 1088.8,
            283: 1019.7,
            303: 939.62,
            323: 839.26,
        }

        return expt_liq_density

    @property
    def expt_vap_density(self):
        """Return a dictionary with experimental vapor density
        Temperature units K
        Density units kg/m**3
        """

        expt_vap_density = {
            243: 7.6389,
            263: 15.870,
            283: 30.232,
            303: 54.776,
            323: 98.55,
        }

        return expt_vap_density

    @property
    def expt_Pvap(self):
        """Return a dictionary with experimental vapor pressure
        Temperature units K
        Vapor pressure units bar
        """

        expt_Pvap = {
            243: 2.7344,
            263: 5.8263,
            283: 11.0690,
            303: 19.2750,
            323: 31.4120,
        }

        return expt_Pvap

    @property
    def expt_Hvap(self):
        """Return a dictionary with experimental enthalpy of vaporization
        Temperature units K
        Vapor pressure units kJ/kg
        """

        expt_Hvap = {
            243: 356.82,
            263: 330.26,
            283: 298.92,
            303: 260.40,
            323: 209.61,
        }

        return expt_Hvap


    @property
    def temperature_bounds(self):
        """Return the bounds on temperature in units of K"""

        bounds = (np.asarray([243, 323],) * u.K).value

        return bounds


    @property
    def liq_density_bounds(self):
        """Return the bounds on liquid density in units of kg/m^3"""

        bounds = (np.asarray([839.26, 1151.0],) * u.Unit("kg/m**3")).value

        return bounds


    @property
    def vap_density_bounds(self):
        """Return the bounds on vapor density in units of kg/m^3"""

        bounds = (np.asarray([7.6389, 98.55],) * u.Unit("kg/m**3")).value

        return bounds


    @property
    def Pvap_bounds(self):
        """Return the bounds on vapor pressure in units of bar"""

        bounds = (np.asarray([2.7344, 31.4120],) * u.Unit("bar")).value

        return bounds


    @property
    def Hvap_bounds(self):
        """Return the bounds on enthaply of vaporization in units of kJ/kg"""

        bounds = (np.asarray([209.61, 356.82],) * u.Unit("kJ/kg")).value

        return bounds
