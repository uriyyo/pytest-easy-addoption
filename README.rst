
.. raw:: html
    
    <h1 align="center">Pytest-Easy-Addoption</h2>
    
    <p align="center">
        <a href="https://www.python.org/dev/peps/pep-0008/"><img alt="Code Style" src="https://img.shields.io/badge/Code%20Style-PEP%208-blueviolet"></a>
        <a href="https://github.com/uriyyo/pytest-easy-addoption/blob/develop/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
        <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-brightgreen">
        <a href="https://github.com/uriyyo/pytest-easy-addoption/actions?query=workflow%3ATest"><img alt="Build Status" src="https://github.com/uriyyo/pytest-easy-addoption/workflows/Test/badge.svg?branch=develop"></a>
        <a href="https://codecov.io/gh/uriyyo/pytest-easy-addoption"><img alt="Coverage" src="https://codecov.io/gh/uriyyo/pytest-easy-addoption/branch/develop/graph/badge.svg"></a>
    </p>


``pytest-easy-addoption`` pytest addoption but with power of type annotations and dataclasses.

More documentation `here <https://github.com/uriyyo/pytest-easy-addoption/blob/develop/doc/en.rst>`_.

An quick example of a usage:

.. code-block:: python

    from pytest_easy_addoption import AddOption
    
    class FooBarAddOption(AddOption):
        foo: str
        bar: str = 'BAR'
    
    def pytest_addoption(parser):
        FooBarAddOption.register(parser)

.. code-block:: python

    from .conftest import FooBarAddOption

    def test_example(request):
        print(FooBarAddOption())

::

    $ pytest --foo="FOO"
    ============================= test session starts =============================
    collected 1 items

    test_sample.py FooBarAddOption(foo='FOO', bar='BAR')
    .

    =============================  1 passed in 0.03s  =============================
