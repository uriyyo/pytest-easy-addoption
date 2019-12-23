from pytest import fixture

pytest_plugins = ["pytester"]


@fixture
def conftest(testdir):
    return testdir.makeconftest(
        """
        from pytest_easy_addoption import AddOption

        class FooAddOption(AddOption):
            foo: str

        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )
