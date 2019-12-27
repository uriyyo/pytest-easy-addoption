from pathlib import Path
from subprocess import PIPE, run


def test_mypy(testdir):
    f = testdir.makepyfile(
        script="""
    from typing import ClassVar

    from easy_addoption import AddOption, Option

    class FooAddOption(AddOption):
        bar: int
        foo: str = Option('FOO')
        bar_foo: int = Option(10)
    
        foo_bar: ClassVar[bytes]
    
        def my_method(self) -> None:
            pass
    
        class MyClass:
            pass

    def function(foo: str, bar: int, foo_bar: bytes) -> None:
        pass

    def main() -> None:
        add_options = FooAddOption()
    
        function(add_options.foo, add_options.bar, add_options.foo_bar)

        a: int = add_options.bar
        b: str = add_options.foo
        c: int = add_options.bar_foo
    """
    )

    cwd = str(Path(__file__).parent.parent.parent)  # mypy should be run in project root directory
    result = run(f"mypy {f}", shell=True, cwd=cwd, stdout=PIPE)
    assert not result.returncode, result.stdout
