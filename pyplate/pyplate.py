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
	def __init__(self, f_name, name=""):
		self.f_name = f_name
		self.name = name
		self.data_objects = []
	def __call__(self, *args, **kwargs):
		for obj in args:
			self.data_objects.append(obj)
	def cast(self, f_obj):
		file_length = os.path.getsize(f_obj.name)
		for obj in self.data_objects:
			obj.cast(f_obj, file_length)

class BaseDatatype(object):
	def __init__(self, name="", repeat=1, cast_start_offset = None, endianess=NATIVE_ENDIAN):
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
			f_obj.read(self.length)
		self.casted = True
	def extract(self, f_obj):
		if not self.casted:
			self.cast(f_obj, os.path.getsize(f_obj.name))
		for start in self.f_offset_start:
			f_obj.seek(start)
			type_data = f_obj.read(self.length)
			yield struct.unpack(self.endianess + self.unpack_sequence, type_data)

class BYTE(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(BYTE, self).__init__(*args, **kwargs)
		self.length = _BYTE_SIZE
		self.unpack_sequence = _BYTE * self.repeat
class CHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(UINT, self).__init__(*args, **kwargs)
		self.length = _CHAR_SIZE
		self.unpack_sequence = _CHAR * self.repeat
class SCHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(SCHAR, self).__init__(*args, **kwargs)
		self.length = _SCHAR_SIZE
		self.unpack_sequence = _SCHAR * self.repeat
class UCHAR(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(UCHAR, self).__init__(*args, **kwargs)
		self.length = _UCHAR_SIZE
		self.unpack_sequence = _UCHAR * self.repeat
class BOOL(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(BOOL, self).__init__(*args, **kwargs)
		self.length = _BOOL_SIZE
		self.unpack_sequence = _BOOL * self.repeat
class SHORT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(SHORT, self).__init__(*args, **kwargs)
		self.length = _SHORT_SIZE
		self.unpack_sequence = _SHORT * self.repeat
class USHORT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(USHORT, self).__init__(*args, **kwargs)
		self.length = _USHORT_SIZE
		self.unpack_sequence = _USHORT * self.repeat
class INT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(INT, self).__init__(*args, **kwargs)
		self.length = _INT_SIZE
		self.unpack_sequence = _INT * self.repeat
class UINT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(UINT, self).__init__(*args, **kwargs)
		self.length = _UINT_SIZE
		self.unpack_sequence = _UINT * self.repeat
class LONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(LONG, self).__init__(*args, **kwargs)
		self.length = _LONG_SIZE
		self.unpack_sequence = _LONG * self.repeat
class ULONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(ULONG, self).__init__(*args, **kwargs)
		self.length = _ULONG_SIZE
		self.unpack_sequence = _ULONG * self.repeat
class LLONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(LLONG, self).__init__(*args, **kwargs)
		self.length = _LLONG_SIZE
		self.unpack_sequence = _LLONG * self.repeat
class ULLONG(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(ULLONG, self).__init__(*args, **kwargs)
		self.length = _ULLONG_SIZE
		self.unpack_sequence = _ULLONG * self.repeat
class FLOAT(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(FLOAT, self).__init__(*args, **kwargs)
		self.length = _FLOAT_SIZE
		self.unpack_sequence = _FLOAT * self.repeat
class DOUBLE(BaseDatatype):
	def __init__(self, *args, **kwargs):
		super(DOUBLE, self).__init__(*args, **kwargs)
		self.length = _DOUBLE_SIZE
		self.unpack_sequence = _DOUBLE * self.repeat