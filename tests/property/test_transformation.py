import hypothesis.strategies as st
from hypothesis import given

from skspatial.transformation import array_to_objects, objects_to_array
from tests.property.strategies import st_point, st_vector


st_list_points = st.lists(st_point(), min_size=1, max_size=10)
st_list_vectors = st.lists(st_vector(), min_size=1, max_size=10)


@given(st.one_of(st_list_points, st_list_vectors))
def test_objects_to_array(list_objects):
    """Test converting between spatial objects and a numpy array."""

    # Obtain the class of a spatial object (Point or Vector).
    class_spatial = list_objects[0].__class__

    array = objects_to_array(list_objects)
    list_objects_new = list(array_to_objects(array, class_spatial))

    assert list_objects_new == list_objects


