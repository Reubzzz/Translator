
#libraries used
import numpy as np
import laspy 
import open3d as o3d
import PySimpleGUI as sg


# %%
#GUI for searching for file to read .LAS
sg.theme("DarkTeal2")
layout = [[sg.T("")], [sg.Text("Choose a folder: "), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-")],[sg.Button("Submit"),[sg.Button("Exit")]]]

###Building Window
window = sg.Window('My File Browser', layout, size=(600,150))

def Close():
        window.close()
        print(data)
  

while True:
    event, values = window.read()
    print(values["-IN2-"])
    if event == sg.WIN_CLOSED or event=="Exit":
        window.close()
        break
    elif event == "Submit":
        print(values["-IN-"])
        savedata = (values["-IN-"])
        data = values["-IN-"]
        Close()
        break
        

            



# %%
print (savedata)

# %%
#path set to .LAS File
dataname=data
point_cloud= laspy.read(dataname)

# %%

# Open a file in read mode:
inFile = point_cloud

# Grab a numpy dataset of our clustering dimensions:
dataset = np.vstack([inFile.X, inFile.Y, inFile.Z]).transpose()
colors = np.vstack([inFile.red, inFile.green, inFile.blue]).transpose()

#setting the colors of the pointcloud data to between 1 and 0
colors = colors / 255 / 255
colors = np.round(colors, 1)

print("the ponts")
print(dataset)
print("the colors")
print(colors)



# %%
# Pass xyz and RGB to Open3D.o3d.geometry.PointCloud 

pcd = o3d.geometry.PointCloud()

pcd.points = o3d.utility.Vector3dVector(dataset)

pcd.colors = o3d.utility.Vector3dVector(colors) 


pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

print (pcd)

print(np.all(np.isfinite(np.asarray(pcd.colors))))


# %%
#Creating the Triangles and Vertices For a Mesh.
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting (pcd, o3d.utility.DoubleVector([1,2,3,4]))




print("The Vertices")
print(np.asarray(mesh.vertices))
print("The Triangles")
print(np.asarray(mesh.triangles))
print("The Colors")
print(np.asarray(pcd.colors))
print("The Points")
print(np.asarray(pcd.points))

mesh = o3d.geometry.TriangleMesh.compute_triangle_normals (mesh)

# %%
#Shaping the quality of the mesh (Rendering)

mesh = mesh.filter_sharpen(number_of_iterations=1, strength=0.010)

# %%
#write .LAS file of PCD or PLY or PTS OR XYZRGB

o3d.io.write_point_cloud("./result.ply", pcd, write_ascii=False)

# %%
#Reading file of PCD or PLY or PTS OR XYZRGB

testing = o3d.io.read_point_cloud("./result.ply")
print(np.asarray(testing.points))
print(np.asarray(testing.colors))


# %%
#writing the .LAS to a mesh.
o3d.io.write_triangle_mesh("./meshes.ply", mesh)

# %%
#Reading the Mesh
testing = o3d.io.read_point_cloud("./meshes.ply")
print(np.asarray(testing.points))
print(np.asarray(testing.colors))


