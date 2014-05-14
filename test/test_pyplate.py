import pyplate
import unittest
import os
class TestPyplate(unittest.TestCase):
	def setUp(self):
		numeric        = "1"
		alphanumeric   = "a"
		self.data_name = "test"
		self.data_key  = "test[1]"
		self.test_byte   = pyplate.String(numeric)
		self.test_char   = pyplate.String(alphanumeric)
		self.test_bool   = pyplate.String(numeric)
		self.test_short  = pyplate.String(numeric * 2)
		self.test_int    = pyplate.String(numeric * 4)
		self.test_long   = pyplate.String(numeric * 4)
		self.test_llong  = pyplate.String(numeric * 8)
		self.test_float  = pyplate.String(numeric * 4)
		self.test_double = pyplate.String(numeric * 8)
		self.test_file   = pyplate.File("test/data/data_file.txt", 'rb')
	def tearDown(self):
		self.test_file.close()
	def test_BYTE_extract(self):
		t_byte = (pyplate.BYTE)(name=self.data_name)
		extracted_value = t_byte.extract(self.test_byte)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_CHAR_extract(self):
		t_char = (pyplate.CHAR)(name=self.data_name)
		extracted_value = t_char.extract(self.test_char)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_BOOL_extract(self):
		t_bool = (pyplate.BOOL)(name=self.data_name)
		extracted_value = t_bool.extract(self.test_bool)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_SHORT_extract(self):
		t_short = (pyplate.SHORT)(name=self.data_name)
		extracted_value = t_short.extract(self.test_short)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_INT_extract(self):
		t_int = (pyplate.INT)(name=self.data_name)
		extracted_value = t_int.extract(self.test_int)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_LONG_extract(self):
		t_long = (pyplate.BOOL)(name=self.data_name)
		extracted_value = t_long.extract(self.test_long)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_LLONG_extract(self):
		t_llong = (pyplate.LLONG)(name=self.data_name)
		extracted_value = t_llong.extract(self.test_llong)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_FLOAT_extract(self):
		t_float = (pyplate.FLOAT)(name=self.data_name)
		extracted_value = t_float.extract(self.test_float)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)
	def test_DOUBLE_extract(self):
		t_double = (pyplate.DOUBLE)(name=self.data_name)
		extracted_value = t_double.extract(self.test_double)
		self.assertTrue(
			len(extracted_value[0][self.data_key]) == 1
		)

if __name__ == '__main__':
	unittest.main()