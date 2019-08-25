# Author Jamie Booth
# This code processes the vasprun.xml file to extract the total density of states
# It outputs one file if the calculation is not spin-resolved, and two files if it is.
# They will be "tdos_shifted.txt", or "spin_1_tdos_shifted.txt" and "spin_2_tdos_shifted.txt"
# The energies are shifted with respect to the fermi level, and are in the first column, while the ensity of states is the second column

import xml.etree.ElementTree as etree
import numpy as np
import csv

params = []
spin = []
smear = []

tree = etree.parse('vasprun.xml')
root = tree.getroot()

#Spin-resolved? This finds the ISPIN value
for element in root.findall("./parameters/separator[@name='electronic']//separator[@name='electronic spin']/i[@name='ISPIN']"):
    spin.append(element.text)
    
ispin = int(spin[0])

# This finds the ISMEAR value, this code can only compute band gaps if ISMEAR =-5 (Tetrahedron Method)
for element in root.findall("./parameters/separator[@name='electronic']//separator[@name='electronic smearing']/i[@name='ISMEAR']"):
    smear.append(element.text)
    
ismear = int(smear[0])

#Get the NEDOS value
for element in root.findall("./parameters/separator[@name='dos']/i[@name='NEDOS']"):
    params.append(element.text)
    
nd = int(params[0])

#Spin dependent sectio, it ISPIN = 1 does single spin, if ISPIN = 2 out puts both spin tdos
if ispin == 1:
   
    nodeList = tree.findall('./calculation/dos/total/array/set/set[@comment="spin 1"]/r')
    
    eigs = []
    dos = []
    
    for child in nodeList:
        
        nodeValues = child.text.split(" ")
    
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[0])
        dos.append(nodeFloats[1])
    
    x = np.array(eigs)
    y = np.array(dos)
    
    ef = []
    
    for child in root.findall("./calculation/dos/i[@name='efermi']"):
        ef.append(child.text)
        
    efermi = float(ef[0])
    
    x_values = x[0:nd]
    States = y[0:nd]
    Energy = x_values-efermi
    
    tdos = np.column_stack((Energy,States))
    
    with open('tdos_shifted.txt', 'w') as f:
        csv.writer(f, delimiter=' ').writerows(tdos)
    
    if ismear == -5:    
        
        gap = np.where(Energy>=0)
        
        trunc_states = []
        
        for value in gap:
            trunc_states.append(States[value])
            
        ext_states = trunc_states[0]
            
        b = np.argwhere(ext_states != 0)
        
        gap_index = b[0]+gap[0]
        
        band_gap = Energy[gap_index[0]]
        
        print "The band gap is", band_gap, "eV"
    else:
        print "Smearing is not Tetrahedron, cannot compute band gap" 
        
#Spin-resolved section   
elif ispin == 2:
     
    nodeList1 = tree.findall('./calculation/dos/total/array/set/set[@comment="spin 1"]/r')
    
    eigs = []
    dos = []
    
    for child in nodeList1:
        
        nodeValues = child.text.split(" ")
    
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[0])
        dos.append(nodeFloats[1])
    
    x1 = np.array(eigs)
    y1 = np.array(dos)
    
    ef = []
    
    for child in root.findall("./calculation/dos/i[@name='efermi']"):
        ef.append(child.text)
        
    efermi = float(ef[0])
    
    x_values1 = x1[0:nd]
    States1 = y1[0:nd]
    Energy1 = x_values1-efermi
    
    tdos1 = np.column_stack((Energy1,States1))
    
    with open('spin_1_tdos_shifted.txt', 'w') as f:
        csv.writer(f, delimiter=' ').writerows(tdos1)
    
    if ismear == -5:
        gap1 = np.where(Energy1>=0)
        
        trunc_states1 = []
        
        for value in gap1:
            trunc_states1.append(States1[value])
            
        ext_states1 = trunc_states1[0]
            
        b1 = np.argwhere(ext_states1 != 0)
        
        gap_index1 = b1[0]+gap1[0]
        
        band_gap1 = Energy1[gap_index1[0]]
        
        print "The spin 1 band gap is", band_gap1, "eV"
    else:
        print "Smearing is not Tetrahedron, cannot compute spin 1 band gap"
        
    #Now for the other spin
    nodeList2 = tree.findall('./calculation/dos/total/array/set/set[@comment="spin 2"]/r')
    
    eigs = []
    dos = []
    
    for child in nodeList2:
        
        nodeValues = child.text.split(" ")
    
        nodeFloats = []
        for nodeValue in nodeValues:
            if nodeValue != "":
                nodeFloats.append(float(nodeValue))
        eigs.append(nodeFloats[0])
        dos.append(nodeFloats[1])
    
    x2 = np.array(eigs)
    y2 = np.array(dos)
    
    x_values2 = x2[0:nd]
    States2 = y2[0:nd]
    Energy2 = x_values2-efermi
    
    tdos2 = np.column_stack((Energy2,States2))
    
    with open('spin_2_tdos_shifted.txt', 'w') as f:
        csv.writer(f, delimiter=' ').writerows(tdos2)
        
    if ismear == -5:     
        gap2 = np.where(Energy2>=0)
        
        trunc_states2 = []
        
        for value in gap2:
            trunc_states2.append(States2[value])
            
        ext_states2 = trunc_states2[0]
            
        b2 = np.argwhere(ext_states2 != 0)
        
        gap_index2 = b2[0]+gap2[0]
        
        band_gap2 = Energy2[gap_index2[0]]
        
        print "The spin 2 band gap is", band_gap2, "eV"
    else:
        print "Smearing is not Tetrahedron, cannot compute spin 2 band gap"
