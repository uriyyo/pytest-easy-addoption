def test_register(testdir, conftest):
    testdir.makepyfile(
        """
        from conftest import FooAddOption

        def test_manual_register(request):
            assert FooAddOption(request.config).foo == 'foo'
        """
    )

    result = testdir.runpytest_inprocess("--foo=foo")
    result.assert_outcomes(passed=1)
