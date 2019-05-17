import OpenImageIO as oiio
import array

def genArray4(w,h,bpp=16):
    valMax = 2**bpp - 1
    s=1
    yStep = float(valMax)/(h-1)
    for j in range(h):
        for i in range(w):
            yield 0
            yield valMax if (i+j)%(2*s) else 0
            yield 0      if (i+j)%(2*s) else valMax
            yield int(j*yStep)

def premultArray4(w,h,buf,bpp=16):
    valMax = float(2**bpp - 1)
    for i in range(0,4*w*h,4):
        alpha = buf[i+3]/valMax
        buf[i+0] = int(buf[i+0]*alpha)
        buf[i+1] = int(buf[i+1]*alpha)
        buf[i+2] = int(buf[i+2]*alpha)

    return buf

def writeTIFF16(filename, data, size=(8,8), attributes={}):
    w,h = size
    spec = oiio.ImageSpec(w,h,4,oiio.UINT16)
    for key,val in attributes.items():
        spec.attribute(key,val)
    out = oiio.ImageOutput.create(filename)
    assert out, "Can not create ImageOutput \"%s\"" % oiio.getError()
    assert out.open(filename, spec, oiio.Create ), "Can not open %s : \"%s\"" % (filename, oiio.getError())
    out.write_image(spec.format, data)
    out.close()
    print filename

def printArray(w,h,buf):
    for j in range(h):
        line = list()
        for i in range(w):
            offset = 4*(h*j+i)
            r = buf[offset+0]
            g = buf[offset+1]
            b = buf[offset+2]
            a = buf[offset+3]
            line.append("(%i,%i,%i,%i)"%(r,g,b,a))
        print " ".join(line)

def main():
    references=(("ref_Checker16i_unassociated.tif", {"oiio:UnassociatedAlpha":1}),
                ("ref_Checker16i_unassociated_nometadata.tif", {}),
                ("ref_Checker16i_premult.tif",      {"oiio:UnassociatedAlpha":0}),
                ("ref_Checker16i_premult_nometadata.tif", {}),
                )

    w=8
    h=8

    a = array.array('H', genArray4(8,8,16))
    for filename,attribs in references[:2]:
        writeTIFF16( filename, a, (w,h), attribs)
    printArray(w,h,a)

    premultArray4(w,h,a)

    for filename,attribs in references[2:]:
        writeTIFF16( filename, a, (w,h), attribs)
    printArray(w,h,a)

main()

