import OpenImageIO as oiio
import array

def genArray4(w,h,precision=16):
    valMax = 2**precision - 1
    s=1
    yStep = valMax/(h-1)
    for j in range(h):
        for i in range(w):
            yield 0
            yield valMax if (i+j)%(2*s) else 0
            yield 0      if (i+j)%(2*s) else valMax
            yield int(j*yStep)


def main():
    filename="ref_Checker16i_unassociated.tif"
    #filename="ref_Checker16i_premult.png"
    spec = oiio.ImageSpec(8,8,4,oiio.UINT16)
    out = oiio.ImageOutput.create(filename)
    if not out:
        print oiio.getError()
        return
    #spec.attribute("oiio:alpha",1)
    spec.attribute("oiio:UnassociatedAlpha", 1)
    if not out.open(filename, spec, oiio.Create ):
        print "Could not open %s : \"%s\" " % (filename, out.geterror())
        return
    a = array.array('H', genArray4(8,8,16))
    print a
    out.write_image(spec.format, a)
    out.close()

main()
