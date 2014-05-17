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

Within this example, several important features of pyplate are used. The first thing we do after we are done with imports is define our `template`:

```python
#define the template
my_template = pyplate.template(name="MyAwesomeTemplate")(
  (pyplate.CHAR)(name="MyChar", repeat=2)
)
```
The defining of the template allows us to not only create a data structure, but it allows us to extract data using this data structure. This is done by using the `template`'s `cast` and `extract` functions. All that you have to pass is a `pyplate.File`, `pyplate.String`, or `open` file object.

* `cast`: The `cast` function provides a method to apply a data structure to an object without reading any data into the data structure itself. This works by recording offsets within an object based on a data type's size.
 **note**: a call to `cast` is **required** for the `extract` function to work, since it provides the offsets for the extract method to use when reading data into the structures. Cast also reads the variable definitions **in the order they were passed to the template**.

* `extract`: The `extract` function provides a method to both apply a data structure to an object and read data into  data structure.

Looking further inside of the template definition, we can see that there is this line:

```python
...
(pyplate.CHAR)(name="MyChar", repeat=2)
...
```
This line is actually a definition for a variable named "MyChar" that is a list of 2 `pyplate.CHAR`'s. You can have as many variables as you want defined in a `template`. This is just one of many data types provided by pyplate. The full list is:

* `pyplate.BYTE`
* `pyplate.CHAR`
* `pyplate.SCHAR`
* `pyplate.UCHAR`
* `pyplate.BOOL`
* `pyplate.SHORT`
* `pyplate.USHORT`
* `pyplate.INT`
* `pyplate.UINT`
* `pyplate.LONG`
* `pyplate.ULONG`
* `pyplate.LLONG`
* `pyplate.ULLONG`
* `pyplate.FLOAT`
* `pyplate.DOUBLE`

Each of these data types are in fact usable without a template, as they each provide their own `extract` and `cast` methods. The only difference between the template `cast` and the data type `cast` is that you must supply an extra parameter `file_length` to the data type's `cast`. This is to prevent attempting to cast a data type past the end of an object.

If you wish to add more variable definitions to a template after you have defined it, you can simply use the `template.append` function (ex: `template.append((pyplate.INT)(name="myAddedVariable"))`). This will append the data type to the template's definition. You can also pass the data type to the template directly using `my_template((pyplate.INT)(name="myAddedVariable"))` because `template`'s `__call__` method will append the data type to the structure.

Next in the example, a data source is prepared:

```python
#provide data for the template to run on
my_string = pyplate.String("hello")
```
Here, you can see that `my_string` is a `pyplate.String` object. `pyplate.String` allows a `str` type to be operated on by the `template` and data types. However, there are two classes such as this:

* `pyplate.String`: `pyplate.String` turns a regular string (of type `str`) into a `StringIO` object so that it can be used as if it were a file.

* `pyplate.File`: `pyplate.File` takes a path and opening-mode just like you would pass to `open`, and can be used with context managers (ex: `with pyplate.File(...) as my_file:...`).

 **NOTE** You are still able to use `open` and pass it to a template or data type, however this is not suggested as it could cause the template extraction and casting performance to slow.

Following this in the example, the template extracts information from the data source:

```python
#extract data from my_string using the template
my_template.extract(my_string)
```

This extracts information from `my_string` and the template stores it appropriately inside itself for accessing later.

Finally, in the example you can see that the information from the data source is accessed:

```python
#view data extracted
pp.pprint(my_template["variables"])
```

In order to access the information extracted by the template, you must use `template["variables"]` to extract variables, or `template["templates"]` to access templates (template nesting is explained later) within the `template` that was extracted.

Both `template["variables"]` and `template["templates"]` return dictionaries that you can use to access the extracted information. In the example, you can see that the `template["variables"]` has extracted 2 `pyplate.CHAR`'s and assigned them to the name `MyChar`, just like in the template definition:

```python
#output of pprint
#{   'MyChar': [   {   'length': 1, 'offset': 0, 'value': 'h'},
#                  {   'length': 1, 'offset': 1, 'value': 'e'}]}
```

Therefore, you could access the first `pyplate.CHAR` of `MyChar` by using: `my_template["variables"]["MyChar"][0]`. This then gives you a dictionary of the length of the data type, the offset of where the data value was extracted, and the value that was extracted.