from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pylab import *

# Low Level: Primitive operations where Input and Output are Images, i.e.: noise reduction, contrast enhancement
# Sharpening
# Noise removal
# De-blurring
# Blurring

# Mid Level: Extraction of attributes from Images, i.e.: edges, contours or regions extractions
# Edge detection
# Binary Thresholding
from skimage import data
scanned = data.page()
plt.imshow(scanned)
plt.show()
# Contrast enhancement

# High Level: Analysis or interpretation of content of an Image
# Segmentation / labeling
