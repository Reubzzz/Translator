# %%
#libraries used
import numpy as np
import laspy 
import open3d as o3d
import PySimpleGUI as sg
import trimesh



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

print("THE POINTS")
print(dataset)
print("THE COLORS")
print(colors)



# %%
# Pass xyz and RGB to Open3D.o3d.geometry.PointCloud 

pcd = o3d.geometry.PointCloud()

pcd.points = o3d.utility.Vector3dVector(dataset)

pcd.colors = o3d.utility.Vector3dVector(colors) 

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))


print (pcd)



# %%
#write .LAS file of PCD or PLY or PTS OR XYZRGB
print ("EXPORTING PLY TO FILE")

# Creating Name for pointcloud Window


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Name of PointCloud'), sg.InputText(key="name")],
            [sg.Button('Ok'), sg.Button('Close Window')]
]

# Create the Window
window = sg.Window('Test', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    elif event == "Ok":
        print('Name of PointCloud will be:' + (values['name']) + '.ply')
        print(values['name'])  # get the content of multiline via its unique key
        pointname=(values['name'])
       
window.close()

print (pointname)

o3d.io.write_point_cloud( "./" + pointname + ".ply", pcd, write_ascii=False)

print ("DONE")




#Reading file of PCD or PLY or PTS OR XYZRGB
print ("PREPARING PLY TO BECOME MESH")

testingPointCloud = o3d.io.read_point_cloud("./" + pointname + ".ply")
print(np.asarray(testingPointCloud.points))
print(np.asarray(testingPointCloud.colors))

print ("DONE")

#Creating the Triangles and Vertices For a Mesh.
print ("NORMALS BEING ESTIMATED")

testingPointCloud.estimate_normals()

print ("DONE")


# estimate radius for rolling ball

print ("PIVIOTING THE POINTCLOUD")
distances = testingPointCloud.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist   
# 1.5 original  3 is best

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
           testingPointCloud,
           o3d.utility.DoubleVector([radius, radius * 2]))
print ("DONE")

# create the triangular mesh with the vertices and faces from open3d
print ("CREATING TRIANGLES")
tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),vertex_colors = np.asarray(mesh.vertex_colors),
                          vertex_normals=np.asarray(mesh.vertex_normals),write_triangle_uvs=True)

trimesh.convex.is_convex(tri_mesh)

print (tri_mesh)
print ("DONE")

print ("EXPORTING TO OBJ")


# Creating Name for OBJECT Window


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Name of Meshfile'), sg.InputText(key="objname")],
            [sg.Button('Ok'), sg.Button('Close Window')]
]

# Create the Window
window = sg.Window('Test', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    elif event == "Ok":
        print('Object name will be:' + (values['objname']) + '.obj' )
        print(values['objname'])  # get the content of multiline via its unique key
        objectname=(values['objname'])
window.close()

print (objectname)



trimesh.exchange.export.export_mesh(tri_mesh,"./" + objectname + ".obj")

Finish_mesh = o3d.io.read_triangle_mesh("./" + objectname + ".obj", True)
print ("DONE")

print ("CURRENT DATA")
print (Finish_mesh)
print ("VISULIZING")
o3d.visualization.draw_geometries([Finish_mesh])



