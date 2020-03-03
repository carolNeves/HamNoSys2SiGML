/*Copyright (c) <2019> <carolina neves>
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "RunPythonScripts"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, and/or sell copies of the merged or modified Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*/



using UnityEngine;
using System.Diagnostics;
using System.IO;

//Class which contains Python related functions
public class RunPythonScripts : MonoBehaviour {

    private string sigmlFilesPath = "/Assets/SiGML_Files/";
    private string pythonScriptsPath = "/Assets/PythonScripts/";


    //Checks if Python is installed -> if not installs it
    public void checkPythonInstallation(){
        ProcessStartInfo pythonVerify = new ProcessStartInfo();
        pythonVerify.FileName = "cmd.exe";
        pythonVerify.Arguments = "/C python --version";

        Process process = new Process();
        process.StartInfo = pythonVerify;
        process.StartInfo.RedirectStandardOutput = true;
        process.StartInfo.UseShellExecute = false;
        process.Start();

        string pythonVersion = process.StandardOutput.ReadToEnd();
        if (!pythonVersion.Contains("Python 3.7.3"))
        {
            ProcessStartInfo pythonInstall = new ProcessStartInfo();
            pythonInstall.FileName = "cmd.exe";
            string pathInstallation = Path.GetDirectoryName(UnityEngine.Application.dataPath) + "/Assets/PythonScripts" +
                "/PythonInstaller/python-3.7.3-amd64.exe";
            pythonInstall.Arguments = "/C " + pathInstallation;
            Process.Start(pythonInstall);
        }
    }

    
    public string runPythonScripts(string inputHTML, string finalOutput){
        //-------Run parser.py which receives ELAN html as input (inputHTML) and returns a .txt-------//
        string outputParser = "outputParser.txt";
        string inputParser = inputHTML + " " + Path.GetDirectoryName(UnityEngine.Application.dataPath) + pythonScriptsPath + outputParser;
        ProcessStartInfo processInfoParser = new ProcessStartInfo();
        processInfoParser.FileName = "cmd.exe";
        processInfoParser.WorkingDirectory = Path.GetDirectoryName(UnityEngine.Application.dataPath) + pythonScriptsPath;
        processInfoParser.Arguments = "/C py -3 parser.py " + inputParser;     // "/K" to keep command line open
        Process.Start(processInfoParser);

        //-------Run HamNoSys_SiGML.py which receives parser output (outputParser) and returns a .sigml-------//
        string outputFinal = Path.GetDirectoryName(UnityEngine.Application.dataPath) + sigmlFilesPath + finalOutput + ".sigml";
        string inputHSiGML = Path.GetDirectoryName(UnityEngine.Application.dataPath) + pythonScriptsPath + outputParser + " " +
            Path.GetDirectoryName(UnityEngine.Application.dataPath) + sigmlFilesPath + finalOutput + ".sigml";
        ProcessStartInfo processInfoHSiGML = new ProcessStartInfo();
        processInfoHSiGML.FileName = "cmd.exe";
        processInfoHSiGML.WorkingDirectory = Path.GetDirectoryName(UnityEngine.Application.dataPath) + pythonScriptsPath;
        processInfoHSiGML.Arguments = "/C py -3 HamNoSys_SiGML.py " + inputHSiGML;
        Process.Start(processInfoHSiGML);

        return outputFinal;
    }
}
