#Import packages
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

STEP = 0.0005 #increment

#Define 2D Gaussian function
def gaussian2D(x, y, sigma):
    return (1/(2*np.pi*sigma**2))*np.exp(-1*(x**2+y**2)/(2*sigma**2))

#Plot points
def plot(z):
    plt.imshow(z.T)
    plt.gca().invert_yaxis()  # flip axes to get imshow to plot representatively
    plt.xlabel("X"); plt.ylabel("Y"); plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)

def main(limit, sigma=1):
    xmin, xmax, ymin, ymax = limit
    X = np.arange(float(xmin), float(xmax), STEP)
    Y = np.arange(float(ymin), float(ymax), STEP)
    Z = []  # 1D array
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))
    ZZ = np.array(Z).reshape(len(X), len(Y))  # 2D array
    #plot(ZZ)
    return ZZ

if __name__ == "__main__":

    #Determine number of cores on computer
    my_cores = os.cpu_count()
    #print(f'Number of cores: {my_cores}')
    start = time.time()

    workers = []
    runtimes = []

    max_workers = 1

    #Run the program for max_workers + 100 iterations, or until crash
    while max_workers <= my_cores + 100:
        try:
            start = time.time()
            serial = False

            xmin = float(sys.argv[1])
            xmax = float(sys.argv[2])
            ymin = float(sys.argv[3])
            ymax = float(sys.argv[4])

            X = np.arange(float(xmin), float(xmax), STEP)
            Y = np.arange(float(ymin), float(ymax), STEP)

            limits = []
            x0 = xmin
            for x1 in np.linspace(xmin, xmax, max_workers + 1)[1:]:
                limits.append([int(x0), int(x1), ymin, ymax])
                x0 = x1
    
            z = np.array([])
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                 executor.submit(main, limit): i for i, limit in enumerate(limits)
                }

                #reordering futures for plotting
                results = [None] * max_workers

                for future in as_completed(futures):
                    index = futures[future]
                    results[index] = future.result()

            z = np.vstack(results) #cleaner way to stack array
            #plot(z)
            elapsed = time.time() - start
            workers.append(max_workers)
            runtimes.append(elapsed)

            print(f"Workers: {max_workers}, Elapsed Time: {elapsed}s")

        except Exception as e:
            print(f'\nCrash occurred at max_workers = {max_workers}')
            print(f'Error: {e}')
            break

        if max_workers < my_cores:
            max_workers += 1
        else: 
            max_workers += 5

        #plt.show()

    #Plot of max_workers vs. runtime
    plt.figure()
    plt.plot(workers, runtimes, marker='o')
    plt.xlabel('max_worker value')
    plt.ylabel('Time elapsed (s)')
    plt.title('Scaling Task: Workers vs. Runtime')
    plt.show()
