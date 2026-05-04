import pytest

from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.element.Set import EagerSet
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

def test_from_dataset():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    dataset = {"val": list(range(10)), "irrelevant": list("ABCDEFGHIJ"), "id": list(map(str, range(10))), "double": list(range(0,20,2))}

    eager_set = EagerSet.from_dataset(metadatas, dataset)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size == 10)

    element0 = eager_set.get_element_by_index(0)
    e = Repository(metadatas[0].name)
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)

def test_from_iter_of_maps():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    it = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x], "id": str(x), "double": 2*x} for x in range(10)]

    eager_set = EagerSet.from_iter_of_maps(metadatas, it)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size == 10)

    element0 = eager_set.get_element_by_index(0)
    e = Repository(metadatas[0].name)
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)
    
def test_from_lazyset():
    elements = [(str(x), x, 2*x) for x in range(10)]
    lazy_set = LazySet(iter(elements))

    eager_set = EagerSet.from_lazyset(lazy_set)
    assert(isinstance(eager_set, EagerSet))
    assert(eager_set.size == 10)

    element0 = eager_set.get_element_by_index(0)
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    e = Repository(metadatas[0].name)
    e.add_metadata_values([metadatas[0].create_metadata_value("0"), metadatas[1].create_metadata_value(0), metadatas[2].create_metadata_value(0)])
    assert(element0 == e)
    
def test_allcreationsareequal():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    dataset = {"val": list(range(10)), "irrelevant": list("ABCDEFGHIJ"), "id": list(map(str, range(10))), "double": list(range(0,20,2))}
    maps = [{"val": x, "irrelevant": "ABCDEFGHIJ"[x], "id": str(x), "double": 2*x} for x in range(10)]
    lazy_set = LazySet(((str(x), x, 2*x) for x in range(10)))

    set_from_ds = EagerSet.from_dataset(metadatas, dataset)
    set_from_maps = EagerSet.from_iter_of_maps(metadatas, maps)
    set_from_lazy = EagerSet.from_lazyset

    assert(set_from_ds == set_from_maps)
    assert(set_from_maps == set_from_lazy)



def test_iter():
    metadatas = [Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")]
    elements = [(str(x), x, 2*x) for x in range(10)]
    es = EagerSet.from_iter(iter(elements))
    for x,y in zip(iter(es), elements, strict=True):
        ry = Repository(metadatas[0].name)
        ry.add_metadata_values(y)
        assert(x == y)

def test_hash():
    es1 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(10)))
    es2 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(100, 103)))
    assert(hash(es1) != hash(es2))
    s = {es1, es2}
    
def test_eq():
    es1 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(10)))
    es2 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(100, 103)))
    es3 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(10)))
    
    assert(es1 == es1)
    assert(es1 != es2)
    assert(es1 == es3)
    
    assert(es2 != es1)
    assert(es2 == es2)
    assert(es2 != es3)

    assert(es3 == es1)
    assert(es3 != es2)
    assert(es3 == es3)
    
