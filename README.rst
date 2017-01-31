==========
pypixplore
==========

This tool provides interesting ways to explore python packages, both local and remote. This package is being built as a
Python teaching exercise. This does not diminish our expectations for a full featured  tool. Please use and report any bugs
or missing features.

Download the package to your env with::

    pip install pypixplore


Getting Started
===============
These instructions will get you a copy of this package up and running in your local machine for development and test porpouses. Keep reading if you want to deploy and contribute to the project.

Prerequisites
-------------
First of all, make sure that you have installed:

* Python_ 3.5

.. _Python: http://www.python.org/

* Python Package Index. Usually known as pip_. To install it, open the terminal and type::

      easy_install pip

.. _pip: https://pypi.python.org/pypi/pip


Installing
----------

Let's do a step-by-step installation:

* Fork the project to your account.
* Choose a path in your computer to store the project, go to it.
* Clone the fork that you have just done to this path using the terminal command::

    git clone https://github.com/YOUR-USERNAME/pypiexplorer

* At this point, you should have an exact copy of the latest version of the project on your machine.
* Now you have to install the requirements of this package. It is really easy, open the terminal in the root of the project and type::

      pip install -r requirements.txt
      pip install -r test-requirements.txt

* To make sure that everything is working, run a test with::

      python3 setup.py test

Congratulations! Now you have a version of the project running in your machine. If you want to contribute and help to build this incredible tool, keep reading!

Using
=====

After installation you will get a command-line tool named `ppx`. You can learn how to use it by issuing the following command::

    ppx -h
    usage: skeleton.py [-h] [--version] [-s NAME] [-l] [-r RELEASES] [-i INFO]
                   [-p POPULARITY] [-v] [-vv]

    Copyright (C) 2017 Flavio C. Coelho This program comes with ABSOLUTELY NO
    WARRANTY; This is free software, and you are welcome to redistribute it under
    certain conditions; For details access:
    https://www.gnu.org/licenses/gpl-3.0.en.html Explore Python Package Index

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -s NAME, --status NAME
                            Show Status for a given package.
      -l, --list            List installed packages
      -r RELEASES, --releases RELEASES
                            List package latest release
      -i INFO, --info INFO  Shows package info
      -p POPULARITY, --popularity POPULARITY
                            Return the popularity of a package as the number of
                            recent downloads
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG

for example, if you want to get the dependency tree of a package, you can::

    ppx -t pypixplore
    pypixplore
    ╠═ asciitree
    ╠═ pipdeptree
    ║  ╚═ pip
    ╠═ pip
    ╠═ morfessor
    ╚═ tinydb
    note: only two levels shown.

Contributing
============

To contribute to the project it is better to follow some steps.

* First of all, you should decide on what to contribute to. You can resolve an open issue or create a new one. Whichever the case, ask a repository manager to assign you to the new or existing issue.
* Now, implement the contribution on your version of the code, i.e. your fork.
* After that, build some tests on the tests folder. This is an important step: if you do not build a test to your contribution, it will not be accepted.
* Run those tests typing::

        python3 setup.py test/TEST_FILE.py

. Hint: Make sure that you are running with the last version of the main project. Just type ``git pull fccoelho master`` on terminal.

* Now, you have to write the docstring for your function or class. Follow this template_.

    .. _template: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
* If you are pretty sure that everything is working, do a pull request. Someone is going to read and test. After the reviewer approval, your contribution will be accepted.


Built With
==========

* This project has been set up using PyScaffold 2.5.7. For details and usage information on PyScaffold see http://pyscaffold.readthedocs.org/



