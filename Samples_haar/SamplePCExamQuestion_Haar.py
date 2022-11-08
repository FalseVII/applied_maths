import numpy as np
from PIL import Image
import requests
from io import BytesIO
import pywt as pw
import matplotlib.pyplot as plt

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
    image = Image.open(BytesIO(response.content))
    printImageInfo(image)
    return image

def LoadImageFromFile(fileName):
    """
        Read an image from a local file
    :param fileName:
    :return: image
    """
    image = Image.open(fileName)
    printImageInfo(image)
    return image

def printImageInfo(image):
    print ("Image acquired:")
    print ("Image Size: {0}".format(image.size))
    print ("Image Format: {0}".format(image.mode))
    #image.show()

def convertTo2DArray(img):
    """
        Convert the image to a 2D gray scale image with grayscale values.
        Information about the array are printed to the user
    :param img:
    :return: 2d numpy array
    """

    grayImage =  img.convert('L')
    print((type(grayImage)))
    imageMat = np.asanyarray(grayImage)
    imageMat = imageMat.astype(np.int)  # Students will get an error if this line is not in the file
    print("\n=============================\n2D Array Details")
    print("Class:\t{0}\nSize:\t{1}\nDimensions:\t{2}".format(type(imageMat), np.size(imageMat), imageMat.shape))
    return imageMat


def Haar_dwt2D(imgMat):
    """
        Preform a 2D Haar decomposition on an image
    :param imgArray (2D):
    :return:
    """
    titles = ['Approximation', ' Horizontal detail',
              'Vertical detail', 'Diagonal detail']
    coeffs2 = pw.dwt2(imgMat, 'haar')
    LL, (LH, HL, HH) = coeffs2
    np.savetxt(titles[0] + ".csv", LL, delimiter=",", fmt='%f')
    np.savetxt(titles[1] + ".csv", LH, delimiter=",", fmt='%f')
    np.savetxt(titles[2] + ".csv", HL, delimiter=",", fmt='%f')
    np.savetxt(titles[3] + ".csv", HH, delimiter=",", fmt='%f')



def loadFromFile():
    print('Loading Data')
    titles = ['Approximation', ' Horizontal detail',
              'Vertical detail', 'Diagonal detail']

    LL = np.loadtxt(open(titles[0]+".csv", "rb"), delimiter=",")
    LH = np.loadtxt(open(titles[1]+".csv", "rb"), delimiter=",")
    HL = np.loadtxt(open(titles[2]+".csv", "rb"), delimiter=",")
    HH = np.loadtxt(open(titles[3]+".csv", "rb"), delimiter=",")

    print("Reconstructing data")
    data = LL, (LH, HL, HH)
    img = pw.idwt2(data, 'haar')
    saveGrayImage(img)
    plt.imshow(img, cmap='gray')
    plt.show()


def saveGrayImage(img):
    min = np.min(img)
    max = np.max(img)
    img = (img-min)/(max-min)*255
    outFile = Image.fromarray(img)
    outFile.convert('L').save("RecomposedGrayScaleImage.png")

def main():
    #url = 'https://homepages.cae.wisc.edu/~ece533/images/lena.png'
    #img = LoadImageFromURL(url)

    """If the students is unable to load from the URL then they must 
    load from a local file.  This is handled in the next two lines"""
    fileName = 'lena.png'
    img = LoadImageFromFile(fileName)
    imgArray = convertTo2DArray(img)
    Haar_dwt2D(imgArray)
    loadFromFile()
    print('Finished')

if __name__=='__main__':
    main()