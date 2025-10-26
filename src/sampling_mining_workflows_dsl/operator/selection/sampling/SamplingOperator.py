
from sampling_mining_workflows_dsl.operator.selection.SelectionOperator import SelectionOperator


class SamplingOperator(SelectionOperator):
    def __init__(self, workflow, cardinality: int):
        super().__init__(workflow)
        self._cardinality = cardinality
    def get_cardinality(self):
        return self._cardinality
        
