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
{% include googleDrivePlayer.html id=1BABBCKGn34PggsBdyMrSexeXV5VK6Wgu/preview %}


Video 2:



Video 3:



Video 4:



Video 5:


