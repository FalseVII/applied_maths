"""
This script will
    1. Retrieve an image from a server
    2. Convert it to grayscale and save it in a 2D array
    3. Create a integral image from it
    4. Normalise the integral image and save it as a grayscale image
    5. Prompt the user to enter a (x, y) position and width and height
    6. Calculate the sum of the region entered
    7. Plot the grayscale image with a bounding-box around that region
    8. Display in the title the sum of all pixels in that region
"""
import matplotlib.image
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
import matplotlib.pyplot as plt
import matplotlib.patches

class IntImage(object):
    def __init__(self, imageData):
        self.height, self.width = imageData.shape
        self.IImage = np.copy(imageData)
        self.II()

    def II(self):
        self.IImage = self.IImage.cumsum(axis=0).cumsum(axis=1)
        self.normAndSave(self.IImage)

    def CalculateSum(self, x, y, w, h):
        d = self.IImage[x+w][y+h]
        a = self.IImage[x][y]
        b = self.IImage[x][y+h]
        c = self.IImage[x+w][y]
        sum = d + a - b - c
        return(sum)

    def normAndSave(self, array):
        min = np.min(array)
        max = np.max(array)

        normImage = (array-min)/(max-min)*255
        outFile = Image.fromarray(normImage)
        outFile.convert('L').save("IntegralImage.png")
        outFile.show()

def LoadImageFromURL(url):
    """
        Make a  http request for an image, download and open the image
        giving information about its file format, image size and mode.
        Finially display the image.
    :param url:
    :return: image
    """
    image_url = url
    response = requests.get(image_url)
    #image = Image.open(BytesIO(response.content)).convert('LA') - To convert directly to grayscale
    image = Image.open(BytesIO(response.content))
    print ("Image acquired:")
    print ("Image Name: {0}".format(os.path.basename(image_url)))
    print ("Image Size: {0}".format(image.size))
    print ("Image Format: {0}".format(image.mode))
    image.show()
    return image

def convertTo2DArray(img):
    """
        Conver the image to a 2D gray scale image with grayscale values.
        Information about the array are printed to the user
    :param img:
    :return: 2d numpy array
    """
    #width, height = img.size
    grayImage =  img.convert('L')
    grayImage.save("GrayImage.png")
    print((type(grayImage)))
    #imageMat = np.array(grayImage).reshape(width, height)
    imageMat = np.asanyarray(grayImage)
    print("\n=============================\n2D Array Details")
    print("Class:\t{0}\nSize:\t{1}\nDimensions:\t{2}".format(type(imageMat), np.size(imageMat), imageMat.shape))
    return imageMat

def plotRegion(x,y,width, height, titlesum):
    """
    This function will draw them region of the area being calculated
    :return: Nothing to return
    """
    img = matplotlib.image.imread("GrayImage.png")
    #img = Image.open("GrayImage.png").convert("L")
    figure, ax = matplotlib.pyplot.subplots(1)
    region = matplotlib.patches.Rectangle((x,y), width, height, edgecolor='r', facecolor='none', lw=5)
    ax.imshow(img, cmap='gray')
    ax.add_patch(region)
    plt.title("Sum of pixels in red region: {0} ".format(titlesum))
    plt.show()


def main():
    url = 'https://jsfractioncalcdemo.z6.web.core.windows.net/MASE/images/URL_Image.png'
    img = LoadImageFromURL(url)
    imgArray = convertTo2DArray(img)
    ii = IntImage(imgArray)
    print('Data has been sucessfully loaded\nNow you can calculate the area within the image using 4 points')
    x = int(input("Select x position: "))
    y = int(input("Select x position: "))
    width = int(input("Select width: "))
    height = int(input("Select height: "))
    areaSum = ii.CalculateSum(x,y,width,height)
    print("The sum of pixels, at ({0}, {1}) with width: {2} and height: {3} = {4}".format(x,y,width,height, areaSum))
    plotRegion(x,y,width, height, areaSum)

if __name__=="__main__":
    main()
