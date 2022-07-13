from PIL import Image, ImageDraw, ImageShow

DEPTH = 7
THRESHOLD = 7

def avgRgb(l,t,r,b,img):
    rsum,gsum,bsum = 0,0,0
    len = 0
    for i in range(l,r):
        for j in range(t,b):
            rc,gc,bc = img.getpixel((i,j))
            rsum += rc
            gsum += gc
            bsum += bc
            len += 1

    return (rsum//len,gsum//len,bsum//len)

def ManhattonError(l,t,r,b,c,img):
    error,len = 0,0
    for i  in range(l,r):
        for j in range(t,b):
            rc,gc,bc = img.getpixel((i,j))
            error += abs(c[0] - rc)
            error += abs(c[1] - gc)
            error += abs(c[2] - bc)
            len += 1

    return error//(3*len)

def weightedAverage(hist):
    """Returns the weighted color average and error from a hisogram of pixles"""
    total = sum(hist)
    value, error = 0, 0
    if total > 0:
        value = sum(i * x for i, x in enumerate(hist)) / total
        error = sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
        error = error ** 0.5
    return value, error


def HistColor(hist):
    """Returns the average rgb color from a given histogram of pixle color counts"""
    r, re = weightedAverage(hist[:256])
    g, ge = weightedAverage(hist[256:512])
    b, be = weightedAverage(hist[512:768])
    e = re * 0.2989 + ge * 0.5870 + be * 0.1140
    return (int(r), int(g), int(b)), e

def quadtree(img,leaf,l,t,r,b,level):

    region = img.crop((l,t,r,b))
    c,err = HistColor(region.histogram())

    if err > THRESHOLD :
        if level < DEPTH :
            lr = l +  (r - l) // 2
            tb = t +  (b - t) // 2
            quadtree(img, leaf, l, t, lr, tb, level+1)
            quadtree(img, leaf, lr, t, r, tb, level+1)
            quadtree(img, leaf, l, tb, lr, b, level+1)
            quadtree(img, leaf, lr, tb, r, b, level+1)
        else :
            leaf.append((l,t,r,b,c))
    else :
        leaf.append((l,t,r,b,c))

def renderCompressedImage(leafNodes,w,h):
    image = Image.new("RGB",(w,h))
    tree_structure_image = Image.new("RGB",(w,h))
    tree_image = Image.new("RGB",(w,h))

    draw = ImageDraw.Draw(image)
    tree_structure = ImageDraw.Draw(tree_structure_image)
    tree = ImageDraw.Draw(tree_image)

    for leaf in leafNodes :
        l,t,r,b,c = leaf
        box = (l,t,r-1,b-1)
        draw.rectangle(box,c)
        tree_structure.rectangle(box,c,"black")
        tree.rectangle(box,"#FFFFFF","black")

    ImageShow.show(image,title="Compressed Image")
    ImageShow.show(tree_structure_image,title="Quad Tree Render")
    ImageShow.show(tree_image,title="Quad Tree Structure")

    image.save("CompressedImage.jpg")
    tree_structure_image.save("QuadTreeRender.jpg")
    image.save("QuadTreeStructure.jpg")

def main():
    image = Image.open(r"C:\Users\Aritra Datta\Documents\BGIM\BIM_4.jpg")
    l,t,r,b = image.getbbox()
    leaf_nodes = []
    quadtree(image,leaf_nodes,l,t,r,b,0)
    renderCompressedImage(leaf_nodes,r,b)

main()
