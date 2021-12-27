import codecs
import os
import platform
import re
import sys

from setuptools import find_packages, setup


###############################################################################

NAME = "attrs"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "wordclock", "__init__.py")
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = [
    "adafruit-circuitpython-dotstar==2.0.0",
    "adafruit-circuitpython-led-animation==2.4.2",
    "gpiozero==1.5.1",
    "rich==9.0.0"
]

EXTRAS_REQUIRE = {
    # "docs": ["furo", "sphinx", "zope.interface", "sphinx-notfound-page"],
    "tests": [
        "coverage",
        "flake8",
        "pytest"
    ],
}
if (
    sys.version_info[:2] >= (3, 6)
    and platform.python_implementation() != "PyPy"
):
    EXTRAS_REQUIRE["tests"].extend(["mypy", "pytest-mypy-plugins"])

EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"]
)

###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")


if __name__ == "__main__":
    setup(
        name='wordclock',
        description='test',
        license='MIT',
        url='http://test.com',
        # project_urls=PROJECT_URLS,
        version=VERSION,
        author="Joe Meissler",
        author_email="joe.meissler@gmail.com",
        maintainer="Joe Meissler",
        # maintainer_email=find_meta("email"),
        keywords=[],
        long_description='',
        long_description_content_type="text/x-rst",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=3.6",
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        include_package_data=True,
        options={"bdist_wheel": {"universal": "1"}},
    )
