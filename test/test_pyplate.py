import pyplate
import unittest
import os
from struct import unpack, calcsize


class TestPyplate(unittest.TestCase):
	def setUp(self):
		self.template_name = "template"
		self.data_name     = "test"
		self.data_key      = "test[0]"
		numeric          = "1"
		alphanumeric     = "a"
		self.test_byte   = pyplate.String(numeric)
		self.test_char   = pyplate.String(alphanumeric)
		self.test_bool   = pyplate.String(numeric)
		self.test_short  = pyplate.String(numeric * calcsize("h"))
		self.test_int    = pyplate.String(numeric * calcsize("i"))
		self.test_long   = pyplate.String(numeric * calcsize("l"))
		self.test_llong  = pyplate.String(numeric * calcsize("q"))
		self.test_float  = pyplate.String(numeric * calcsize("f"))
		self.test_double = pyplate.String(numeric * calcsize("d"))
		self.test_file_path = "test/data/data_file.txt"
	def test_BYTE_extract(self):
		t_byte = (pyplate.BYTE)(name=self.data_name)
		extracted_values = t_byte.extract(self.test_byte)[1]
		self.assertTrue(
			unpack("c", str(self.test_byte))[0] == extracted_values["value"]
		)
	def test_CHAR_extract(self):
		t_char = (pyplate.CHAR)(name=self.data_name)
		extracted_values = t_char.extract(self.test_char)[1]
		self.assertTrue(
			unpack("c", str(self.test_char))[0] == extracted_values["value"]
		)
	def test_CHAR_STRING_extract(self):
		t_char = (pyplate.CHAR)(name=self.data_name, repeat = 5, extract_as_string = True)
		extracted_values = t_char.extract(pyplate.String(str(self.test_char) * 5))[1]
		self.assertTrue(
			unpack("5s", str(self.test_char) * 5)[0] == extracted_values["value"]
		)
	def test_BOOL_extract(self):
		t_bool = (pyplate.BOOL)(name=self.data_name)
		extracted_values = t_bool.extract(self.test_bool)[1]
		self.assertTrue(
			unpack("?", str(self.test_bool))[0] == extracted_values["value"]
		)
	def test_SHORT_extract(self):
		t_short = (pyplate.SHORT)(name=self.data_name)
		extracted_values = t_short.extract(self.test_short)[1]
		self.assertTrue(
			unpack("h", str(self.test_short))[0] == extracted_values["value"]
		)
	def test_INT_extract(self):
		t_int = (pyplate.INT)(name=self.data_name)
		extracted_values = t_int.extract(self.test_int)[1]
		self.assertTrue(
			unpack("i", str(self.test_int))[0] == extracted_values["value"]
		)
	def test_LONG_extract(self):
		t_long = (pyplate.LONG)(name=self.data_name)
		extracted_values = t_long.extract(self.test_long)[1]
		self.assertTrue(
			unpack("l", str(self.test_long))[0] == extracted_values["value"]
		)
	def test_LLONG_extract(self):
		t_llong = (pyplate.LLONG)(name=self.data_name)
		extracted_values = t_llong.extract(self.test_llong)[1]
		self.assertTrue(
			unpack("q", str(self.test_llong))[0] == extracted_values["value"]
		)
	def test_FLOAT_extract(self):
		t_float = (pyplate.FLOAT)(name=self.data_name)
		extracted_values = t_float.extract(self.test_float)[1]
		self.assertTrue(
			unpack("f", str(self.test_float))[0] == extracted_values["value"]
		)
	def test_DOUBLE_extract(self):
		t_double = (pyplate.DOUBLE)(name=self.data_name)
		extracted_values = t_double.extract(self.test_double)[1]
		self.assertTrue(
			unpack("d", str(self.test_double))[0] == extracted_values["value"]
		)
	def test_template_cast(self):
		t_template = pyplate.template(name=self.template_name)(
			(pyplate.CHAR)(name=self.data_name)
		)
		t_template.cast(self.test_char)
		self.assertTrue(
			t_template.data_objects[0].casted
		)
	def test_template_extract(self):
		t_template = pyplate.template(name=self.template_name)(
			(pyplate.CHAR)(name=self.data_name),
			pyplate.template(name="test2")(
				(pyplate.INT)(name="datatest2")
			)
		)
		compiled_strings = pyplate.String(str(self.test_char) + str(self.test_int))
		t_template.extract(compiled_strings)
		self.assertTrue(
			t_template["templates"]["test2"]["variables"]["datatest2"]["length"] == calcsize("i"),
			t_template["variables"][self.data_name]["length"] == 1
		)
	def test_template_fseek(self):
		t_template = pyplate.template(name=self.template_name)(
			(pyplate.FSeek)(1),
			(pyplate.CHAR)(name=self.data_name)
		)
		compiled_strings = pyplate.String(str(self.test_char) + str(self.test_char))
		t_template.extract(compiled_strings)
		self.assertTrue(
			t_template["variables"][self.data_name]["offset"] == 1
		)
	def test_extract_as_string(self):
		t_char_as_string = (pyplate.CHAR)(name=self.data_name, repeat=2, extract_as_string=True)
		compiled_strings = pyplate.String(str(self.test_char) + str(self.test_char))
		extracted_values = t_char_as_string.extract(compiled_strings)[1]
		self.assertTrue(
			unpack("2s", str(compiled_strings))[0] == extracted_values["value"]
		)
	def test_file_extract(self):
		with pyplate.File(self.test_file_path, 'rb') as t_file:
			t_template = pyplate.template(name=self.template_name)(
				(pyplate.CHAR)(name=self.data_name, repeat=4, extract_as_string = True),
				(pyplate.SHORT)(name=self.data_name+"short")
			)
			t_template.extract(t_file)
			self.assertTrue(
				t_template["variables"][self.data_name]["value"] != None,
				t_template["variables"][self.data_name+"short"]["value"] != None
			)

if __name__ == '__main__':
	unittest.main()