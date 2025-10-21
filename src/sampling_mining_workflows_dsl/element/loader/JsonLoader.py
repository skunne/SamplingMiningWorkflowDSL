import json
from pathlib import Path
from typing import TYPE_CHECKING, Any
import logging
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue


class JsonLoader(Loader):
    def __init__(self, set_path: Path, *metadatas: Metadata):
        super().__init__(*metadatas)
        self.set_path = set_path
        self.set = Set()

    def load_set(self) -> Set:
        try:
            if self.set_path.is_dir():
                json_files = sorted(self.set_path.glob("*.json"))
                if not json_files:
                    raise RuntimeError(
                        f"No JSON files found in directory: {self.set_path}"
                    )
            else:
                if not self.set_path.exists():
                    raise RuntimeError(f"File not found: {self.set_path}")
                json_files = [self.set_path]

            for json_file in json_files:
                print(f"Loading JSON file: {json_file}")
                with json_file.open("r") as reader:
                    json_list: list[dict[str, Any]] = json.load(reader)
                    for json_obj in json_list:
                        try:
                            repository = self.create_repository_from_map(json_obj)
                            if repository is not None:
                                self.set.add_element(repository)
                        except Exception as e:
                            logging.info(f"Row skipped due to {e} : {json_obj}")
            return self.set
        except OSError as e:
            raise RuntimeError("Error reading the JSON file", e) from e

    def create_repository_from_map(self, json_object: dict[str, Any]) -> Repository:
        id_metadata_value = json_object.get(self.metadata_id_name)

        if id_metadata_value is None or id_metadata_value == "":
            raise ValueError(f"Invalid ID {self.metadata_id_name}")

        repo = Repository(self.metadatas.get(self.metadata_id_name))

        metadata_values: list[MetadataValue] = []
        for metadata in self.metadatas.values():
            try:
                metadata_value = metadata.create_metadata_value(json_object.get(metadata.name))
                metadata_values.append(metadata_value)
            except Exception as e:
                raise ValueError(
                    f"Error creating metadata value for '{metadata.name}' with value '{json_object.get(metadata.name)}'",
                ) from e

        repo.add_metadata_values(metadata_values)
        return repo

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, str]:
        import argparse

        default_input_path = Path(__file__).parent / "input.json"

        parser = argparse.ArgumentParser(description="Sampling Workflow")
        parser.add_argument(
            "-i",
            "--inputPath",
            type=str,
            default=str(default_input_path),
            help="Input path file",
        )
        parsed_args = parser.parse_args(args)
        return vars(parsed_args)
