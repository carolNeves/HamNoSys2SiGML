'''Copyright (c) <2019> <carolina neves>
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
(the "parser"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, and/or sell copies of the merged or modified Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''


import io, sys, os
import xml.etree.ElementTree as ET

#
#To run:
#   python parser.py *inputfile_name*.html *outputfile_name*.txt
#
# - Reads ELAN file and saves the information defined
#



def readGlossesTable(output, root):
    maxCount = 0    #nr of glosses in each table
    for i in root.findall(".//*[@class='ti-0']"):   
        for j in i.findall("*[@colspan='1']"):             
            str = j.text
            if str:
                maxCount += 1
    count = 1
    read = True
    while(count <= maxCount):

        #Gloss
        #for with just one iteration -> in each table it only exist one class of this kind
        for i in root.findall(".//*[@class='ti-0']"):
            for j in i.findall("*[@colspan='1']"):             
                str = j.text
                if str:      
                    if read:      
                        glosses.append(str)             

                    if(maxCount!=1):
                        read = not read

        count += 1
        read = not read



def readCodesTable(output, root):
    maxCount = 0    #nr of hamnosys in each table
    for i in root.findall(".//*[@class='ti-1']"):
        for j in i.findall("*[@colspan='1']"):             
            str = j.text
            if str:
                maxCount += 1
    
    count = 1
    read = True
    while(count <= maxCount):

        #HamNoSys symbols
        #for with just one iteration -> in each table it only exist one class of this kind
        for i in root.findall(".//*[@class='ti-1']"):
            for j in i.findall("*[@colspan='1']"):
                str = j.text
                if str:    
                    if read:          
                        str = str.encode('unicode_escape').decode()
                        str = str.replace("\\u", "")
                        hmsymbols.append(str.upper())
                    if(maxCount!=1):
                        read = not read

        count += 1
        read = not read


def main():
    global root, outputfile, dictionary, glosses, hmsymbols
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    glosses_hamnosys = {}
    glosses = []
    hmsymbols = []

    inputfile = open(inputfile, "r", encoding='utf-8')
    file = open("aux_file.html", "w+", encoding='utf-8') 
    for line in inputfile:
        if "nbsp;" in line: 
            line = ""
        file.write(line)        #file = inputfile but without "nbps;" (which create errors)
    inputfile.close() 

    file.seek(0)
    tree = ET.parse(file)     
    root = tree.getroot()
    doc = ET.tostring(root, encoding='utf-8').decode('utf8')


    with io.open(outputfile, 'a') as output:
        for j in root.findall(".//td/table"):
            readGlossesTable(output, j)
            readCodesTable(output, j)

        #Create the association between the glosses read and their hamnosys codes
        for i in range(0, len(glosses)):
            glosses_hamnosys[glosses[i]] = hmsymbols[i]

        #Write hamnosys symbols in .txt
        output.write('"')
        for key in glosses_hamnosys:
        	output.write(glosses_hamnosys[key] + " ")
        output.write('" ')

        #Write glosses in .txt
        output.write('"')
        for key in glosses_hamnosys:
        	output.write(key + " ")
        output.write('"')

    file.close()
    os.remove("aux_file.html") 
    print('SUCESSFUL')

main()