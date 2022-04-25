To run the program you need a file named "config.txt"
The first line must be a cmap compatible with the colormaps in Matplotlib https://matplotlib.org/3.5.0/tutorials/colors/colormaps.html
All of the following lines can be used to add densities, vectors or solids.
To add a solid you must type "S" followed by the area where you want the object. ex; "S 5:26,29:30"
To add a density is the same process as a solid but with a "D" instead of the "S". ex; "D 25:35,20:28"
There are 3 types of vectors; 
Normal vectors: "V" (Constant vector)
Pulsating vectors: "PV"
Rotating Vectors: "RV"

To declare a normal or pulsating vector you need the coordenates and the direction.
Keep in mind that the direction must be given as if the position of the vector was 0,0. ex; "PV 25,5:1,3"

To declare a rotating vector you need the position and a starting direction(this acts as the power as well). ex; "RV 30,50:2,2"
All rotating vectors rotate in a clockwise direction.

Examples of the code running:

Video 1:
https://user-images.githubusercontent.com/63068119/165022205-81b6046a-ffdf-433e-8ff5-c724c9dc5e9e.mp4


Video 2:
https://user-images.githubusercontent.com/63068119/165022197-1315cbf8-78b4-489b-801e-ce103abe933d.mp4


Video 3:
https://user-images.githubusercontent.com/63068119/165022222-e602581f-2d59-4800-a1ad-bf3dbd34b4de.mp4


Video 4:
https://user-images.githubusercontent.com/63068119/165022230-53f05eb9-f1da-4a0e-87c8-17a04fea999d.mp4


Video 5:
https://user-images.githubusercontent.com/63068119/165022242-ce26bddd-c458-4cc0-82a7-4fa5489b0d3c.mp4


