# Create a Symlinked R3D Sequence

This Fusion comp is used to generate a unit test for debugging 55 camera array geometry A110-Z579 format R3D filenames.

A sample R3D file named "`Source.R3D"` is placed in the same folder as the .comp file. The comp then uses the Vonk data nodes to generate a sample filename sequence based upon the naming template in the file "`R3D File Sequence.ifl`":

```
A110_A050_0619BX_001.R3D
...
Z579_E050_0619BX_001.R3D
```
