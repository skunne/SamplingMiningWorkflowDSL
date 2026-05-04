from abc import ABC, abstractmethod

from sampling_mining_workflows_dsl.element.Set import EagerSet


class Writer(ABC):
    @abstractmethod
    def write_set(self, set: EagerSet):
        pass
