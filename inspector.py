import pickle
from PIL import Image
import numpy as np

with open('img.p','rb') as f:
    a=pickle.load(f)

for i in a:
    img = Image.fromarray(i, 'RGB')
    img.save('my.png')
    img.show()