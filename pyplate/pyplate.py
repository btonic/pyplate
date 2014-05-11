import os
import struct

#used to determine endianess
NATIVE_ENDIAN =  "@"
LITTLE_ENDIAN =  "<"
BIG_ENDIAN    =  ">"
NETWORK_ENDIAN = "!"

#used when unpacking during an extraction
_BYTE,   _BYTE_SIZE    = "c", 1 #extracted as a char because python does not have a null byte value
_CHAR,   _CHAR_SIZE    = "c", 1
_SCHAR,  _SCHAR_SIZE   = "b", 1
_UCHAR,  _UCHAR_SIZE   = "B", 1
_BOOL,   _BOOL_SIZE    = "?", 1
_SHORT,  _SHORT_SIZE   = "h", 2
_USHORT, _USHORT_SIZE  = "H", 2
_INT,    _INT_SIZE     = "i", 4
_UINT,   _UINT_SIZE    = "I", 4
_LONG,   _LONG_SIZE    = "l", 4
_ULONG,  _ULONG_SIZE   = "L", 4
_LLONG,  _LLONG_SIZE   = "q", 8
_ULLONG, _ULLONG_SIZE  = "Q", 8
_FLOAT,  _FLOAT_SIZE   = "f", 4
_DOUBLE, _DOUBLE_SIZE  = "d", 8


class template(object):
	def __init__(self, name=""):
		self.name = name
		self.data_objects = []
		self.extracted = {}
	def __call__(self, *args, **kwargs):
		for obj in args:
			self.data_objects.append(obj)
		return self
	def append(self, obj):
		self.data_objects.append(obj)
	def cast(self, f_obj):
		file_length = os.path.getsize(f_obj.name)
		for obj in self.data_objects:
			obj.cast(f_obj, file_length)
	def extract(self, f_obj):
		for index, obj in enumerate(self.data_objects):
			extracted_data = obj.extract(f_obj)
			if extracted_data != None:
				self.extracted[(index, obj.name)] = extracted_data
		return self.extracted

class BaseDatatype(object):
	def __init__(self, name="", repeat=1, endianess=NATIVE_ENDIAN):
		#file IO related
		self.f_offset_start = []
		self.length = 0
		self.endianess = endianess
		self.repeat = repeat
		self.unpack_sequence = ""
		self.casted = False
		#template related
		self.name = name
	def cast(self, f_obj, file_length):
		for cast_num in range(self.repeat):
			self.f_offset_start.append(f_obj.tell())
			if (f_obj.tell() + self.length) > file_length:
				raise TypeError("Unable to cast data type to file object at offset: %s" % str(f_obj.tell()))
			#push the pointer forward to account for it being "read"
			f_obj.seek(f_obj.tell() + self.length)
		self.casted = True
	def extract(self, f_obj):
		extracted_values = []
		if not self.casted:
			self.cast(f_obj, os.path.getsize(f_obj.name))
		for index, start in enumerate(self.f_offset_start):
			f_obj.seek(start)
			type_data = f_obj.read(self.length)
			extracted_values.append(
				dict(
					[
						("%s%s" % (self.name, index), struct.unpack(self.endianess + self.unpack_sequence, type_data)),
				 		("length", self.length),
				 		("offset", f_obj.tell())
				 	]
				)
			)
		return extracted_values

#Utility "types", it's just a simple way to jump around the file
class FSeek(object):
	def __init__(self, offset):
		self.offset = offset
	def cast(self, f_obj, *args, **kwargs):
		f_obj.seek(self.offset)
	def extract(self):
		"""
		Simple compliance for the extraction of objects
		"""
		for x in range(0):
			yield None

class BYTE(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _BYTE_SIZE
		self.unpack_sequence = _BYTE
class CHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _CHAR_SIZE
		self.unpack_sequence = _CHAR
class SCHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _SCHAR_SIZE
		self.unpack_sequence = _SCHAR
class UCHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _UCHAR_SIZE
		self.unpack_sequence = _UCHAR
class BOOL(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _BOOL_SIZE
		self.unpack_sequence = _BOOL
class SHORT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _SHORT_SIZE
		self.unpack_sequence = _SHORT
class USHORT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _USHORT_SIZE
		self.unpack_sequence = _USHORT
class INT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _INT_SIZE
		self.unpack_sequence = _INT
class UINT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _UINT_SIZE
		self.unpack_sequence = _UINT
class LONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _LONG_SIZE
		self.unpack_sequence = _LONG
class ULONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _ULONG_SIZE
		self.unpack_sequence = _ULONG
class LLONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _LLONG_SIZE
		self.unpack_sequence = _LLONG
class ULLONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _ULLONG_SIZE
		self.unpack_sequence = _ULLONG
class FLOAT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _FLOAT_SIZE
		self.unpack_sequence = _FLOAT
class DOUBLE(BaseDatatype):
	def __init__(self, *args, **kwargs):
		BaseDatatype.__init__(self, *args, **kwargs)
		self.length = _DOUBLE_SIZE
		self.unpack_sequence = _DOUBLE