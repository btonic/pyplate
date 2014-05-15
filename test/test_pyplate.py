import pyplate
import unittest
import os
from struct import unpack



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
		self.test_short  = pyplate.String(numeric * 2)
		self.test_int    = pyplate.String(numeric * 4)
		self.test_long   = pyplate.String(numeric * 8)
		self.test_llong  = pyplate.String(numeric * 8)
		self.test_float  = pyplate.String(numeric * 4)
		self.test_double = pyplate.String(numeric * 8)
		self.test_file   = pyplate.File("test/data/data_file.txt", 'rb')
	def tearDown(self):
		self.test_file.close()
	def test_BYTE_extract(self):
		t_byte = (pyplate.BYTE)(name=self.data_name)
		extracted_value = t_byte.extract(self.test_byte)[0][self.data_key]
		self.assertTrue(
			unpack("c", str(self.test_byte)) == extracted_value
		)
	def test_CHAR_extract(self):
		t_char = (pyplate.CHAR)(name=self.data_name)
		extracted_value = t_char.extract(self.test_char)[0][self.data_key]
		self.assertTrue(
			unpack("c", str(self.test_char)) == extracted_value
		)
	def test_BOOL_extract(self):
		t_bool = (pyplate.BOOL)(name=self.data_name)
		extracted_value = t_bool.extract(self.test_bool)[0][self.data_key]
		self.assertTrue(
			unpack("?", str(self.test_bool)) == extracted_value
		)
	def test_SHORT_extract(self):
		t_short = (pyplate.SHORT)(name=self.data_name)
		extracted_value = t_short.extract(self.test_short)[0][self.data_key]
		self.assertTrue(
			unpack("h", str(self.test_short)) == extracted_value
		)
	def test_INT_extract(self):
		t_int = (pyplate.INT)(name=self.data_name)
		extracted_value = t_int.extract(self.test_int)[0][self.data_key]
		self.assertTrue(
			unpack("i", str(self.test_int)) == extracted_value
		)
	def test_LONG_extract(self):
		t_long = (pyplate.LONG)(name=self.data_name)
		extracted_value = t_long.extract(self.test_long)[0][self.data_key]
		self.assertTrue(
			unpack("l", str(self.test_long)) == extracted_value
		)
	def test_LLONG_extract(self):
		t_llong = (pyplate.LLONG)(name=self.data_name)
		extracted_value = t_llong.extract(self.test_llong)[0][self.data_key]
		self.assertTrue(
			unpack("q", str(self.test_llong)) == extracted_value
		)
	def test_FLOAT_extract(self):
		t_float = (pyplate.FLOAT)(name=self.data_name)
		extracted_value = t_float.extract(self.test_float)[0][self.data_key]
		self.assertTrue(
			unpack("f", str(self.test_float)) == extracted_value
		)
	def test_DOUBLE_extract(self):
		t_double = (pyplate.DOUBLE)(name=self.data_name)
		extracted_value = t_double.extract(self.test_double)[0][self.data_key]
		self.assertTrue(
			unpack("d", str(self.test_double)) == extracted_value
		)
	def test_template_extract(self):
		t_template = pyplate.template(name=self.template_name)(
			(pyplate.CHAR)(name=self.data_name)
		)
		extracted_value = t_template.extract(self.test_char)[self.template_name][(0, self.data_name)][0][self.data_key]
		self.assertTrue(
			len(extracted_value) > 0
		)
		

if __name__ == '__main__':
	unittest.main()