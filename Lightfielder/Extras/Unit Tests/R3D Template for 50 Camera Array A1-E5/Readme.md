# Create a Symlinked R3D Sequence

This Fusion comp is used to generate a unit test for debugging 50 camera array geometry A1-E5 format R3D filenames.

A sample R3D file named "`Source.R3D`" is placed in the same folder as the .comp file. The comp then uses the Vonk data nodes to generate a sample filename sequence based upon the naming template in the file "`R3D File Sequence.ifl`":

```
A001_A050_0309BX_001.R3D
...
J001_E050_0309BX_001.R3D
```

