from PIL import Image  # Pillow python Imaging Library adds image processing capabilities to your Python interpreter.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

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


# Create an Image
x = np.random.randint(0,255,(300,300)).astype('uint8')
plt.imshow(x,cmap=cm.gray)
plt.show()
y = np.random.randint(0,255,(300,400,3)).astype('uint8')
plt.imshow(x)
plt.show()

