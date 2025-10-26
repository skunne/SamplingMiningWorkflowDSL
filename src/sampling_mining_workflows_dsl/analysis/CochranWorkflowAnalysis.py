from sampling_mining_workflows_dsl.Workflow import Workflow
from sampling_mining_workflows_dsl.analysis.WorkflowAnalysis import WorkflowAnalysis
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from sampling_mining_workflows_dsl.analysis.CochranTest import CochranTest


class CochranWorkflowAnalysis(WorkflowAnalysis):
    def init(self,confidence_level=0.95,margin_error=0.05,p=0.5):
        super().init()
        self.confidence_level=confidence_level
        self.margin_error=margin_error
        self.p=p

    def analyze(self,workflow : Workflow):
        #dict set_num --> (set,op) 
        set_op_dict = workflow.get_all_set_from_workflow()
        for (set_nb,value) in set_op_dict.items():
            set_id,op = value
            if isinstance(op,RandomSelectionOperator):
                print(f"Set #{set_id} produced by a random selection operator, checking sample size")
                cochran_test = CochranTest(op,self.confidence_level,self.margin_error,self.p)
                required_sample_size = cochran_test.cochran_sample_size()
                actual_sample_size = op.cardinality
                print(f"Cochran's Test Analysis for set {set_nb}:")
                print("Required Sample Size:", required_sample_size)
                print("Actual Sample Size:", actual_sample_size)

                if cochran_test.is_representative():
                    print("The sample is representative based on Cochran's test.")
                else:
                    print("The sample is not representative based on Cochran's test.")

                print("------------------------------------------")

        
 
    
        
