# NASA ChemCam Data Compilers
## Overview

### Introduction
This repository consists of two Python programs that intake [directories of data](https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/) produced by [NASA's Curiosity Rover ChemCam instrument](https://mars.nasa.gov/msl/spacecraft/instruments/chemcam/) and compiles all relevant information into CSV files that can be given to [The Sequencer](http://sequencer.org/documentation) so that patterns may be identified.

NASA's ChemCam tool consists of a laser, camera, and spectrogram that  work together to identify the chemical and mineral composition of rocks and soil on Mars. The Sequencer is an algorithm designed to automatically find patterns in datasets. It does this by reordering the dataset to produce the most elongated manifold describing the database's similarities.

### Program 1:
Each time ChemCam's laser vaporizes a rock surface, light (or radiance) is produced, and ChemCam's spectrometer divides that light into wavelengths. So, every time a rock surface is vaporized, the amount of light for every wavelength 240 nm - 906 nm is recorded in a file following this naming convention: cl5\*ccs\*.csv. When recording the amount of light 30 to 150 snapshots of the light are taken, and an average radiance for each wavelength is calculated. avgRadianceCompiler.py is designed to compile the average radiance per wavelength from every relevant file in the directory given. This program will output the compiled average radiance and one other file containing a list of the wavelengths light has been recorded for. The order of the rows in the compiled average radiance file is the same order in which the spectral data was taken (using space clock time). 

Note: This program “process” the data so that it is compatible with the Sequencer. All data is shifted up so the minimum value is 1.

### Program 2:
For every rock surface vaporized by ChemCam’s laser, there is another relevant file. This file contains the "Concatenated Multivariant Oxides Composition" (MOC) of the rock, and many other rocks across a range of days (sols). Each file records the amount of SiO2, TiO2, Al2O3, FeOT, MgO, CaO, Na2O, K2O and MnO that each rock is predicted to have as a weighted percentage, and the file follows this naming convention: moc\*.csv. mocCompiler.py is designed to compile the MOC data from every relevant file in the directory given. This program will output the compiled file and one other file which contains a list of numbers: each number corresponding to an oxide in the order they were listed above. The order of the rows in the compiled MOC file is the same order in which the spectral data was taken (using space clock time). 

Note: This program “process” the data so that it is compatible with the Sequencer. All data is shifted up so the minimum value is 1.

## Requirements
* Linux OS
* Python3 Interpreter
* Pandas 2.0.3
```
sudo apt install python3
pip install pandas==2.0.3
```

## Installation

### From this Repository
Clone the repository to your computer with the below command. This creates a `ChemCamDataCompliers` directory containing the relevant files on your computer. 
```
git clone https://codeberg.org/MatthewKing/ChemCamDataCompliers.git --depth 1
```
Move into this directory to prepare for the next steps with:
```cd ChemCamDataCompliers```

### Local copy of ChemCam data
To run either Python program in this repository you will have to already have a local copy of the relevant ChemCam data. You can 1) download everything, or 2) download a small subset for testing purposes. 

(1) You can download only the entire data set (~80GB, only Radiance and MOC) with:
```
wget -m -np -R "index.html*" -A "cl5*ccs*.csv" https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/
wget -m -np -R "index.html*" -A "moc*.csv" https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/
```
(2) Or, you can download only part of ChemCam's database (~250MB ) with:
```
wget -m -np -R "index.html*" -A "cl5_39*ccs*.csv" https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/
wget -m -np -R "index.html*" -A "moc*.csv" https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/
```
To rename this directory to something more descriptive and delete the junk we don't need: 
``` 
mv pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/data/ spectraMocDataSets spectraMocDataset
rm -rf pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/
```


## Usage
Please ensure that you are still in the ChemCamDataCompliers directory. Currently both programs can be run as follows (However, they are missing mandatory arguments, and the program will ask for them):
```
python3 avgRadianceCompiler.py
python3 mocCompiler.py
```
Here is a sample run compatible with everything done up to this point (includes the mandatory arguments):
```
python3 avgRadianceCompiler.py spectraMocDataset 0 5000 compiledSpectral.csv wavelengths.csv
python3 mocCompiler.py spectraMocDataset compiledMoc.csv oxideNumbers.csv
```
### Here is an explanation of the mandatory arguments for both programs

#### avgRadianceCompiler

1) Input Path: This is the relative or absolute path to the directory this program will compile files from (this is what you downloaded during the "Local copy of ChemCam data" step). 
2) Start file: This is the file the program will start compiling from. If for instance, the program crashes before it finishes compiling, you can simply start from the last file it got to. 
3) Cache Every X Files: Again, if this program is killed before it can finish comping, the cashing feature can save every X files so that they do not have to re-compiled. It is recommended to cache every 5000 or 10000 files. 
4) Name for Compiled Spectra File: This is the name (or path) to the first file this program will output. This is the compiled average radiance values from all of the files downloaded. Be sure to include ".csv" at the end. 
5) Name of the wavelengths file: This is the name (or path) to the second file this program will output. This is a list of all the wavelengths of light for which radiance values where recorded by ChemCam. Again, be sure to include ".csv" at the end of the file name. 

#### avgMocCompiler

1) Input Path: This is the relative or absolute path to the directory this program will compile files from (this is what you downloaded during the "Local copy of ChemCam data" step). 
2) Name for Compiled MOC File: This is the name (or path) to the first file this program will output. This is the compiled Major Oxide Composition (MOC) from all of the files downloaded. Be sure to include ".csv" at the end. 
3) Name of the Oxide Number's file: This is the name (or path) to the second file this program will output. This is just a small list of numbers each corresponding to a major oxide: SiO2, TiO2, Al2O3, FeOT, MgO, CaO, Na2O, K2O and MnO. Again, be sure to include ".csv" at the end of the file name. 

## Compiling LaTeX Documents

To complete the following steps, you must first insure that [LaTeX](https://www.latex-project.org/) is installed on your computer. Also confirm that you have [latexmk](https://mg.readthedocs.io/latexmk.html) installed to make the presentation.

### The Research Paper
Please follow these commands:
```
cd Paper
pdflatex MatthewKing_ResearchPaper.tex
biber MatthewKing_ResearchPaper
pdflatex MatthewKing_ResearchPaper.tex
open MatthewKing_ResearchPaper.pdf
```

### The Slide Show
Please follow these commands:
```
cd Presentation
latexmk -xelatex MatthewKing_SlideShow.tex
latexmk -c
```

## Conclusion
Now your compiled files have been created and saved. You can now reference [The Sequencer’s GitHub](https://github.com/dalya/Sequencer) if you want to sequence the data to identify patterns. Note: The Sequencer is most compatible with Linux, and you must downgrade the networkx package to version 2.4 with the below commands (their requirements.txt file is currently inaccurate).
```
pip uninstall networkx
pip install networkx==2.4
```

## License
This project uses a GNU General Public License v3. For more information, please look at the LICENSE file in this repository.
