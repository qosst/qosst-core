"""
Generic timing recovery estimator.
"""
import abc
from typing import Optional

import numpy as np


# pylint: disable=too-few-public-methods
class TimingRecoveryEstimator(abc.ABC):
    """
    Abstract class for the timing recovery estimator.
    """

    def __init__(self, **_kwargs) -> None:
        pass

    @abc.abstractmethod
    def sample(self) -> np.ndarray:
        """
        Estimate the timing.

        Returns:
            np.ndarray: the estimated timing.
        """