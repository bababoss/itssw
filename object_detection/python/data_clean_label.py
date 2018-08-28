from shutil import copyfile

# copyfile(src, dst)
src="/home/cogknit/experiments/dataset/clean_900_dataset/"
dst="/home/cogknit/experiments/dataset/900_dataset_label/"
for i in label_t:
    name=os.path.split(i)[-1].split('.')[0]
    #print(name)
    #copyfile(src+name+'.jpg', dst+name+'.jpg')
    copyfile(i, dst+name+'.txt')
    
