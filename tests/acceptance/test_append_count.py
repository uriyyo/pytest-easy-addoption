def test_count_and_append_options(testdir):
    testdir.makeconftest(
        """
        from typing import List
        from easy_addoption import AddOption, Append, Count

        class FooAddOption(AddOption):
            foo: List[str] = Append()
            bar: int = Count()

        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )

    testdir.makepyfile(
        """
        from conftest import FooAddOption

        def test_count():
            assert FooAddOption().bar == 3

        def test_append():
            assert FooAddOption().foo == ['1', '2', '3']
        """
    )

    result = testdir.runpytest_inprocess("--foo=1", "--foo=2", "--foo=3", "--bar", "--bar", "--bar")
    result.assert_outcomes(passed=2)
