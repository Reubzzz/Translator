# Program
 Reubens and Rowans Unity Program


8/06/22

Steps to use Program

Step 1: Download a .LAS File pointcloud from https://opentopography.org/

Step 2: Run the Program.py 

Step 3: Choose .LAS File 

Step 4: Name PointCloud File (example).ply

Step 5: Name Mesh File (Example).obj


Step 6: Run file into MeshLAB:

        In MeshLab run:

        Import (Example).obj

        Parametrization : Trivial per Triangle 
                            (Txt Dimentions = 8192)

        Transfer Vertext attributes to texture
                            (Set Height and Width to = 8192)

        Export as an OBJ


Step 7: In Blender run:

        Import: New.obj

        export: New.obj to new.fbx
                PathMode: = Copy
                Click box next to PathMode


Step 8: Import New asset into Unity.



Hints:

Locations of files will be where application is run from.
 
Non colored .LAS Files dont work. (Currently)


