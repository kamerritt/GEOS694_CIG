#Import packages
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

STEP = .001 #increment

#Define 2D Gaussian function
def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))

#Plot points
def plot(z):
    plt.imshow(z.T)
    plt.gca().invert_yaxis()  # flip axes to get imshow to plot representatively
    plt.xlabel("X"); plt.ylabel("Y"); plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)

def main(xmin, xmax, ymin, ymax, sigma=1):
    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)
    Z = []  # 1D array
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))
    ZZ = np.array(Z).reshape(len(X), len(Y))  # 2D array
    plot(ZZ)

if __name__ == "__main__":
    start = time.time()
    main(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    #main(-2, 2, -2, 2)
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed}s")
    plt.show()