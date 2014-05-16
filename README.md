pyplate
=======
[![Build Status](https://travis-ci.org/ThatITNinja/pyplate.svg?branch=master)](https://travis-ci.org/ThatITNinja/pyplate)

Pyplate is a binary templating framework written in pure python. It aims to add the functionality of statically typed structs to python easily and in a way that doesn't make you want to claw your eyes out.

Installation
=======
To install pyplate, simply clone the repository and run the setup.py file.

```sh
git clone git@github.com:ThatITNinja/pyplate.git
python setup.py install
```

This is all that is required to install pyplate, however it is suggested that you install pyplate into a python virtualenvironment (using python virtualenv and virtualenv-wrapper).

Usage
=======
Pyplate provides the standard data types (int, char, etc), as well as a template data type. Together, they provide the main functionality of the framework. A very simple example of usage can be seen below:

```python
import pyplate
#pprint is not required, but provides a simple way to visualize results
import pprint
pp = pprint.PrettyPrinter(indent=4)

#define the template
my_template = pyplate.template(name="MyAwesomeTemplate")(
  (pyplate.CHAR)(name="MyChar", repeat=2)
)

#provide data for the template to run on
my_string = pyplate.String("hello")

#extract data from my_string using the template
my_template.extract(my_string)

#view data extracted
pp.pprint(my_template["variables"])

#output of pprint
#{   'MyChar': [   {   'length': 1, 'offset': 0, 'value': 'h'},
#                  {   'length': 1, 'offset': 1, 'value': 'e'}]}



```
