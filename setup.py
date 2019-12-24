from setuptools import (
    setup,
    find_packages,
)
from pathlib import Path

__version__ = "0.1.0"

README: Path = Path(__file__).parent / "README.md"

test_requirements = [
    "pytest-mock",
    "pytest-cov",
    "pre-commit",
]

lint_requirements = [
    "mypy",
    "isort",
    "flake8",
    "flake8-isort",
    "flake8-docstrings",
    "flake8-bugbear",
]

setup(
    name="pytest-easy-addoption",
    version="0.1.0",
    python_requires=">=3.6",
    author="Yurii Karabas",
    author_email="1998uriyyo@gmail.com",
    url="https://github.com/uriyyo/instapi",
    description="pytest-easy-addoption: Easy way to work with pytest addoption",
    long_description=README.read_text(),
    license="MIT",
    packages=find_packages(exclude=("tests*",)),
    install_requires=["dataclasses>=0.6", "pytest>=5.0"],
    extras_require={
        "test": test_requirements,
        "lint": lint_requirements,
        "dev": [*test_requirements, *lint_requirements, "pre-commit"],
    },
    classifiers=[
        "License :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
