# Author Jamie Booth
# Python script for reading in vasprun.xml and outputting bands from band structure calculation
#  to a text file which can be plotted in your favourite program
#  (matplotlib, matlab, gnuplot etc.).
# The eigenvalues are adjusted by subtracting the fermi energy
# During execution the program will print the number of bands to screen.
# To plot obviously you need to plot this many bands vs the x values this program creates,
# so you may need this value to loop over when plotting, depending on how you do it.
# Use a bash script to load a python module and call this program.
# for example:
# module load python/2.7.11
# python /home/your_home_directory_Where_you_saved_this_file/Bands.py
# The plotable output is "bands.txt", 
# the first column is a vector with values between 1 and 100 used as a dummy x value for plotting against.
# The other columns are the bands at each kpoint, if ISPIN = 2 the there are two output files "spin_1_bands.txt" and "spin_2_bands.txt"

import xml.etree.ElementTree as etree
import numpy as np
import csv

#Create empty lists
data=[]
data1=[]
nb = []
ef = []
ptsSegment = []
ispin = []

#Parse vasprun.xml
tree = etree.parse('vasprun.xml')
root = tree.getroot()

#Spin-resolved?
for element in root.findall("./parameters/separator[@name='electronic']//separator[@name='electronic spin']/i[@name='ISPIN']"):
    ispin.append(element.text)
    
spin = int(ispin[0])

#Pull out segments and number of points per segment
for element in root.findall("./kpoints/generation/v"):
    data.append(element.text)
    
for element in root.findall("./kpoints/generation/i[@name='divisions']"):
    ptsSegment.append(element.text)
    
#Convert points per segment to integer
pts = int(ptsSegment[0])

#Get total number of kpoints then create the same number of x values as a vector
kp_list_n = (len(data)-1)*pts

x = np.linspace(1,100,kp_list_n)

#Get parameter section containing NBANDS, extract NBANDS, convert to integer 
# and print to screen, this is needed for plotting
for element in root.findall("./parameters/separator[@name='electronic']/i[@name='NBANDS']"):
    nb.append(element.text)
    
nbands = int(nb[0])

print "NBANDS is", nbands

#Get fermi energy and convert to float
for element in root.findall("./calculation/dos/i[@name='efermi']"):
    ef.append(element.text)
    
efermi = float(ef[0])

# For ISPIN = 1 only one data set
if spin == 1:

    # XPath to eigenvalues and put all children in nodeList
    nodeList = tree.findall('./calculation/eigenvalues/array/set/set[@comment="spin 1"]/set/r')

    nodeValuesAsFloats = []
    eigs = []

    #Split values in nodeList and covert to float, pick first column and write to list "eigs"
    for child in nodeList:
    
        nodeValues = child.text.split(" ")

        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
            
        nodeValuesAsFloats.append(nodeFloats)
        eigs.append(nodeFloats[0])

    #Reshape "eigs" array into matrix of "nbands" rows with "kpt_list_n" columns and 
    # add x values as first row, subtract fermi energy from eigenvalues
    total_eigs = np.reshape(eigs, [kp_list_n, nbands])

    y_values = total_eigs.T-efermi

    bands_data = np.row_stack((x,y_values))

    #Write this matrix to a text file for easy plotting
    with open('bands.txt', 'w') as f:
        csv.writer(f, delimiter=' ').writerows(bands_data)

# For spin-resolved calcs do both spins
if spin == 2:
    # XPath to eigenvalues and put all children in nodeList
   nodeList = tree.findall('./calculation/eigenvalues/array/set/set[@comment="spin 1"]/set/r')

   nodeValuesAsFloats = []
   eigs1 = []

   # Split values in nodeList and covert to float, pick first column and write to list "eigs"
   for child in nodeList:
    
        nodeValues = child.text.split(" ")

        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
            
        nodeValuesAsFloats.append(nodeFloats)
        eigs1.append(nodeFloats[0])
        
   total_eigs1 = np.reshape(eigs1, [kp_list_n, nbands])

   y_values1 = total_eigs1.T-efermi

   bands_data1 = np.row_stack((x,y_values1))
   
   with open('spin_1_bands.txt', 'w') as f:
       csv.writer(f, delimiter=' ').writerows(bands_data1)

   nodeList = tree.findall('./calculation/eigenvalues/array/set/set[@comment="spin 2"]/set/r')

   nodeValuesAsFloats = []
   eigs2 = []

   # Split values in nodeList and covert to float, pick first column and write to list "eigs"
   for child in nodeList:
    
        nodeValues = child.text.split(" ")

        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
            
        nodeValuesAsFloats.append(nodeFloats)
        eigs2.append(nodeFloats[0])
        
   total_eigs2 = np.reshape(eigs2, [kp_list_n, nbands])

   y_values2 = total_eigs2.T-efermi

   bands_data2 = np.row_stack((x,y_values2))
   
   with open('spin_2_bands.txt', 'w') as f:
       csv.writer(f, delimiter=' ').writerows(bands_data2)
