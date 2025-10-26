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
        output_path: str = "analysis",
    ):
        super().__init__()

        self.metadata = metadata
        self.file_path = output_path+"/ks_analysis.txt"

    def analyze(
        self, workflow
    ):
        import os
        from datetime import datetime
        
        # Create all directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)        
        print(f"KS Analysis results will be saved in {self.file_path}")
        
        # Store pairs that pass the test
        passing_pairs = []
        failing_pairs = []
        
        # Open file for writing
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"Kolmogorov-Smirnov Analysis Results\n")
            f.write(f"{'='*50}\n")
            f.write(f"Metadata: {self.metadata.name}\n")
            f.write(f"{'='*50}\n\n")

            #compute for all pair
            tuples = self.get_all_set_from_workflow(workflow)
            
            if len(tuples) < 2:
                f.write("Warning: Less than 2 sets found. Cannot perform pairwise analysis.\n")
                print("Warning: Less than 2 sets found. Cannot perform pairwise analysis.")
                return
            
            comparison_count = 0
            for i in range(1, len(tuples)+1):
                for j in range(i+1, len(tuples)+1):
                    set_1, op_1 = tuples[i]
                    set_2, op_2 = tuples[j]
                    
                    comparison_count += 1
                    
                    # Write comparison header
                    op_1_name = op_1.__class__.__name__ if op_1 else 'Initial set'
                    op_1_name = f"Set #{i}"+op_1_name
                    op_2_name = op_2.__class__.__name__ if op_2 else 'Initial Input'
                    op_2_name = f"Set #{j}"+op_2_name
                    f.write(f"Comparison #{comparison_count}\n")
                    f.write(f"Set 1: {op_1_name} (size: {set_1.size()})\n")
                    f.write(f"Set 2: {op_2_name} (size: {set_2.size()})\n")
                    f.write(f"{'-'*30}\n")
                    
                    # Perform KS analysis
                    print(f"Analyzing sets {i} from {op_1_name} and {j} from {op_2_name}")
                    
                    try:
                        ks_result = kolmogorov_smirnov(self.metadata).analyze(set_1, set_2)
                        
                        # Extract results from KstestResult object
                        statistic = ks_result.statistic if hasattr(ks_result, 'statistic') else 'N/A'
                        p_value = ks_result.pvalue if hasattr(ks_result, 'pvalue') else 'N/A'
                        
                        # Create interpretation
                        if p_value != 'N/A':
                            if p_value > 0.05:
                                interpretation = "No significant difference (p > 0.05)"
                            else:
                                interpretation = "Significant difference detected (p ≤ 0.05)"
                        else:
                            interpretation = "Unable to determine"
                        
                        # Check if test passes (typically p_value > 0.05 means no significant difference)
                        test_passed = p_value != 'N/A' and float(p_value) > 0.05
                        
                        pair_info = {
                            'comparison': comparison_count,
                            'set_1': op_1_name,
                            'set_2': op_2_name,
                            'statistic': statistic,
                            'p_value': p_value,
                            'interpretation': interpretation
                        }
                        
                        if test_passed:
                            passing_pairs.append(pair_info)
                            f.write(f"✓ TEST PASSED - ")
                        else:
                            failing_pairs.append(pair_info)
                            f.write(f"✗ TEST FAILED - ")
                        
                        # Write results to file
                        f.write(f"KS Statistic: {statistic}\n")
                        f.write(f"P-value: {p_value}\n")
                        f.write(f"Interpretation: {interpretation}\n")
                        
                        # Print to console as well
                        status = "PASSED" if test_passed else "FAILED"
                        print(f"  [{status}] KS Statistic: {statistic}, P-value: {p_value}")
                        
                    except Exception as e:
                        error_msg = f"Error during analysis: {str(e)}"
                        f.write(f"{error_msg}\n")
                        print(f"  {error_msg}")
                        failing_pairs.append({
                            'comparison': comparison_count,
                            'set_1': op_1_name,
                            'set_2': op_2_name,
                            'error': str(e)
                        })
                    
                    f.write(f"\n")
            
            # Write summary section
            f.write(f"\n{'='*50}\n")
            f.write(f"SUMMARY\n")
            f.write(f"{'='*50}\n")
            f.write(f"Total comparisons: {comparison_count}\n")
            f.write(f"Tests passed: {len(passing_pairs)}\n")
            f.write(f"Tests failed: {len(failing_pairs)}\n")
            f.write(f"\nPassing pairs (no significant difference):\n")
            f.write(f"{'-'*30}\n")
            
            if passing_pairs:
                for pair in passing_pairs:
                    f.write(f"• {pair['set_1']} vs {pair['set_2']} (p-value: {pair['p_value']})\n")
            else:
                f.write("None\n")
            
            f.write(f"\nFailing pairs (significant difference detected):\n")
            f.write(f"{'-'*30}\n")
            
            if failing_pairs:
                for pair in failing_pairs:
                    if 'error' in pair:
                        f.write(f"• {pair['set_1']} vs {pair['set_2']} (Error: {pair['error']})\n")
                    else:
                        f.write(f"• {pair['set_1']} vs {pair['set_2']} (p-value: {pair['p_value']})\n")
            else:
                f.write("None\n")
            
            f.write(f"\nAnalysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Print summary to console
        print(f"\n{'='*50}")
        print(f"KS ANALYSIS SUMMARY")
        print(f"{'='*50}")
        print(f"Total comparisons: {comparison_count}")
        print(f"Tests passed: {len(passing_pairs)}")
        print(f"Tests failed: {len(failing_pairs)}")
        
        if passing_pairs:
            print(f"\nPassing pairs (no significant difference):")
            for pair in passing_pairs:
                print(f"  ✓ {pair['set_1']} vs {pair['set_2']} (p-value: {pair['p_value']})")
        
        if failing_pairs:
            print(f"\nFailing pairs (significant difference detected):")
            for pair in failing_pairs:
                if 'error' in pair:
                    print(f"  ✗ {pair['set_1']} vs {pair['set_2']} (Error)")
                else:
                    print(f"  ✗ {pair['set_1']} vs {pair['set_2']} (p-value: {pair['p_value']})")
        
        print(f"\nResults saved to: {self.file_path}")
        
        return {
            'passing_pairs': passing_pairs,
            'failing_pairs': failing_pairs,
            'total_comparisons': comparison_count
        }

                


    
    def get_all_set_from_workflow(self, workflow: Workflow, index=0):
        sets = {}
        if index==0:
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
