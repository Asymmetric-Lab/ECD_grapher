import setuptools


# Chosen from http://www.python.org/pypi?:action=list_classifiers
classifiers = """Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering :: Chemistry
Topic :: Software Development :: Libraries :: Python Modules"""


def setup_grapher():

    doclines = __doc__.split("\n")
    with open('README.md') as f:
        readme = f.read()
    
    setuptools.setup(
        name="ECD Grapher",
        version="1.0.0",
        url="https://github.com/Asymmetric-Lab/ECD_grapher",
        author="Asymmetric Lab development team",
        author_email="andrea.pellegrini15@unibo.it",
        maintainer="Asymmetric Lab team",
        maintainer_email="andrea.pellegrini15@unibo.it",
        license="MIT License",
        description=__doc__,
        long_description=readme,
        classifiers=classifiers.split("\n"),
        platforms=["Any."],
        packages=setuptools.find_packages(exclude=['*test*']),
        install_requires=[
            "packaging>=19.0",
            "matplotlib"
            "numpy",
            "scipy",
        ],

    )


if __name__ == '__main__':
    setup_grapher()
