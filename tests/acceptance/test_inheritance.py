def test_inheritance(testdir):
    testdir.makeconftest(
        """
        from easy_addoption import AddOption

        class BarAddOption(AddOption):
            bar: str
        
        class FooAddOption(BarAddOption):
            foo: str
        
        def pytest_addoption(parser):
            FooAddOption.register(parser)
        """
    )

    testdir.makepyfile(
        """
        from conftest import FooAddOption

        def test_manual_register(request):
            options = FooAddOption(request.config)

            assert options.foo == 'foo'
            assert options.bar == 'bar'
        """
    )

    result = testdir.runpytest_inprocess("--foo=foo", "--bar=bar")
    result.assert_outcomes(passed=1)
