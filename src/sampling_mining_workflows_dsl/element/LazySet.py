import random
from functools import cmp_to_key
from collections import OrderedDict

from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.element.Set import Set


class LazySet(Set):
    def __init__(self):
        super().__init__()
        self.n_seen = 0

    def __hash__(self):
        raise NotImplementedError
        # return hash(tuple(self.elements.items)) + super().__hash__()

    def __eq__(self, other):
        raise NotImplementedError
        # if not super().__eq__(other):
        #     return False
        # if not isinstance(other, Set):
        #     return False
        # return self.elements == other.elements
    
    def get_element_by_index(self, index: int) -> Element:
        raise NotImplementedError
        # if index < 0 or index >= len(self.elements):
        #     raise IndexError("Index out of range")
        # return list(self.elements.values())[index]
    def __next__(self) -> Element:
        pass
    def __iter__(self):
        return self
    
    def remove_all_elements(self) -> "Set":
        raise NotImplementedError
        # self.elements.clear()
        # self.ids.clear()
        # return self
    def add_element(self, element: Element) -> "Set":
        raise NotImplementedError
        # if not element.get_id() in self.ids:
        #     self.elements[element.get_id()]=element
        #     self.ids.add(element.get_id())
        # else :
        #     print(f"{element.get_id()} Already present")

        # return self

    def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> "Set":
        raise NotImplementedError
        # # Sort the items of the OrderedDict
        # sorted_items = sorted(
        #     self.elements.items(),
        #     key=cmp_to_key(lambda x, y: comparator.compare(x[1], y[1])),
        #     reverse=reverse
        # )
    
        # # Rebuild as OrderedDict
        # self.elements = OrderedDict(sorted_items)
        # return self

    def get_depth(self) -> int:
        raise NotImplementedError
        # max_depth = 1
        # for element in self.elements.values():
        #     if isinstance(element, Set):
        #         max_depth = max(max_depth, 1 + element.get_depth())
        # return max_depth
    
    def union(self, other: "Set") -> "UnionLazySet":
        return UnionLazySet(self, other)
    
    def intersection(self, other: "Set") -> "IntersectionLazySet":
        return IntersectionLazySet(self, other)
    
    def difference(self, other: "Set") -> "Set":
        """Return a new set with elements in this set but not in other"""
        return DifferenceLazySet(self, other)
    
    def symmetric_difference(self, other: "Set") -> "Set":
        raise NotImplementedError
        # """Return a new set with elements in either set but not in both"""
        # sym_diff = Set()
        
        # # Add elements from this set that are not in other
        # for id, element in self.elements.items():
        #     if id not in other.elements.keys():
        #         sym_diff.add_element(element)
        
        # # Add elements from other set that are not in this
        # for id, element in other.elements.items():
        #     if id not in self.elements.keys():
        #         sym_diff.add_element(element)
        
        # return sym_diff
    
    def is_subset(self, other: "Set") -> bool:
        raise NotImplementedError
        # """Return True if all elements in this set are also in other"""
        # for id in self.elements.keys():
        #     if id not in other.elements.keys():
        #         return False
        # return True
    
    def is_superset(self, other: "Set") -> bool:
        raise NotImplementedError
        # """Return True if all elements in other set are also in this set"""
        # return other.is_subset(self)
    
    def is_disjoint(self, other: "Set") -> bool:
        raise NotImplementedError
        # """Return True if this set and other have no elements in common"""
        # for id in self.elements.keys():
        #     if id in other.elements.keys():
        #         return False
        # return True
    
    def is_empty(self) -> bool:
        """Return True if the set is empty"""
        # if self.n_seen > 0:
        #     return False
        # else:
        #     raise NotImplementedError
        raise NotImplementedError
        #return len(self.elements) == 0
    
    def size(self) -> int:
        raise NotImplementedError
        # TODO: add a self.fully_itered flag initially set to False, then set to True when we finish the iterator
        # if self.fully_itered:
        #     return self.n_seen
        # else:
        #     raise SomeCustomException
        return len(self.elements)

    def get_element(self, id: str) -> Element:
        raise NotImplementedError
        # if not id  in self.elements.keys():
        #     raise RuntimeError(f"Element with id {id} not found in the set")
        # return self.elements.get(id)
    
    def set_id(self, set_id: str) -> "Set":
        self.set_id = set_id
        return self 

    def get_id(self):
        if self.set_id is not None:
            return self.set_id
        
        set_id = ""
        for id in self.elements.keys():
            set_id = set_id + "_" + str(id)
        return set_id

    def flatten_set(self) -> "Set":
        raise NotImplementedError
        # flattened = Set()
        # for element in self.get_elements():
        #     if isinstance(element, Set):
        #         # Recursively flatten nested Sets
        #         flattened.union(element.flatten_set())
        #     else:
        #         # Add non-Set, non-list elements directly
        #         flattened.add_element(element)
        # return flattened

    def get_random_subset(self, subset_size: int, seed: int) -> "Set":
        # Reservoir sampling algorithm R
        reservoir = [next(self) for _ in range(subset_size)]
        random.seed(seed)
        for i, x in enumerate(self, start = subset_size):
            j = random.randrange(i+1)
            if j < subset_size:
                reservoir[j] = x

        result = Set()
        for x in reservoir:
            result.add_element(x)
        return result

    def get_elements(self) -> list[Element]:
        raise NotImplementedError
        # return list(self.elements.values())
    
    def clone(self) -> "Set":
        raise NotImplementedError
        # cloned_set = Set()
        # for element in self.get_elements():
        #     cloned_set.add_element(element)
        # return cloned_set
    
    def __str__(self) -> str:
        raise NotImplementedError
        # return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        raise NotImplementedError
        # truncate_after = 10
        # indent = "    " * level

        # result = f"{indent}(size={len(self.elements)})["
        # elements_list = self.get_elements()
        # element_to_print = min(truncate_after, len(self.elements))

        # for i in range(element_to_print):
        #     next_element = elements_list[i]

        #     if isinstance(next_element, Set):
        #         # Recursively call to_string for nested Sets
        #         result += f"\n{next_element.to_string(level + 4)}"
        #     else:
        #         result += str(next_element)

        #     if i != element_to_print - 1:
        #         result += ","

        # if len(self.elements) > truncate_after:
        #     result += "...]"
        # else:
        #     result += "]"

        # return result

