from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pylab import *
from skimage import data

# Low Level: Primitive operations where Input and Output are Images, i.e.: noise reduction, contrast enhancement
# Sharpening
# Noise removal
# De-blurring
# Blurring

# Mid Level: Extraction of attributes from Images, i.e.: edges, contours or regions extractions
# Edge detection
# Binary Thresholding
scanned = data.page()
#plt.imshow(scanned, cmap = cm.gray)
thres = np.zeros(shape(scanned)).astype('uint8')
threshold = 150
thres[scanned < threshold] = 0
thres[scanned >= threshold] = 255
plt.imshow(thres, cmap = cm.gray)
plt.show()
# Contrast enhancement

# High Level: Analysis or interpretation of content of an Image
# Segmentation / labeling
