import os

image_path = 'I:\CS3-New\Source\Chuangshi'

def get_filelist(dir, Filelist):
	newDir = dir
	if os.path.isfile(dir):
		Filelist.append(dir)
	elif os.path.isdir(dir):
		for s in os.listdir(dir):
			newDir=os.path.join(dir,s)
			get_filelist(newDir, Filelist)
	return Filelist


if __name__ =='__main__' :
    list = get_filelist(image_path, [])
    print(len(list))
    for e in list:
        if(".h" in e ):
            print(e[e.find('Chuangshi')+10:])

