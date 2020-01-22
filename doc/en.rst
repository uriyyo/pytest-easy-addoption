=====================
Pytest-Easy-Addoption
=====================

General Information
-------------------

Purpose of ``pytest-easy-addoption`` - add ability to easily add addoptins using class variables.

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

    from easy_addoption import AddOption

    class FooBarAddOption(AddOption):
        foo: bool
        bar: str = "BAR"

    def pytest_addoption(parser):
        FooBarAddOption.register(parser)

Then addoptions can be accessed as instance attributes:

.. code-block:: python

    addoption = FooBarAddOption()
    addoption.foo
    addoption.bar



API Reference
-------------

Packages
##########
1. easy_addoption - package with core functionality.
2. _pytest_easy_addoption - *pytest* plugin.
3. _mypy_easy_addoption_plugin - *mypy* plugin.

AddOption
#########

To use class as addoption you must inherit from ``easy_addoption.AddOption`` class:

.. code-block:: python

    from easy_addoptoin import AddOption

    class FooBarAddOption(AddOption):
        ...

There are class variable ``prefix`` used to set default prefix which will be concatenated to option name.
By default in equals to ``None``.

When class inherit from ``AddOption`` all class variables will be treated as addoptions.
Basically, every ``AddOption`` class will be converted into ``dataclass`` by ``easy_addoptoin.addoption.AddOptionMeta`` metaclass.

To register addoption class you can use two options:

1. Use ``AddOption.register`` method and pass instance of pytest ``Parser`` class.

.. code-block:: python

    def pytest_addoption(parser):
        FooBarAddOption.register(parser)

2. Add ``pytest-easy-addoption`` entry point to *setup* file.     Using this option addoption will be automatically registered using ``pytest_addoption`` hook.


.. code-block:: python

    setup(
        ...
        entry_points={
            "pytest11": [
                "foo-bar-addoption = my_plugin:FooBarAddOption"
            ]
        }
    )

When you create instance of ``AddOption`` class config argument can be omit.

.. code-block:: python

    class FooBarAddOption(AddOption):
        foo: int

    ...

    foo_bar = FooBarAddOption()
    print(foo_bar.foo * 10)

Option
######

Option class used to declared option it roughly equals to ``Parser.addoption`` call.
All arguments passed to Option will be redirected to addoption call.

.. code-block:: python

    class FooBarAddOption:
        foo: int = Option(10)


.. code-block:: python

    def pytest_addoption(parser):
        parser.addoption(
            '--foo',
            type=int,
            default=10,
        )

Option name convert rules

1. In case when no *name* provided class variable name fill be used.

.. code-block:: python

    class FooBarAddOption(AddOption):
        foo: int


    class FooBarAddOption(AddOption):
        foo: int = Option(name='foo')

2. In case when *name* provided it will override class variable name.

.. code-block:: python

    class FooBarAddOption(AddOption):
        foo: int = Option(name='bar')  # bar name will be used

3. In case when *prefix* class variable set, it will be concatenated with option *name*.

.. code-block:: python

    class FooBarAddOption(AddOption):
        prefix: str = 'bar'

        foo: int


    class FooBarAddOption(AddOption):
        foo: int = Option(name='bar_foo')

Examples
########

In case when no default value provided, option will be required.

.. code-block:: python

    class FooBarAddOption(AddOption):
        foo: int


    class FooBarAddOption(AddOption):
        foo: int = Option(required=True)

In case when class variable assigned to not ``Option`` object, this object will be used as default value.

.. code-block:: python

    class FooBarAddOption(AddOption):
        foo: int = 10


    class FooBarAddOption(AddOption):
        foo: int = Option(10, required=False)

MyPy
----

There are *easy-addoption* plugin for mypy.
In order to enable it add ``_mypy_easy_addoption_plugin`` to list of plugin at *mypy.ini*.

.. code-block:: cfg

    plugins = _mypy_easy_addoption_plugin
