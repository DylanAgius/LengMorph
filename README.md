# LengMorph
A tool to include length scale effects for crystal plasticity using slip distance

# Usage
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
from Lengthmorph.fileconstruct import grainboundary
grainboundary(file='testcase',nodinc=True)
```

# Installation
Download the GitHub repo via the following link:

https://github.com/DylanAgius/LengMorph.git

Once unpacked, navigate to the LengMorph folder and use the following command:

`pip install .`
