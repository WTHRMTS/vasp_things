# Author Jamie Booth
# This script takes the vasprun.xml file of a Time-Dependent DFT calculation as input.
# It outputs three text files
# 1. Real Part of the Dielectric Response as EP1.txt
# 2. Imaginary Part of the Dielectric Response as EP2.txt
# 3. Optical Transitions as Opt_Trans.txt


import xml.etree.ElementTree as etree
import csv

#Init some empty lists
EP1nodeValuesAsFloats = []
EP2nodeValuesAsFloats = []
OTnodeValuesAsFloats = []

tree = etree.parse('vasprun.xml')
root = tree.getroot()

#Pull out imaginary part of dielectric response and convert to float
EP1nodeList = tree.findall("./dielectricfunction/real/array/set/r")

for child in EP1nodeList:
    
    EP1nodeValues = child.text.split(" ")

    EP1nodeFloats = []
    for EP1nodeValue in EP1nodeValues:
        if EP1nodeValue != "":
            EP1nodeFloats.append(float(EP1nodeValue))
    EP1nodeValuesAsFloats.append(EP1nodeFloats)

#Write this matrix to a text file for easy plotting
with open('TDDFT_EPS1.txt', 'w') as f:
    csv.writer(f, delimiter=' ').writerows(EP1nodeValuesAsFloats)
   
#Same as above but for the real part of the dielectric response
EP2nodeList = tree.findall("./dielectricfunction/imag/array/set/r")

for child in EP2nodeList:
    
    EP2nodeValues = child.text.split(" ")

    EP2nodeFloats = []
    for EP2nodeValue in EP2nodeValues:
        if EP2nodeValue != "":
            EP2nodeFloats.append(float(EP2nodeValue))
    EP2nodeValuesAsFloats.append(EP2nodeFloats)

#Write this matrix to a text file for easy plotting
with open('TDDFT_EPS2.txt', 'w') as f:
    csv.writer(f, delimiter=' ').writerows(EP2nodeValuesAsFloats)

OTnodeList = root.findall("./varray[@name='opticaltransitions']/v")
#    data.append(child)
    
for child in OTnodeList:
    
    OTnodeValues = child.text.split(" ")

    OTnodeFloats = []
    for OTnodeValue in OTnodeValues:
        if OTnodeValue != "":
            OTnodeFloats.append(float(OTnodeValue))
    OTnodeValuesAsFloats.append(OTnodeFloats)

#Write this matrix to a text file for easy plotting
with open('TDDFT_Opt_Trans.txt', 'w') as f:
    csv.writer(f, delimiter=' ').writerows(OTnodeValuesAsFloats)
