# Author Jamie Booth
# This program takes a vasprun.xml file as input and outputs the projected density of states
# for each atom and spin into a separate text file. 
# The energies are the first column, which are shifted by the fermi level (i.e. Efermi = 0 eV)
# Obviously this only works if you have set LORBIT appropriately in your INCAR.

import xml.etree.ElementTree as etree
import numpy as np
import csv

# Init some empty lists
nedos = []
spin = []
na = []
ef = []

# Parse vasprun.xml using elementTree
tree = etree.parse('vasprun.xml')
root = tree.getroot()

# Get number of atoms which dos is projected onto
for element in root.findall("./atominfo/atoms"):
    na.append(element.text)
    
natoms = int(na[0])

# Get Fermi level
for child in root.findall("./calculation/dos/i[@name='efermi']"):
        ef.append(child.text)
        
efermi = float(ef[0])

#Get the ISPIN value
for element in root.findall("./parameters/separator[@name='electronic']//separator[@name='electronic spin']/i[@name='ISPIN']"):
    spin.append(element.text)
    
ispin = int(spin[0])

#Get the NEDOS value
for element in root.findall("./parameters/separator[@name='dos']/i[@name='NEDOS']"):
    nedos.append(element.text)
    
nd = int(nedos[0])

# Two separate loops for non spin-resolved and spin-resolved

if ispin == 1:
    # Get data nodes
    nodeList = tree.findall('./calculation/dos/partial/array/set/set/set[@comment="spin 1"]/r')
    
    eigs = []
    dos = []
    # Write data as floats to a list
    for child in nodeList:
            
        nodeValues = child.text.split(" ")
        
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[:])
    # Convert list to numpy array
    x = np.array(eigs)
    # Get first column (Energies) and shift by Fermi level
    x_data = x[:,0]
    
    energy = x_data-efermi
    # Get rest of columns and combine with shifted energies into new array
    y_values = x[:,1:]
    
    pdos = np.column_stack((energy,y_values))        
    # Loop to write each atoms projected dos to a separate text file, i.e. n(files) = n(atoms)
    for i in range(0,natoms):
        dos_i = pdos[(i)*nd:(i+1)*nd,:]
        j=i+1
        with open('pdos_atom_%s.txt' % j, 'w') as f:
            csv.writer(f, delimiter=' ').writerows(dos_i)

# This does everything the above loop does, but twice, once for each spin
if ispin == 2:
    # Get data nodes
    nodeList = tree.findall('./calculation/dos/partial/array/set/set/set[@comment="spin 1"]/r')
    
    eigs = []
    dos = []
    # Write data as floats to a list
    for child in nodeList:
            
        nodeValues = child.text.split(" ")
        
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[:])
    # Convert list to numpy array
    x1 = np.array(eigs)
    # Get first column (Energies) and shift by Fermi level
    x_data1 = x1[:,0]
    
    energy1 = x_data1-efermi
    # Get rest of columns and combine with shifted energies into new array
    y_values1 = x1[:,1:]
    
    pdos1 = np.column_stack((energy1,y_values1))
    # Loop to write each atoms projected dos to a separate text file, i.e. n(files) = n(atoms) for spin 1
    for i in range(0,natoms):
        dos_i = pdos1[(i)*nd:(i+1)*nd,:]
        j=i+1
        with open('pdos_atom_%s_spin_1.txt' % j, 'w') as f:
            csv.writer(f, delimiter=' ').writerows(dos_i)
            
    # Get data nodes
    nodeList = tree.findall('./calculation/dos/partial/array/set/set/set[@comment="spin 2"]/r')
    
    eigs = []
    dos = []
    # Write data as floats to a list
    for child in nodeList:
            
        nodeValues = child.text.split(" ")
        
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[:])
    # Convert list to numpy array
    x2 = np.array(eigs)
    # Get first column (Energies) and shift by Fermi level
    x_data2 = x2[:,0]
    
    energy2 = x_data2-efermi
    # Get rest of columns and combine with shifted energies into new array
    y_values2 = x2[:,1:]
    
    pdos2 = np.column_stack((energy2,y_values2))        
    # Loop to write each atoms projected dos to a separate text file, i.e. n(files) = n(atoms) for spin 2
    for i in range(0,natoms):
        dos_i = pdos2[(i)*nd:(i+1)*nd,:]
        j=i+1
        with open('pdos_atom_%s_spin_2.txt' % j, 'w') as f:
            csv.writer(f, delimiter=' ').writerows(dos_i)
