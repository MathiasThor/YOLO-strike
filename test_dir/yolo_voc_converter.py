
import os
from os import walk, getcwd
from PIL import Image

classes = ["CT", "T"]

def refinery(x):
	new_list=list()
	for b in x:
		a=b.split('\n')
		for each in a:
			if each!= '':
				new_list.append(each)
	del new_list[0]
	x=new_list
	nums=list()
	for i in range(0, len(x),4):
		elems= x[i:i+4]
		xmin = elems[0]
	        xmax = elems[2]
	        ymin = elems[1]
	        ymax = elems[3]
		nums.append((xmin, xmax, ymin, ymax))

	return nums


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


"""-------------------------------------------------------------------"""

""" Configure Paths"""
mypath = "/home/mat/Dropbox/CSGO_screens/data/cs-labels/"
myimages = "/home/mat/Dropbox/CSGO_screens/data/cs-images/"
outpath = "/home/mat/Dropbox/CSGO_screens/data/cs-labels_voc/"

cls = "CT"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break



""" Process """

for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\r\n')   #for ubuntu, use "\r\n" instead of "\n"

    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")


    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        if(len(line) >= 2):
           ct = ct + 1
           #print(line + "\n")
           elems = line.split(' ')
	   print elems
	   nums= refinery(elems)
	   for n in nums:
	    xmin, xmax, ymin, ymax = n
	    print (xmin, xmax, ymin, ymax)
	    img_path = str('%s/%s.jpg'%(myimages, os.path.splitext(txt_name)[0]))
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            print(w, h)
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s/images/%s/%s.JPEG\n'%(wd, cls, os.path.splitext(txt_name)[0]))

list_file.close()
