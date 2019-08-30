import png
import zlib
import string

def get_decompressed_data(filename):
    img = png.Reader(filename)
    for chunk in img.chunks():
        if chunk[0] == "IDAT":
            print len(chunk[1])
            return zlib.decompress(chunk[1])

data = get_decompressed_data("ninth.png")
len_data = str(len(data))
print '{0}'.format('len_data = :' + len_data)

image_width = 1200
image_height = 848
bytes_per_pixel = 3
bytes_per_filter = 1
data = data[(image_width*bytes_per_pixel + bytes_per_fileter)*image_height:]

print ''.join([x for xin data if x in string.printable])
