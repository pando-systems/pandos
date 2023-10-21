from pandos.utils.pyobj_serializers import PyObjSerializationFrameworkEnum


def test_pyobj_serialization_framework_enum_with_payload_pickle():
    import pickle

    payload = {"hello": "world"}
    payload_serialized = pickle.dumps(payload)

    payload_deserialized = PyObjSerializationFrameworkEnum.PICKLE.loads(payload_serialized)
    assert payload == payload_deserialized


def test_pyobj_serialization_framework_enum_with_payload_dill():
    import dill

    payload = {"hello": "world"}
    payload_serialized = dill.dumps(payload)

    payload_deserialized = PyObjSerializationFrameworkEnum.PICKLE.loads(payload_serialized)
    assert payload == payload_deserialized


def test_pyobj_serialization_framework_enum_with_function_dill():
    import dill

    output = "Hello, world!"
    function_serialized = dill.dumps(lambda: output)

    function_deserialized = PyObjSerializationFrameworkEnum.DILL.loads(function_serialized)
    assert function_deserialized() == output
