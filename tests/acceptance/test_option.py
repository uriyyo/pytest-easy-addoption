from pytest import fixture


@fixture(autouse=True)
def test_file(testdir):
    testdir.makepyfile(
        """
        from conftest import FooAddOption

        def test_manual_register(request):
            assert FooAddOption(request.config).foo == 'foo'
        """
    )


def test_explicit_option(testdir):
    testdir.makeconftest(
        """
        from pytest_easy_addoption import AddOption, Option

        class FooAddOption(AddOption):
            foo: str = Option('foo')

        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )

    result = testdir.runpytest_inprocess("--foo=foo")
    result.assert_outcomes(passed=1)


def test_implicit_option(testdir):
    testdir.makeconftest(
        """
        from pytest_easy_addoption import AddOption

        class FooAddOption(AddOption):
            foo: str

        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )

    result = testdir.runpytest_inprocess("--foo=foo")
    result.assert_outcomes(passed=1)


def test_option_default_value_missed(testdir):
    testdir.makeconftest(
        """
        from pytest_easy_addoption import AddOption

        class FooAddOption(AddOption):
            foo: str

        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )

    result = testdir.runpytest_inprocess()
    result.stderr.fnmatch_lines("*the following arguments are required: --foo")
