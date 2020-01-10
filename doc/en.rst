=====================
Pytest-Easy-Addoption
=====================

General Information
-------------------

Purpose of ``pytest-easy-addoption`` - add ability to easily add addoptins using declarative style.

Example:

.. code-block:: python

    def pytest_addoption(parser):
        parser.addoption(
            "--foo", action="store_true", required=True
        )
        parser.addopion(
            "--bar", action="store", default="Bar"
        )

Can be rewrite to:

.. code-block:: python

    from pytest_easy_addoption import AddOption

    class FooBarAddOption(AddOption):
        foo: bool
        bar: str = "BAR"

    def pytest_addoption(parser):
        FooBarAddOption.register(parser)

Then addoptions can be accessed as class instance attributes:

.. code-block:: python

    addoption = FooBarAddOption()
    addoption.foo
    addoption.bar