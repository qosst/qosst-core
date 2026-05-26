"""
Generic phase estimator.
"""
import abc
from typing import Optional

import numpy as np


# pylint: disable=too-few-public-methods
class PhaseEstimator(abc.ABC):
    """
    Abstract class for the phase estimator.
    """

    def __init__(self, **_kwargs) -> None:
        pass

    @abc.abstractmethod
    def estimate_phase(self, **kwargs) -> np.ndarray:
        """
        Estimate the phase.

        Returns:
            np.ndarray: the estimated phase.
        """
        pass
