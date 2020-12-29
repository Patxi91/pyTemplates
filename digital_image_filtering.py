from PIL import Image
from PIL import ImageFilter
from pylab import *
import scipy.ndimage
import numpy as np


# Image filtering using the Python imaging library
im0 = Image.open(r'C:\Users\Patxi\Downloads\images\images\moon.jpg').convert('L')
figure(figsize=(15,15))
subplot(3,4,1)
plt.imshow(im0)
plt.title('Original')
subplot(3,4,2)
im2 = im0.filter(ImageFilter.CONTOUR)
plt.imshow(im2)
plt.title('Contour')
subplot(3,4,3)
im3 = im0.filter(ImageFilter.DETAIL)
plt.imshow(im3)
plt.title('Detail')
subplot(3,4,4)
im4 = im0.filter(ImageFilter.EDGE_ENHANCE)  # Laplacian filter
plt.imshow(im4)
plt.title('Edge Enhance')
subplot(3,4,5)
im5 = im0.filter(ImageFilter.EDGE_ENHANCE_MORE)
plt.imshow(im5)
plt.title('Edge Enhance More')
subplot(3,4,6)
im6 = im0.filter(ImageFilter.EMBOSS)
plt.imshow(im6)
plt.title('Emboss')
subplot(3,4,7)
im7 = im0.filter(ImageFilter.FIND_EDGES)
plt.imshow(im7)
plt.title('Find Edges')
subplot(3,4,8)
im8 = im0.filter(ImageFilter.SMOOTH)
plt.imshow(im8)
plt.title('Lowpass 1')
subplot(3,4,9)
im9 = im0.filter(ImageFilter.SMOOTH_MORE)
plt.imshow(im9)
plt.title('Lowpass 2')
subplot(3,4,10)
im10 = im0.filter(ImageFilter.SHARPEN)
plt.imshow(im10)
plt.title('Sharpen')
# Custom kernels
size = (3,3)
kernel1 = [1,1,1,1,-1,1,-1,-1,-1]
ker1 = ImageFilter.Kernel(size,kernel1,scale=None,offset=0)
subplot(3,4,11)
im11 = im0.filter(ker1)
plt.imshow(im11)
plt.title('Custom Filter 1')
kernel2 = [1,0,-1,1,0,-1,0,0,-1]
ker2 = ImageFilter.Kernel(size,kernel2,scale=None,offset=0)
subplot(3,4,12)
im12 = im0.filter(ker2)
plt.imshow(im12)
plt.title('Custom Filter 2')
plt.show()

# Mean Filter (smooth)
img = Image.open(r'C:\Users\Patxi\Downloads\images\images\profile.jpg')
img_gray = img.convert('L')  # Convert image to grayscale
k = np.ones((5,5))/25 # Kernel
b = scipy.ndimage.filters.convolve(img_gray,k)
b = Image.fromarray(b)
b.save(r'C:\Users\Patxi\Downloads\images\images\mean_profile.jpg')

# Minimum Filter (smooth)
img = Image.open(r'C:\Users\Patxi\Downloads\images\images\lena_noisy.png')
b = scipy.ndimage.filters.minimum_filter(img, size=5, footprint=None, output=None, mode='reflect', cval=0.0, origin=0)
b = Image.fromarray(b)
b.show()

# Maximum Filter
img = Image.open(r'C:\Users\Patxi\Downloads\images\images\lena_noisy.png')
b = scipy.ndimage.filters.maximum_filter(img, size=5, footprint=None, output=None, mode='reflect', cval=0.0, origin=0)
b = Image.fromarray(b)
b.show()

# Median Filter (noise reduction)
img = Image.open(r'C:\Users\Patxi\Downloads\images\images\lena_noisy.png')
b = scipy.ndimage.filters.median_filter(img, size=5, footprint=None, output=None, mode='reflect', cval=0.0, origin=0)
b = Image.fromarray(b)
b.show()