class UnionLazySet(LazySet):
    def __init__(self, lazy_set: LazySet, other: Set | LazySet):
        super().__init__()
        self.lazy_set = lazy_set
        if isinstance(other, LazySet):
            self.other = other
        else:
            self.other = iter(other.elements)
    def __next__(self) -> Element:
        try:
            x = next(self.lazy_set)
        except StopIteration:
            x = next(self.other)
        return x
    
class IntersectionLazySet(LazySet):
    def __init__(self, lazy_set: LazySet, other: Set):
        super().__init__()
        self.lazy_set = lazy_set
        self.other = other
    def __next__(self) -> Element:
        x = next(self.lazy_set)
        while x not in self.other.elements:
            x = next(self.lazy_set)
        return x
    
class DifferenceLazySet(LazySet):
    def __init__(self, lazy_set: LazySet, minus_set: Set):
        super().__init__()
        self.lazy_set = lazy_set
        self.minus_set = minus_set
    def __next__(self) -> Element:
        x = next(self.lazy_set)
        while x in self.minus_set.elements:
            x = next(self.lazy_set)
        return x

    
class FilteredLazySet(LazySet):
    def __init__(self, lazy_set, predicate):
        super().__init__()
        self.lazy_set = lazy_set
        self.predicate = predicate
    def __next__(self) -> Element:
        x = next(self.lazy_set)
        while not self.predicate(x):
            x = next(self.lazy_set)
        return x

