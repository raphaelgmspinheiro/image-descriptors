import pickle
import sys
import os

path= '#### PATH .db FILE'
img_dataset = '#### BINARY IMAGES DIR'
img_names = [
    f for f in os.listdir(img_dataset)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif'))
]

describe = os.listdir(path)

for j in range(int(len(img_names))):
    if j == len(img_names):
        break
    if 'txt' in img_names[j]:
        img_names.remove(img_names[j])

db = pickle.load(open(path+describe[0],'rb'), encoding="latin-1")

if not isinstance(list(db.keys())[0], str):
	db = {key.decode(): v for key, v in db.items()} 
new_file=open("describe.txt",mode="w",encoding="latin-1")

for k in img_names:
    for i in db[k]:
        new_file.write(str(str(i)+' '))
    new_file.write('\n')

with open("names.txt", "w") as output:
    output.write(str(img_names))

