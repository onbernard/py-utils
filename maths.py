from typing import (
    Tuple
)
import math


class MeanDevCounter:
    """~~Number of time someone on the dev team called me a fattie :(~~
    
    Iterative computation of mean and standard deviation
    """
    def __init__(self) -> None:
        self.n = 0
        self.s_1 = 0
        self.s_2 = 0

    @property
    def mu(self) -> float:
        """Get the current mean

        :return: mean
        :rtype: float
        """
        return self.s_1/self.n

    @property
    def sigma(self) -> float:
        """Get the current deviation

        :return: _description_
        :rtype: float
        """
        return math.sqrt(self.s_2/self.n - self.mu**2)

    def __call__(self, value: float) -> Tuple[float,float]:
        """Compute the next mean, sd given a `value`

        :param val: Numerical value
        :type val: float
        :return: A tuple containing the mean and standard deviation
        :rtype: Tuple[float,float]
        """
        self.n += 1
        self.s_1 += value
        self.s_2 += value**2
        return (self.mu, self.sigma)