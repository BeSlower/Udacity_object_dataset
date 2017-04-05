import os

pwd = os.getcwd()
write_filename = 'trainval.txt'
f = open(write_filename, 'wb')
for annot_file in os.listdir(pwd + '/annotations'):
    img_name = annot_file.split('.')[0]
    f.write(img_name+'\n')
f.close()