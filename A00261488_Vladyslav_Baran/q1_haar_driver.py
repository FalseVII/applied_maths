import numpy as np
import requests
import csv
import pywt as pwd
import matplotlib.pyplot as plt


def LoadCSVFromURL(url):
    array = np.asarray(list(csv.reader(requests.get(url).content.decode('utf-8').splitlines(),delimiter=',')))
    return array

def save_image(img, fileName):
    plt.imsave(fileName, img, cmap='gray')

if __name__ == '__main__':
    url = "https://jsfractioncalcdemo.z6.web.core.windows.net/MASE/CSV/Horizontal.csv"
    url2 = "https://jsfractioncalcdemo.z6.web.core.windows.net/MASE/CSV/Diagonal.csv"
    url3 = "https://jsfractioncalcdemo.z6.web.core.windows.net/MASE/CSV/Vertical.csv"
    url4 = "https://jsfractioncalcdemo.z6.web.core.windows.net/MASE/CSV/Approximation.csv"




    horizontal = np.asarray(LoadCSVFromURL(url))
    diagonal = np.asarray(LoadCSVFromURL(url2))
    vertical = np.asarray(LoadCSVFromURL(url3))
    approximation = np.asarray(LoadCSVFromURL(url4))

    # Perform a 1 level inverse discrete wavelet transform on this 2D data
    # using the Haar wavelet.
    coeffs2 = (approximation, (horizontal, vertical, diagonal))
    data = pwd.idwt2(coeffs2, 'haar')

    plt.imshow(data, cmap='gray')
    save_image(data, "Recomposed_image.png")
    plt.show()








