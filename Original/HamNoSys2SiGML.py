'''Copyright (c) <2019> <carolina neves>
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
(the "HamNoSys2SiGML"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, and/or sell copies of the merged or modified Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''


import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom 

#
#To run:
#   python HamNoSys2SiGML.py "hamnosysSymbols" ("glosses")
#												optional
# - If the user chooses to provide the glosses, the number of glosses must be equal to the number of HamNoSys symbols
# - Both the set of HamNoSys symbols and the glosses must be identified by their quotes
#
#	Ex:. python HamNoSyS2SiGML.py "hamnosyssymbol_GOOD hamnosyssymbol_MORNING" ("GOOD MORNING")
#


#Reads command line input and decodes the hamnosys characters
def readInput():
	global data, glosses_sigml, hasGlosses	
	
	# create the xml file structure	
	data = ET.Element('sigml')
	glosses_sigml = []

	inputContent = sys.argv[1:]

	if len(inputContent) > 1:					
		hasGlosses = True						#if the input has glosses
		hamnosysContent = inputContent[0].split(" ")
		glossesList = inputContent[1].split(" ")
	else:										
		hasGlosses = False						#if the input doesnt have glosses
		hamnosysContent = inputContent[0].split(" ")
	
	codesList = []
	for char in hamnosysContent:
		hamnosysCode = char.encode('unicode_escape').decode()	#decode the hamnosys characters
		hamnosysCode = hamnosysCode.replace("\\u", "")
		hamnosysCode = hamnosysCode.upper()
		codesList.append(hamnosysCode)


	if hasGlosses:
		codesList = readLists(glossesList, codesList)	
	else:
		codesList = readLists(None, codesList)


#Makes the association between the hamnosys codes received and their glosses (if received)
def readLists(glosses, codes):	
	if hasGlosses:
		glosses_hamnosys = [(glosses[i], codes[i]) for i in range(0, len(codes))]

		for i in range(0, len(glosses_hamnosys)):
			aux = hamnosysList(glosses_hamnosys[i][1])
			readCode(glosses_hamnosys[i][0], aux)
	else:
		glosses_hamnosys = [(None, codes[i]) for i in range(0, len(codes))]		
		count = 1
		for i in range(0, len(glosses_hamnosys)):
			aux = hamnosysList(glosses_hamnosys[i][1])

			readCode(count, aux)	
			count += 1

	writeSiGML(glosses_sigml)


#Separates hamnosys codes from each other
def hamnosysList(codes):
	hamnosys_list = []
	n = 4 		#each hamnosys code has 4 characters

	for j in range(0, len(codes), n):
		singleCode = codes[j:j+n]
		hamnosys_list.append(singleCode)

	return hamnosys_list


#Provides de association for hamnosys unicode to its sigml code
def readCode(gloss, hamnosys):
	conversionTXT = "conversionSpreadSheet.txt"		#txt file with association between sigml and hamnosys unicode codes
	sigmlList = []

	with open(conversionTXT, 'r') as f:
		for code in hamnosys:
			f.seek(0)
			for line in f:
				if code in line:
					fields = line.split(",")
					sigmlList.append(fields[0])
					break


	for i in range(0, len(sigmlList)):
		glosses_sigml.append((gloss, sigmlList[i]))


#Writes the sigml
def writeSiGML(thisdict):
	previousGloss = "null"

	for i in range(0, len(thisdict)):
		if(previousGloss == thisdict[i][0]):			#if the gloss is the same the hamnosys codes are added in the same component
			ET.SubElement(itemManual, thisdict[i][1])
		else:
			itemGloss = ET.SubElement(data, 'hns_sign')
			if(hasGlosses):
				itemGloss.set('gloss', thisdict[i][0])			
			
			itemNonManual = ET.SubElement(itemGloss, 'hamnosys_nonmanual')
			itemManual = ET.SubElement(itemGloss, 'hamnosys_manual')

			ET.SubElement(itemManual, thisdict[i][1])

		previousGloss = thisdict[i][0]

	dataStr = ET.tostring(data, encoding='unicode')
	dom = xml.dom.minidom.parseString(dataStr)
	aux = dom.toprettyxml(encoding='UTF-8').decode("utf-8")		#to be well indented
	sys.stdout.write(aux)


readInput()