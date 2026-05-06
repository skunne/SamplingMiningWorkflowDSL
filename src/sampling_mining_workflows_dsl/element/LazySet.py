import random
from itertools import chain, islice
from functools import cmp_to_key
from collections import OrderedDict

from typing import Self, Iterable, TYPE_CHECKING

from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.element.Repository import Repository

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.element.EagerSet import EagerSet


class LazySet(Element):
    def __init__(self, iterator):
        super().__init__()
        self.iterator = iterator
        # self.n_seen = 0             # TODO number of elements already iterated through
        # self.fully_consumed = False # TODO becomes True as soon as we encounter StopIteration
    
    @classmethod
    def from_iter_of_maps(cls, metadatas, maps: Iterable) -> Self:
        id = metadatas[0]
        def it():
            for row in maps:
                repo = Repository(id)
                metadata_values = [m.create_metadata_value(row[m.name]) for m in metadatas]
                repo.add_metadata_values(metadata_values)
                yield repo
        return cls(it())

    def __hash__(self):
        raise NotImplementedError
        # return hash(tuple(self.elements.items)) + super().__hash__()

    def __eq__(self, other):
        raise NotImplementedError
        # if not super().__eq__(other):
        #     return False
        # if not isinstance(other, LazySet):
        #     return False
        # return self.elements == other.elements
    
    def get_element_by_index(self, index: int) -> Element:
        raise NotImplementedError
        # if index < 0 or index >= len(self.elements):
        #     raise IndexError("Index out of range")
        # return list(self.elements.values())[index]

    def __next__(self) -> Element:
        return next(self.iterator)
    
    def __iter__(self):
        return self.iterator
    
    def remove_all_elements(self) -> Self:
        raise NotImplementedError
        # self.elements.clear()
        # self.ids.clear()
        # return self

    def add_element(self, element: Element) -> Self:
        raise NotImplementedError
        # if not element.get_id() in self.ids:
        #     self.elements[element.get_id()]=element
        #     self.ids.add(element.get_id())
        # else :
        #     print(f"{element.get_id()} Already present")
        # return self

    def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> Self:
        raise NotImplementedError

    def get_depth(self) -> int:
        raise NotImplementedError
        # max_depth = 1
        # for element in self.elements.values():
        #     if isinstance(element, LazySet):
        #         max_depth = max(max_depth, 1 + element.get_depth())
        # return max_depth
    
    def union(self, other: Iterable) -> Self:
        other_iterator = iter(other)
        iterator = chain(self.iterator, other_iterator)
        return type(self)(iterator)
    
    def intersection(self, other: "EagerSet") -> Self:
        iterator = (x for x in self if x.get_id() in other.elements)
        return type(self)(iterator)
    
    def difference(self, other: "EagerSet") -> Self:
        """Return a new set with elements in this set but not in other"""
        iterator = (x for x in self if x.get_id() not in other.elements)
        return type(self)(iterator)
    
    def symmetric_difference(self, other: "EagerSet") -> Self:
        # """Return a new set with elements in either set but not in both"""
        raise NotImplementedError
    
    def is_subset(self, other: "EagerSet") -> bool:
        raise NotImplementedError
        # """Return True if all elements in this set are also in other"""
        # for id in self.elements.keys():
        #     if id not in other.elements.keys():
        #         return False
        # return True
    
    def is_superset(self, other: "EagerSet") -> bool:
        raise NotImplementedError
        # """Return True if all elements in other set are also in this set"""
        # return other.is_subset(self)
    
    def is_disjoint(self, other: "EagerSet") -> bool:
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
        # TODO
        # if self.fully_consumed:
        #     return self.n_seen
        # else:
        #     raise SomeCustomException

    def get_element(self, id: str) -> Element:
        raise NotImplementedError
        # if not id  in self.elements.keys():
        #     raise RuntimeError(f"Element with id {id} not found in the set")
        # return self.elements.get(id)
    
    # def set_id(self, set_id: str) -> Self:
    #     raise NotImplementedError
    #     self.set_id = set_id
    #     return self 

    def get_id(self):
        return str(id(self))

    def flatten_set(self) -> Self:
        def flattened(s):
            for x in s:
                if isinstance(x, LazySet):
                    yield from flattened(x)
                else:
                    yield x
        return type(self)(flattened(self))

    def get_random_subset(self, subset_size: int, seed: int) -> Self:
        '''Reservoir sampling algorithm R'''
        reservoir = list(islice(self, subset_size))
        if subset_size > len(reservoir):
            print(f"Caution, subset size is larger than the size of the original set, subset size: {subset_size}, current set size: {len(reservoir)}")
            subset_size = len(reservoir)
            return type(self)(iter(reservoir))
        random.seed(seed)
        for i, x in enumerate(self, start = subset_size):
            j = random.randrange(i+1)
            if j < subset_size:
                reservoir[j] = x
        return type(self)(iter(reservoir))

    def get_elements(self) -> list[Element]:
        raise NotImplementedError
        # return list(self.elements.values())
    
    def clone(self) -> Self:
        raise NotImplementedError
        iter1, iter2 = itertools.tee(self.iterator) # not recommended
        self.iterator = iter1
        return LazySet(iter2)
    
    def __str__(self) -> str:
        raise NotImplementedError
        # return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        raise NotImplementedError
