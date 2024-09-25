import struct
f = open("timeblender","wb")
f.write(struct.pack("f",24.0))
f.write(struct.pack("I",0))
f.close()