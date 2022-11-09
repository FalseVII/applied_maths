from DCT import DCT_Demo
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image

def save_and_plot(image, title_name):
    plt.imshow(image, plt.cm.gray)
    plt.title(title_name)
    plt.savefig(title_name + ".png")
    plt.show()



if __name__ == '__main__':
    image = np.random.randint(0, 255, (8, 8))
    save_and_plot(image, "Block_IN")
    value = int(input("Enter the value of Q: "))
    value
    dct = DCT_Demo(value, image)
    dct.Calculate_FDCT()
    print("FDCT:")
    dct.printMatrix(dct.DCT, 1)
    dct.QuantizationStepForward()
    print("Quantization Step Forward:")
    dct.printMatrix(dct.C, 1)
    dct.QuantizationStepInverse()
    print("Quantization Step Inverse:")
    dct.printMatrix(dct.R, 1)
    dct.Calculate_IDCT()
    print("IDCT:")
    dct.printMatrix(dct.fin, 1)
    save_and_plot(dct.fin, "Block_OUT")

