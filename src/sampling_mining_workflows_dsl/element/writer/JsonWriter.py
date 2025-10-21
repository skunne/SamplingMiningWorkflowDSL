import json
from datetime import datetime, date
from pathlib import Path

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set


# Note: Can handle both flat sets (depth 1) and nested sets (depth > 1)
class JsonWriter:
    def __init__(self, set_path: str):
        self.set_path = Path(set_path)

    def write_set(self, set_obj: Set):
        if not isinstance(set_obj, Set):
            raise TypeError("Expected a Set object")

        elements = set_obj.elements.values()

        if not elements:
            raise ValueError("The set is empty. Nothing to write.")

        rows = [self._serialize_element(elem) for elem in elements]

        try:
            with self.set_path.open("w", encoding="utf-8") as f:
                json.dump(rows, f, indent=4, ensure_ascii=False)
            print(f"JSON has been written to {self.set_path}")
        except OSError as e:
            raise RuntimeError("Error while saving file") from e

    def _serialize_element(self, element):
        """Serialize an element, which can be a Repository or a Set."""
        if isinstance(element, Set):
            # Nested Set: serialize as an array of elements
            return [self._serialize_element(elem) for elem in element.elements.values()]
        elif isinstance(element, Repository):
            return self._serialize_repository(element)
        else:
            raise TypeError(f"Unexpected element type: {type(element)}")

    def _serialize_repository(self, repo: Repository):
        if not isinstance(repo, Repository):
            raise TypeError("Expected Repository elements in the set")

        result = {}
        for meta, val in repo.get_all_metadata_values().items():
            value = val.get_value()
            # Convert datetime/date to timestamp
            if isinstance(value, (datetime, date)):
                if isinstance(value, datetime):
                    value = int(value.timestamp())
                else:  # date object
                    value = int(datetime.combine(value, datetime.min.time()).timestamp())
            # Keep lists as lists in JSON (no need to join like CSV)
            result[meta.name] = value
        return result
