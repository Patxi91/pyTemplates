# Pillow python Imaging Library adds image processing capabilities to your Python interpreter.
from PIL import Image

img = Image.open(r'C:\Users\Patxi\Downloads\images\images\profile.jpg')
img.show()

new_img = img.convert('L')  # Convert image to grayscale
new_img.show()


# Analyze Image with numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

A = plt.imread(r'C:\Users\Patxi\Downloads\images\images\profile.jpg')
plt.imshow(A)
plt.show()
print(A)
print(np.shape(A))
print(type(A))
print(A.dtype)

im = array(Image.open(r'C:\Users\Patxi\Downloads\images\images\profile.jpg'))
imshow(im)
x = [100,150,300,400]
y = [50, 500, 200, 500]
plot(x,y,'r*')
plot(x[:2],y[:2],'r')
plot(x[2:],y[2:],'ks:')
show()


# Adding Interactive Annotations
im = array(Image.open(r'C:\Users\Patxi\Downloads\images\images\profile.jpg'))
imshow(im)
# Select 4 points manually
pt = ginput(4)
print('You selected: ', pt)
show()