def test_get_element_by_index():
    es1 = EagerSet.from_iter(((str(x), x, 2*x) for x in range(10)))
    with pytest.raises(IndexError):
        es1.get_element_by_index(-11)
    with pytest.raises(IndexError):
        es1.get_element_by_index(11)
    e = es1.get_element_by_index(2)
    i, v, d = Metadata.of_string("id"), Metadata.of_integer("val"), Metadata.of_integer("double")
    r = Repository(i)
    r.add_metadata_values([MetadataValue(str(2)), MetadataValue(2), MetadataValue(2+2)])
    r.add_metadata_values([Metadata.from_string(str(2)), Metadata.from_integer(2), Metadata.from_integer(4])
    
def remove_all_elements(self) -> "EagerSet":
    self.elements.clear()
    self.ids.clear()
    return self
def add_element(self, element: Element) -> "EagerSet":
    if not element.get_id() in self.ids:
        self.elements[element.get_id()]=element
        self.ids.add(element.get_id())
    else :
        print(f"{element.get_id()} Already present")

    return self

def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> "EagerSet":
    # Sort the items of the OrderedDict
    sorted_items = sorted(
        self.elements.items(),
        key=cmp_to_key(lambda x, y: comparator.compare(x[1], y[1])),
        reverse=reverse
    )

    # Rebuild as OrderedDict
    self.elements = OrderedDict(sorted_items)
    return self

def get_depth(self) -> int:
    max_depth = 1
    for element in self.elements.values():
        if isinstance(element, EagerSet):
            max_depth = max(max_depth, 1 + element.get_depth())
    return max_depth

def union(self, other: Iterable) -> "LazySet":
    if isinstance(other, EagerSet):
        for element in other.elements.values():
            self.add_element(element)
        return self
    else:
        return LazySet(chain(iter(self), iter(other)))

def intersection(self, other: "EagerSet") -> "EagerSet":
    if not isinstance(other, EagerSet):
        raise NotImplementedError
    common_elements = EagerSet()
    for id, element in self.elements.items():
        if id in other.elements.keys():
            common_elements.add_element(element)
    return common_elements

def difference(self, other: "EagerSet") -> "EagerSet":
    if not isinstance(other, EagerSet):
        raise NotImplementedError
    """Return a new set with elements in this set but not in other"""
    diff_elements = EagerSet()
    for id, element in self.elements.items():
        if id not in other.elements.keys():
            diff_elements.add_element(element)
    return diff_elements

def symmetric_difference(self, other: "EagerSet") -> "EagerSet":
    if not isinstance(other, EagerSet):
        raise NotImplementedError
    """Return a new set with elements in either set but not in both"""
    sym_diff = EagerSet()
    
    # Add elements from this set that are not in other
    for id, element in self.elements.items():
        if id not in other.elements.keys():
            sym_diff.add_element(element)
    
    # Add elements from other set that are not in this
    for id, element in other.elements.items():
        if id not in self.elements.keys():
            sym_diff.add_element(element)
    
    return sym_diff

def is_subset(self, other: "EagerSet") -> bool:
    """Return True if all elements in this set are also in other"""
    for id in self.elements.keys():
        if id not in other.elements.keys():
            return False
    return True

def is_superset(self, other: "EagerSet") -> bool:
    """Return True if all elements in other set are also in this set"""
    return other.is_subset(self)

def is_disjoint(self, other: "EagerSet") -> bool:
    """Return True if this set and other have no elements in common"""
    for id in self.elements.keys():
        if id in other.elements.keys():
            return False
    return True

def is_empty(self) -> bool:
    """Return True if the set is empty"""
    return len(self.elements) == 0



def size(self) -> int:
    return len(self.elements)

def get_element(self, id: str) -> Element:
    if id not in self.elements:
        raise RuntimeError(f"Element with id {id} not found in the set")
    return self.elements[id]

# def set_id(self, set_id: str) -> "EagerSet":
#     self.set_id = set_id
#     return self 

# def get_id(self):
#     if self.set_id is not None:
#         return self.set_id
    
#     set_id = ""
#     for id in self.elements.keys():
#         set_id = set_id + "_" + str(id)
#     return set_id

def flatten_set(self) -> "EagerSet":
    flattened = EagerSet()
    for element in self.get_elements():
        if isinstance(element, EagerSet):
            # Recursively flatten nested Sets
            flattened.union(element.flatten_set())
        else:
            # Add non-Set, non-list elements directly
            flattened.add_element(element)
    return flattened


def get_random_subset(self, subset_size: int, seed: int) -> "EagerSet":
    elements_list = self.get_elements()
    if subset_size > len(elements_list):
        print(
            f"Caution, subset size is larger than the size of the original set, subset size: {subset_size}, current set size: {len(elements_list)}"
        )
        subset_size = len(elements_list)

    random.seed(seed)
    random_indices = random.sample(range(len(elements_list)), subset_size)
    original_array = list(elements_list)

    result = EagerSet()
    for index in random_indices:
        result.add_element(original_array[index])

    return result

def get_elements(self) -> list[Element]:
    return list(self.elements.values())

def clone(self) -> "EagerSet":
    cloned_set = EagerSet()
    for element in self.get_elements():
        cloned_set.add_element(element)
    return cloned_set

def __str__(self) -> str:
    return self.to_string(0)

def to_string(self, level: int = 0) -> str:
    truncate_after = 10
    indent = "    " * level

    result = f"{indent}(size={len(self.elements)})["
    elements_list = self.get_elements()
    element_to_print = min(truncate_after, len(self.elements))

    for i in range(element_to_print):
        next_element = elements_list[i]

        if isinstance(next_element, EagerSet):
            # Recursively call to_string for nested Sets
            result += f"\n{next_element.to_string(level + 4)}"
        else:
            result += str(next_element)

        if i != element_to_print - 1:
            result += ","

    if len(self.elements) > truncate_after:
        result += "...]"
    else:
        result += "]"

    return result
