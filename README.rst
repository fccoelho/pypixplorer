==========
pypixplore
==========

This tool provides interesting ways to explore python packages, both local and remote. This package is being built as a
Python teaching exercise. This does not diminish our expectations for a full featured  tool. Please use and report any bugs
or missing features.

Download the package to your env with::
    
    pip install pypixplorer


Getting Started
===========
These instructions will get you a copy of this package up and running in your local machine for development and test porpouses. Keep reading if you want to deploy and contribute to the project.

Prerequisites
-------------
First of all, make sure that you have already installed:

* Python_ 3.5
.. _Python: http://www.python.org/ 

* Python Package Index. Usually know as pip_. To install it, open the terminal and type::

      easy_install pip
.. _pip: https://pypi.python.org/pypi/pip

  


Installing
-----------

Let's do a step-by-step installation:

* Fork the project to your account.
* Choose a path in your computer to store the project, go to it.
* Clone the the fork that you have just done to this path using the terminal command::

    git clone https://github.com/YOUR-USERNAME/pypiexplorer

* At this point, you should have an exact copy of the lastest version of the project on your machine.
* Now, you have to install the requirements of this package. It is really easy, open the terminal in the root of the project and type::

      pip install -r requirements.txt
      pip install -r test-requirements.txt
* To make sure that everything is working, run a test with::

      python3 setup.py test
      
Congratulations! Now you have a version of the project running in your machine. If you want to contribute and help to build this incredible tool, keep reading!

Contributing
===========

To contribute to the project it is better to follow some steps.

* First, you should decide on what to contribute to, it can be an opened issue or a issue that you can create. If the former is the case, make sure to assign yourself to the task. If it is the latter, open an issue and put yourself as a responsible.
* Now, implement the contribution on your version of the code, i.e. your fork.
* After that, build some tests on the tests folder. This is an important step, if you do not build a test to your contribution, it will not be accepted.
* Run those tests typing::

        python3 setup.py test/TEST_FILE.py
        
. Hint: Make sure that you are running with the last version of the main project. Just type ``git pull fccoelho master`` on terminal.

* Now, you have to write the docstring for your function or class. Follow this template_.

    .. _template: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
* If you are pretty sure that everything is working, do a pull request. Someone is going to read and test. After the reviwer approval, your contribution will be accepted.


Built With
===========

* This project has been set up using PyScaffold 2.5.7. For details and usage information on PyScaffold see http://pyscaffold.readthedocs.org/.

Versioning
===========

Authors
===========

License
===========

Acknowledgments
===========



