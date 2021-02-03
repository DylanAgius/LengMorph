# LengMorph
A tool to include length scale effects for crystal plasticity using slip distance.

# Usage
Firstly, there are a number of folders included here containing different tools. 
In **Additional File** the following folders exist:
* AbaqusFiles - includes *Example_UEXTERNALDB.for* which is an example of how to read in the created binary files at the start of an Abaqus analysis;
* Dream3d files - contains the example Dream3D pipeline (*example_supp.json*) to create the necessary data files fo the python function;
* FORTRAN program - contains *lengthscale_program.f90* which is an example fortan program which implements the length scale subroutine and can be used to get familiar with the intricacies of the inputs/outputs;
* Length scale subroutines - 
This tool can be used to construct the arrays required to implement the length scale modification in **ref** to include to include a size dependency in classical crystal plasticity simulations.  The data required for tool to work is extract from a Dream3d pipeline, the example of which is included in this repo.
## Outputs
Four binary files are constructed with the following names:
* boundfeat.bin
* el_centroid.bin
* xvalues.bin
* yvalues.bin
* zvalues.bin

Details on their contents can be found in the following publication **ref**.

## How to
Once installed, the tool can be run by specifying two detail:
1. the name of the files used in the Dream3D pipeline.  In this example case in the repo, this would be *testcase*
2. There is the option to increase the number of nodes defining boundary voxels/elements.  This can be selected by choosing *True* or *False*

```python
import PyLengMorph as plm
plm.grainboundary(loc='\\path\\to\\data\\folder', file='testcase', nodeinc=False, abq=True)
```

# Installation
Download the GitHub repo via the following link:

https://github.com/DylanAgius/LengMorph.git

Once unpacked, navigate to the PyLengMorph folder and use the following command:

`pip install .`
