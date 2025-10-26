import math

from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from scipy.stats import norm

class CochranTest:
    def __init__(self, op :RandomSelectionOperator,confidence_level=0.95,margin_error=0.05,p=0.5):
        self.op: RandomSelectionOperator  = op
        self.confidence_level=confidence_level
        self.e=margin_error
        self.p=p
    """
        Calculate sample size using Cochran's formula.

        Parameters:
            confidence_level (float): Confidence level (e.g. 0.95 for 95%)
            p (float): Estimated proportion of the population (use 0.5 if unknown)
            e (float): Margin of error (e.g. 0.05 for 5%)
            population (int or None): Population size, optional for finite correction

        Returns:
            float: Required sample size
    """
    def cochran_sample_size(self):
        sampling_frame_size = len(self.op.get_input())

        # Get Z-value for given confidence level
        z = norm.ppf(1 - (1 - self.confidence_level) / 2)

        # Cochran's initial sample size
        n0 = (z**2 * self.p * (1 - self.p)) / (self.e**2)

        # Adjust for finite population if given
        if sampling_frame_size:
            n = n0 / (1 + (n0 - 1) / sampling_frame_size)
            return n
        else:
            return n0


    def is_representative(self) -> bool:
        required_sample_size = self.cochran_sample_size
        sample_size = self.op.cardinality
        return sample_size >= required_sample_size
