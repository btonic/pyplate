import os
import struct
import StringIO

#used to determine endianess
NATIVE_ENDIAN =  "@"
LITTLE_ENDIAN =  "<"
BIG_ENDIAN    =  ">"
NETWORK_ENDIAN = "!"

#used when unpacking during an extraction
_BYTE,   _BYTE_SIZE    = "c", struct.calcsize("c") #extracted as a char because python does not have a null byte value
_CHAR,   _CHAR_SIZE    = "c", struct.calcsize("c")
_SCHAR,  _SCHAR_SIZE   = "b", struct.calcsize("b")
_UCHAR,  _UCHAR_SIZE   = "B", struct.calcsize("B")
_BOOL,   _BOOL_SIZE    = "?", struct.calcsize("?")
_SHORT,  _SHORT_SIZE   = "h", struct.calcsize("h")
_USHORT, _USHORT_SIZE  = "H", struct.calcsize("H")
_INT,    _INT_SIZE     = "i", struct.calcsize("i")
_UINT,   _UINT_SIZE    = "I", struct.calcsize("I")
_LONG,   _LONG_SIZE    = "l", struct.calcsize("l")
_ULONG,  _ULONG_SIZE   = "L", struct.calcsize("L")
_LLONG,  _LLONG_SIZE   = "q", struct.calcsize("q")
_ULLONG, _ULLONG_SIZE  = "Q", struct.calcsize("Q")
_FLOAT,  _FLOAT_SIZE   = "f", struct.calcsize("f")
_DOUBLE, _DOUBLE_SIZE  = "d", struct.calcsize("d")


class template(object):
	def __init__(self, name=""):
		self.name = name
		self.data_objects = []
		self.templates = {}
		self.data_values = {}
	def __call__(self, *args, **kwargs):
		for obj in args:
			self.data_objects.append(obj)
		return self
	def __getitem__(self, item):
		if item == "templates":
			return self.templates
		elif item == "variables":
			return self.data_values
	def append(self, obj):
		self.data_objects.append(obj)
	def cast(self, f_obj, *args, **kwargs):
		for obj in self.data_objects:
			if isinstance(f_obj, File) or isinstance(f_obj, String):
				obj.cast(f_obj, f_obj.len)
			else:
				self.cast(f_obj, os.path.getsize(f_obj.name))
	def extract(self, f_obj):
		for index, obj in enumerate(self.data_objects):
			extracted_data = obj.extract(f_obj)
			if extracted_data != None:
				if isinstance(extracted_data[0], template):
					self.templates[obj.name] = extracted_data[0]
				elif isinstance(extracted_data[0], BaseDatatype):
					self.data_values[extracted_data[0].name] = extracted_data[1]
		return [self]

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
				raise TypeError("Unable to cast data type %s:%s to file object at offset: %s" % (self.__class__.__name__, self.name, str(f_obj.tell())))
			#push the pointer forward to account for it being "read"
			f_obj.seek(f_obj.tell() + self.length)
		self.casted = True
	def extract(self, f_obj):
		extracted_values = []
		if not self.casted:
			if isinstance(f_obj,String) or isinstance(f_obj, File):
				#the helper objects are being used. Use the len attribute.
				self.cast(f_obj, f_obj.len)
			else:
				#assume normal open file
				self.cast(f_obj, os.path.getsize(f_obj.name))
		for index, start in enumerate(self.f_offset_start):
			f_obj.seek(start)
			type_data = f_obj.read(self.length)
			extracted_values.append(
				dict(
					[
						("value", struct.unpack(self.endianess + self.unpack_sequence, type_data)[0]),
				 		("length", self.length),
				 		("offset", f_obj.tell())
				 	]
				)
			)
		return [self, extracted_values]


#ease of use functions
class String(StringIO.StringIO):
	def __str__(self):
		return str(self.buf)
#this is required for use with the templates because the .len attribute is required.
class File(file):
	def __init__(self, *args, **kwargs):
		file.__init__(self, *args, **kwargs)
		self.len = os.path.getsize(self.name)


#Utility "types", it's just a simple way to jump around the file
class FSeek(object):
	def __init__(self, offset):
		self.offset = offset
		self.name = None
		self.casted = False
	def cast(self, f_obj, *args, **kwargs):
		f_obj.seek(self.offset)
		self.casted = True
	def extract(self, f_obj):
		"""
		Simple compliance for the extraction of objects
		"""
		if not self.casted:
			self.cast(f_obj)
		return None

#Normal types
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