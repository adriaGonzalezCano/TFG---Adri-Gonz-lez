from time import time
import matplotlib.pyplot as plt
from os import listdir
import os
import numpy as np

#Afegir/eliminar un experiment nou dins la carpeta data per poder executar sense modificar els path

PATH2DATA = "./data/"

SAVE_RESULTS = True

def getListExperiments():
    return listdir(PATH2DATA)

def main():

    listExperiments = getListExperiments()

    for experiment in listExperiments:
        # if experiment not in ['30 deg']:#, '40 deg', '60 deg']:
        #     continue

        PATH2POSITIONS = PATH2DATA + experiment + "/coordinates/"
        RESULTS_2D_PATH = "./results/"+ experiment +"/2d/"

        #Reading the coordinates files
        coordinates_files = listdir(PATH2POSITIONS)
        coordinates_files.sort()
        print(coordinates_files)

        #Creating the  results folder if not existing
        if SAVE_RESULTS:
            
            if not os.path.exists(RESULTS_2D_PATH):
                os.makedirs(RESULTS_2D_PATH)

        old_particles_ids = 0
        color_list = []

        #Itereating over the N coordinate.dat files
        for i in range(12):

            #Preparing the 2d visualization of the particles
            fig_2d = plt.figure("2D", figsize=(11,7))
            # plt.axis('equal')
            plt.gca().set_aspect('equal', adjustable='box')
            ax_2d = fig_2d.add_subplot()
            ax_2d.set_title("t=0."+str(i+1).zfill(3) + "s | Injection_Angle=" + experiment)
            ax_2d.set_xlabel("x")
            ax_2d.set_ylabel("y")
            ax_2d.set_xlim(0.0, 0.65)
            ax_2d.set_ylim(-0.17, 0.17)

            #Reading the coordinate.dat file which contains the position of each particle at time t
            print("Processing cartesian file: ", PATH2POSITIONS+"coordinates0."+str(i+1)+".csv")
            data = np.genfromtxt(PATH2POSITIONS+"coordinates0."+str(i+1)+".csv", dtype=float, delimiter=',')[1:]
    
            #Check if particles are old ones, as they don't change in the file position and at t=0 of a particle we can know
            #from where it started to asign a specific colour along the visualization.
            print("Number of particles in the simulation: ", len(data))
            for idx, particle in enumerate(data):
                if idx > 30000:
                    break
                if idx < old_particles_ids:
                    ax_2d.scatter(particle[0], particle[1], c = color_list[idx], s = 2,
                    linewidth = 0)
                else:
                    #Checking the starting point of the particle and plotting them into the chart
                    if particle[1] < 0:

                        ax_2d.scatter(particle[0], particle[1], c = 'blue', s = 2,
                        linewidth = 0)
                        color_list.append('blue')
                    else:
                        ax_2d.scatter(particle[0], particle[1], c = 'red', s = 2,
                        linewidth = 0)

                        color_list.append('red')
                
            print("--------End Document 0.%d------------" %(i+1))
            
            old_particles_ids = len(data)

            # draw the plot and saving it
            plt.draw() 
            plt.pause(0.03)
            if SAVE_RESULTS:
                fig_2d.savefig(RESULTS_2D_PATH+"timestamp_"+str(i)+'.png')

            plt.clf()
        #plt.show()
        

if __name__ == "__main__":
    main()