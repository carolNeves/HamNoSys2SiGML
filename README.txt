Copyright (c) <2019> <carolina neves>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "HamNoSys2SiGML"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the merged or modified Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



HamNoSys2SiGML is an automation system designed to receive a set of HamNoSys codes with the optional addition of its respective glosses, in said order, and return its SiGML.

Requirements:
*python 3.7.3


Our tool receives HamNoSys symbols. Optionally, the user can also provide their respective glosses. If so, the number of glosses must be equal to the number of HamNoSys symbols. The input must be identified by their quotes.

To run:
   python HamNoSys2SiGML.py "hamnosysSymbols" ("glosses")

   Ex:. python HamNoSyS2SiGML.py "hamnosyssymbol_GOOD hamnosyssymbol_MORNING" ("GOOD MORNING")
   *in brackets are the input which optionally. the brackets should not be included in the input	

The user also can extend the notation by adding the created HamNoSys codes and respective SiGMLs in the conversionSpreadSheet.txt.


parser.py: The parser developed is prepared to read an HTML exported from ELAN with two tiers (Glosses and HamNoSys respectively). If the user wishes to read a different input, for example a different number of tiers, this parser requires the appropriate adjustments.

RunPythonScripts.cs: The python scripts to be saved in a folder "PythonScripts" within the Unity Assets folder. The output from the the parser.py will also be saved in this same folder. The sigml output will be also be saved within the Unity Assets folder, but in the folder "SiGML_Files". 


For a more detailed description: https://www.aclweb.org/anthology/2020.lrec-1.739/
