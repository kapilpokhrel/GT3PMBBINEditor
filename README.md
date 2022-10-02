# GT3PMBBINEditor

Simple tool for editing Gran Turismo 3 PMB.bin files, which are created by BTEST4HE's [GT3MBLPMBTools](https://github.com/BTEST4HE/GT3MBLPMBTools). It allows addition, removal, and to change the order of texture files inside the .bin.

## Running the Script
Standalone executables are provided inside the bins folder, you can just double click the executable to use the editor.  
If you wish to run the python script or the build the executable for youself then first you have to have python installer and you have to build the dependency with
```
pip install -r requirements.txt
```

To run the script, use
```
python main.py
```

To build the stand alone executable file for yourself, run the following command and you'll have the executable inside the dist folder.
```
pyinstaller -F -n "GT3PMBBINEditor" main.py
```

## Credits
- Misuka ミ ス カ - File format reverse engineering
- [kapilpokhrel](https://github.com/kapilpokhrel/) - Programming
- [BTEST4HE](https://github.com/BTEST4HE) - GT3MBLPMBTools creator