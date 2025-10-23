from typing import TypeVar


from sampling_mining_workflows_dsl.Workflow import Workflow
from sampling_mining_workflows_dsl.analysis.HistAnalysis import HistAnalysis
from sampling_mining_workflows_dsl.analysis.WorkflowAnalysis import WorkflowAnalysis
from sampling_mining_workflows_dsl.analysis.kolmogorov_smirnov import kolmogorov_smirnov
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.operator.clustering.GroupingOperator import (
    GroupingOperator,
)

T = TypeVar("T")


class KSWorkflowAnalysis(WorkflowAnalysis):
    def __init__(
        self,
        metadata: Metadata[T],
        output_path: str = "analysis/",
    ):
        super().__init__()

        self.metadata = metadata
        self.file_path = output_path+"ks_analysis.txt"

    def analyze(
        self, workflow, workflow_name: str = "main workflow", op_number: int = 1
    ):
        #create an output file
        print(f"KS Analysis results will be saved in {self.file_path}")


        #compute for all pair
        tuples = self.get_all_set_from_workflow(workflow)
        for i in range(1, len(tuples)+1):
            for j in range(i+1, len(tuples)+1):
                set_1, op_1 = tuples[i]
                set_2, op_2 = tuples[j]
                # Here you can call your analysis method on set_1 and set_2
                print(f"Analyzing sets {i} from {op_1.__class__.__name__} and {j} from {op_2.__class__.__name__} ")
                # Example: KSAnalysis(self.metadata).analyze(set_1, set_2)
                print(kolmogorov_smirnov(self.metadata).analyze(set_1, set_2))

                


    
    def get_all_set_from_workflow(self, workflow: Workflow, index=1):
        sets = {}
        if index==1:
            sets[index] = (workflow._input,None)
            index += 1

        op = workflow.get_root()
        while op is not None:
            if not isinstance(op, GroupingOperator):
                if hasattr(op, "_output") and op._output is not None:
                    sets[index] = (op._output,op)  # Fix: use index as key, not the Set object
                    index += 1
            else:
                for internal_w in op.get_workflows():
                    grouping_sets = self.get_all_set_from_workflow(internal_w, index)
                    index = index + len(grouping_sets)
                    sets.update(grouping_sets)  # Fix: use update() instead of extend()
            op = op.get_next_operator()

        return sets
