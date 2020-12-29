# Low Level: Primitive operations where Input and Output are Images, i.e.: noise reduction, contrast enhancement
# Mid Level: Extraction of attributes from Images, i.e.: edges, contours or regions extractions
# High Level: Analysis or interpretation of content of an Image, i.e.: segmentation/labeling

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pylab import *
from skimage import data


# Binary Thresholding
scanned = data.page()
#plt.imshow(scanned, cmap = cm.gray)
thres = np.zeros(shape(scanned)).astype('uint8')
threshold = 150
thres[scanned < threshold] = 0
thres[scanned >= threshold] = 255
plt.imshow(thres, cmap=cm.gray)
plt.show()

# Histogram: Relative frequency of occurrence of pixels against the values themselves, discrete probability function.
# Equalization causes histogram to spread out. Usually increases the contrast
img = Image.open(r'C:\Users\Patxi\Downloads\images\images\profile.jpg')
img_gray = img.convert('L')  # Convert image to grayscale
img_gray.show()
img_array = array(img_gray)
figure()
hist(img_array.flatten(), 300)
show()  # Histogram
img1 = np.asarray(img_gray)
img_fl = img1.flatten()
hist, bins = np.histogram(img1, 256, [0, 255])
cdf = hist.cumsum()  # Cumulated distribution function
cdf_m = np.ma.masked_equal(cdf,0)
num_cdf_m = (cdf_m - cdf_m.min())*255
den_cdf_m = cdf_m.max() - cdf_m.min()
cdf_m = num_cdf_m / den_cdf_m
cdf = np.ma.filled(cdf_m,0).astype('uint8')
im2 = cdf[img_fl]
im3 = np.reshape(im2,img1.shape)
im4 = Image.fromarray(im3)
im4.show()  # Equalized

# Image Enhancement Gamma correction: Makes Image brighter
a = img1
b = np.asarray(a)
gamma = 0.5
b1 = b.astype(float)
b3 = np.max(b1)
b2 = b1/b3
b3 = np.log(b2)*gamma
c = np.exp(b3)*255.0
c1 = c.astype(int)
d = Image.fromarray(c1)
d.show()

# Image Enhancement Gray-level transformation
im2 = 255 - img_array  # negative image
im3 = (100.0/255)*img_array + 100  # Clamp to interval 100 ... 200
im4 = 255.0*(img_array/255.0)**2
imshow(im2)
show()
