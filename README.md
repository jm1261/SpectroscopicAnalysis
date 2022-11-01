# GMRPeakfFinder

Created by Josh Male on 31/10/2022 as part of an ongoing analysis of Epsilon-Near-Zero materials. Code is under MIT-License for free use.

## Table of Contents

* [General Information](#general-information)
* [Package Requirements](#package-requirements)
* [Launch](#launch)
* [Setup](#setup)

## General Information

Automatic peak finder built using Python3 to find resonant wavelengths in 1D and 2D resonant cavities. Suitable for all fano-resonance structures.

## Package Requirements

Language and package requirements can also be found in requirements.txt. The code was built using the following languages and module versions.

* Python 3.6 onwards (f-strings) [3.10 used]
* tk 0.1.0
* numpy 1.21.4
* matplotlib 3.5.0
* scipy 1.7.2

## Launch

This code can be run from any terminal or editor. File to launch is experimental_peakfinder.py, others are functions. Requires the use of info.json file for non-windows operating system.

info.json must contain the following for non-windows operating systems:

* {
    "Directory Path": /path/to/data/directory,
    "Results Path": /path/to/results/directory,
    "Background Path": /path/to/background/directory
}
* Where all paths to directory are user dependent


## Setup