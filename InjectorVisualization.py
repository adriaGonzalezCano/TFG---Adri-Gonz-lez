from time import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
import os
import numpy as np

#Afegir/eliminar un experiment nou dins la carpeta data per poder executar sense modificar els path

PATH2DATA = "./data/"

SAVE_RESULTS = True

VISUALIZATION_3D = False

def getListExperiments():
    return listdir(PATH2DATA)

def main():

    listExperiments = getListExperiments()

    for experiment in listExperiments:
        PATH2POSITIONS = PATH2DATA + experiment + "/coordinates/"
        RESULTS_3D_PATH = "./results/"+ experiment +"/3d/"
        RESULTS_2D_PATH = "./results/"+ experiment +"/2d/"

        #Reading the coordinates files
        coordinates_files = listdir(PATH2POSITIONS)
        coordinates_files.sort()
        print(coordinates_files)

        #Creating the  results folder if not existing
        if SAVE_RESULTS:
            if not os.path.exists(RESULTS_3D_PATH) and VISUALIZATION_3D:
                os.makedirs(RESULTS_3D_PATH)
            
            if not os.path.exists(RESULTS_2D_PATH):
                os.makedirs(RESULTS_2D_PATH)

        old_particles_ids = 0
        color_list = []

        #Itereating over the N coordinate.dat files
        for i in range(25):
            
            #Preparing the 3D Visualization (Ho pots borrar per posar a l'informe)
            if VISUALIZATION_3D:
                fig_3d = plt.figure("3D")
                ax_3d = fig_3d.add_subplot(projection='3d')
                ax_3d.set_title("3D of particles motion t=0."+str(i+1).zfill(3))
                ax_3d.set_xlabel("x")
                ax_3d.set_ylabel("z")
                ax_3d.set_zlabel("y")
                ax_3d.set_xlim3d(0.0, 0.5)
                ax_3d.set_zlim3d(-0.1, 0.1)
                ax_3d.set_ylim3d(-0.004, 0.004)

                #Es pot modificar l'angle de la visualitzacio 3d
                ax_3d.view_init(elev=10., azim=-80)

            #Preparing the 2d visualization of the particles
            fig_2d = plt.figure("2D")
            ax_2d = fig_2d.add_subplot()
            ax_2d.set_title("t=0."+str(i+1).zfill(3) + " | Injection_Angle=" + experiment)
            ax_2d.set_xlabel("x")
            ax_2d.set_ylabel("y")
            ax_2d.set_xlim(0.06, 0.5)
            ax_2d.set_ylim(-0.1, 0.1)

            #Reading the coordinate.dat file which contains the position of each particle at time t
            print("Processing cartesian file: ", PATH2POSITIONS+"coordinates0."+str(i+1)+".csv")
            data = np.genfromtxt(PATH2POSITIONS+"coordinates0."+str(i+1)+".csv", dtype=float, delimiter=',')[1:]
    
            #Check if particles are old ones, as they don't change in the file position and at t=0 of a particle we can know
            #from where it started to asign a specific colour along the visualization.
            print("Number of particles in the simulation: ", len(data))
            for idx, particle in enumerate(data):
                if idx > 12000:
                    break
                if idx < old_particles_ids:
                    if VISUALIZATION_3D:
                        ax_3d.scatter(particle[0], particle[2], particle[1], c = color_list[idx], s = 10,
                        linewidth = 0)

                    ax_2d.scatter(particle[0], particle[1], c = color_list[idx], s = 10,
                    linewidth = 0)
                else:
                    #Checking the starting point of the particle and plotting them into the chart
                    if particle[1] < 0:
                        if VISUALIZATION_3D:
                            ax_3d.scatter(particle[0], particle[2], particle[1], c = 'blue', s = 10,
                            linewidth = 0)


                        ax_2d.scatter(particle[0], particle[1], c = 'blue', s = 10,
                        linewidth = 0)
                        color_list.append('blue')
                    else:
                        if VISUALIZATION_3D:
                            ax_3d.scatter(particle[0], particle[2], particle[1], c = 'red', s = 10,
                            linewidth = 0)


                        ax_2d.scatter(particle[0], particle[1], c = 'red', s = 10,
                        linewidth = 0)

                        color_list.append('red')
                
            print("--------End Document 0.%d------------" %(i+1))
            
            old_particles_ids = len(data)

            print(data)
            print(color_list)
            # draw the plot and saving it
            plt.draw() 
            plt.pause(0.03)
            if SAVE_RESULTS:
                if VISUALIZATION_3D:
                    fig_3d.savefig(RESULTS_3D_PATH+"timestamp_"+str(i)+'.png')
                fig_2d.savefig(RESULTS_2D_PATH+"timestamp_"+str(i)+'.png')

            plt.clf()
        #si ho descomentes (eliminant el #) pots moure l'angle de la visualitzacio 3D
        #plt.show()
        

if __name__ == "__main__":
    main()