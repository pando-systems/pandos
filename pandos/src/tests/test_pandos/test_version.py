from pandos.version import version


def test_version_value():
    components = version.value.split(".")
    assert len(components) == 3
    for component in components:
        assert component.isdigit()
