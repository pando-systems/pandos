from pandos.utils.pyobj_serializers import PyObjSerializationFrameworkEnum


def test_pyobj_serialization_framework_enum_with_payload_pickle():
    import pickle
    import codecs

    payload = {"hello": "world"}
    payload_serialized: str = PyObjSerializationFrameworkEnum.PICKLE.dumps(payload)

    payload_deserialized = PyObjSerializationFrameworkEnum.PICKLE.loads(payload_serialized)
    assert payload == payload_deserialized


def test_pyobj_serialization_framework_enum_with_payload_dill():
    import dill

    payload = {"hello": "world"}
    payload_serialized: str = PyObjSerializationFrameworkEnum.DILL.dumps(payload)

    payload_deserialized = PyObjSerializationFrameworkEnum.DILL.loads(payload_serialized)
    assert payload == payload_deserialized


def test_pyobj_serialization_framework_enum_with_function_dill():
    import dill

    output = "Hello, world!"
    function_serialized: str = PyObjSerializationFrameworkEnum.DILL.dumps(lambda: output)

    function_deserialized = PyObjSerializationFrameworkEnum.DILL.loads(function_serialized)
    assert function_deserialized() == output
