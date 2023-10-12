from pandos.cli import CLI


def test_hello():
    cli = CLI()
    assert cli.hello(name="test") == "Hello, test!"
