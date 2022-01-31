"""Python script to open fits image with [x,y,i,j] size where
x is x axis, y is y axis, i is axis value, e.g., frequency and j
is j axis value, e.g., Stokes I, etc."""



from numpy import *
from matplotlib.pyplot import *
from astropy.io import fits
from mpl_toolkits.mplot3d import axes3d
from astropy.wcs import WCS
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("image", type=argparse.FileType('rb')) #required to read fits, make fits
                                                           #file an argument called image
args = vars(parser.parse_args()) #vars extract the key in dictionary from above called image

def get_arg(idict):
    #function use the name of fits file
    #and return already the string of the fits image
    image = idict["image"]
    return image



img = fits.open(get_arg(args)) #get_arg(args) = "your-fits-file.fits"

#below this is only works for fits file [x,y,i,j] size, but nothing to worry
#if fits file is [x,y] just use dat = img[0].data and now dat is a
#2d array of x and y pixel and a value for each pixel.

dat = img[0].data 
dat = dat[0]
dat = dat[0]

hd = img[0].header
my_wcs = WCS(hd).celestial

x = arange(0,hd["NAXIS1"]) 
y = arange(0,hd["NAXIS2"])

x = x * abs(hd["CDELT1"]) * 3600
y = y * abs(hd["CDELT2"]) * 3600
X,Y = meshgrid(x,y)

fig = figure()

ax1 = fig.add_subplot(221, projection = my_wcs) 
ax1.imshow(dat, cmap = "cubehelix")

ax2 = fig.add_subplot(222, projection = my_wcs) 
ax2.imshow(10 * log10(dat), cmap = "cubehelix")

ax3  = fig.add_subplot(223, projection="3d") 
surf = ax3.plot_surface(X,Y,dat, cmap = "rainbow")
fig.colorbar(surf)

ax4  = fig.add_subplot(224, projection="3d") 
surf = ax4.plot_surface(X,Y,10 * log10(dat), cmap = "rainbow")
fig.colorbar(surf)



show()
