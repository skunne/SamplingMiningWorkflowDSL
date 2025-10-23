import os
from collections import Counter
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata import MetadataValue


class HistAnalysis:
    def __init__(
        self,
        save_path: str,
        metadata: Metadata,
        top_x: int = -1,
        category: bool = True,
        sort: bool = False,
        show: bool = False,
        log_y: bool = False,
        fixed_bins: int = None,
        max_x_bound: float = None,
    ):
        self.metadata = metadata
        # Wether data should be treated as categorical data or continous
        self.category = category
        self.top_x = top_x
        self.sort = sort
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)
        self.show = show
        self.log_y = log_y
        self.fixed_bins = fixed_bins
        self.max_x_bound = max_x_bound

    def analyze(self, s: Set, file_name: str, op_info: str):
        # From Set to List of Metadata values
        try:
            metadata_values = []
            for element in s.get_elements():
                if not isinstance(element, Set):
                    metadata_value: MetadataValue = element.get_metadata_value(
                        self.metadata
                    )
                    if self.metadata.type is list:
                        metadata_values.extend(metadata_value.get_value())
                    else:
                        metadata_values.append(metadata_value.get_value())

            if self.top_x > 0:
                # Count all and find top_x
                counter = Counter(metadata_values)
                most_common = dict(counter.most_common(self.top_x))
                top_values = set(most_common.keys())

                # Replace non-top values with 'Other'
                metadata_values = [
                    val if val in top_values else "Other" for val in metadata_values
                ]

            fig, ax = self.create_histogram(metadata_values, op_info)
            if self.show:    
                self.show_histogram()
            self.save_histogram(fig, file_name)
        except Exception as e:
            print(f"Error analyzing {self.metadata.name}: {e}")
            return

    def create_histogram(self, data: list, op_info: str):
        df = pd.DataFrame(data, columns=["value"])
        series = df["value"]

        # Apply max x bound filter if specified
        if self.max_x_bound is not None and not self.category:
            # Only filter for continuous data
            filtered_data = [x for x in data if x <= self.max_x_bound]
            df = pd.DataFrame(filtered_data, columns=["value"])
            series = df["value"]
            data = filtered_data

        unique_values = series.nunique()

        fig, ax = plt.subplots()
        if not self.category:
            # Determine number of bins
            if self.fixed_bins is not None:
                bins = self.fixed_bins
            else:
                bins = min(10, unique_values)
            
            ax.hist(x=data, bins=bins)
            
            if self.log_y:
                ax.set_yscale('log')
            
            # Set x-axis limit if max_x_bound is specified
            if self.max_x_bound is not None:
                ax.set_xlim(right=self.max_x_bound)
        else:
            if self.sort:
                value_counts = series.value_counts(ascending=False, sort=True)
            else:
                value_counts = series.value_counts().sort_index(ascending=True)
            value_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Category")
            # Note: log scale and x bounds don't make sense for categorical data (bar charts)
            # so we only apply them to continuous histograms

        ax.set_title(op_info)
        ax.set_ylabel("Frequency")
        
        # Format axis numbers with separators
        # Format x-axis with space separators for thousands
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}".replace(',', ' ')))
        # Format y-axis with space separators for thousands
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}".replace(',', ' ')))
        
        plt.tight_layout()
        return fig, ax

    def save_histogram(self, fig, file_name: str):
        
        if file_name:
            # Create folder if needed
            os.makedirs(self.save_path, exist_ok=True)
            file_path = os.path.join(self.save_path, file_name)
            fig.savefig(file_path)
        else:
            print("No save path provided, displaying histogram instead.")
            self.show_histogram()
        plt.close(fig)

    def show_histogram(self):
        plt.show()
