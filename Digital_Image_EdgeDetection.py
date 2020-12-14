import cv2
from skimage import img_as_ubyte, img_as_int, filters
from scipy import ndimage
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


# Vertical Edges with Prewitt Mask
moon = cv2.imread(r'C:\Users\Patxi\Downloads\images\images\moon.jpg',0)
prewitt_vertical = np.array([[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]], dtype='float64')  # Kernel
moon_int = img_as_int(moon)
prewitt_vertical_out = img_as_ubyte(ndimage.convolve(moon_int, prewitt_vertical))
plt.imshow(prewitt_vertical_out, cmap='gray')
plt.show()

# Horizontal Edges with Prewitt Mask
prewitt_horizontal = np.array([[-1, -1, -1],[0, 0, 0],[1, 1, 1]], dtype='float64')  # Kernel
prewitt_horizontal_out = img_as_ubyte(ndimage.convolve(moon_int, prewitt_vertical))
plt.imshow(prewitt_horizontal_out, cmap='gray')
plt.show()

# Edge detection with Sobel Operator
a = Image.open(r'C:\Users\Patxi\Downloads\images\images\moon.jpg')
b = filters.sobel(a)
plt.imshow(b, cmap='gray')
plt.show()

# Edge detection with Sobel Operator in OpenCV
img = cv2.imread(r'C:\Users\Patxi\Downloads\images\images\profile.jpg',0)
sobel_x = cv2.Sobel(img, -1, 1, 0, ksize=5)
sobel_y = cv2.Sobel(img, -1, 0, 1, ksize=5)
plt.imshow(sobel_x)
plt.show()
plt.imshow(sobel_y)
plt.show()

# Edge detection with Laplacian Operator in OpenCV
img = cv2.imread(r'C:\Users\Patxi\Downloads\images\images\profile.jpg',0)
output = cv2.Laplacian(img, -1)
plt.imshow(output)
plt.show()
