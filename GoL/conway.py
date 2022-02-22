
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from datetime import datetime
from tabulate import tabulate

ON = 255
OFF = 0
vals = [ON, OFF]
N = 100
M = 100
grid = np.array([])
Gen=200
genCount = 0
allGrid = np.zeros((200, 100, 100))





def menu():
  global grid
  global N
  global M
  global Gen
  global allGrid
  print("Choose an option")
  print("1) Default (100*100 random creation 200Gen)")
  print("2) Input size (random creation 200Gen)")
  print("3) Input size and #generations (ramdom creation)")
  print("4) Read from file")
  val = input()
  if(val == '1'):
    grid = randomGrid(N,M)
  elif(val == '2'):
    n = input("Enter x value")
    m = input("Enter y value")
    N = int(n)
    M = int(m)
    grid = randomGrid(N,M)
    allGrid = np.zeros((200, N, M))
  elif(val == '3'):
    print("Enter x value")
    n = input()
    print("Enter y value")
    m = input()
    print("Enter # of generations")
    g = input()
    Gen = int(g)
    N = int(n)
    M = int(m)
    grid = randomGrid(N,M)
    allGrid = np.zeros((Gen, N, M))
  elif(val == '4'):
    readconf()
  else:
    print("Inavlid input, please try again")
    menu()


def readconf():
  c = 0
  global grid
  global N
  global M
  global Gen
  global allGrid
  
  
  with open("config.txt","r") as file:
    for line in file:
      line = line.strip()
      #to read N and M dimensions
      if(c == 0):

        n, m = line.split(" ")
        N = int(n)
        M = int(m)
        grid = np.zeros(N*M).reshape(N, M)
      elif(c == 1):
        g = line
        Gen = int(g)
        allGrid = np.zeros((Gen, N, M))
        
      else:
        i, j = line.split(" ")
        i = int(i)
        j = int(j)
        grid[i,j]=255

      c+=1
  file.close()


def randomGrid(N, M):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid ):
	global genCount
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    #newGrid = grid.copy()
	newGrid = np.zeros(N*M).reshape(N, M)
	count=0
    # TODO: Implement the rules of Conway's Game of Life
	if(genCount < Gen):
		
		for i in range(1,N-1):
			for j in range(1,M-1):
				count =0
				if(grid[i-1,j-1] == 255):
					count +=1
				if(grid[i,j-1] == 255):
					count +=1
				if(grid[i+1,j-1] == 255):
					count +=1
				if(grid[i-1,j] == 255):
					count +=1
				if(grid[i+1,j] == 255):
					count +=1
				if(grid[i-1,j+1] == 255):
					count +=1
				if(grid[i,j+1] == 255):
					count +=1
				if(grid[i+1,j+1] == 255):
					count +=1
				if(grid[i,j]==255):
					if(count <2):
						newGrid[i,j] = 0
					if(count ==2 or count ==3):
						newGrid[i,j] = 255
					if(count >3):
						newGrid[i,j] = 0
				if(grid[i,j]==0):
					if(count ==3):
						newGrid[i,j] =255
		# update data
		img.set_data(newGrid)
		grid[:] = newGrid[:]
		allGrid[genCount,:,:] = newGrid[:]
	#close program if last gen reached
	else:
		#sys.exit()
		print('Creating report of all generations')
		validateFigures()


	genCount +=1
	return img,



def validateFigures():
  global allGrid
  global N
  global M
  global Gen
  ####################### glider #################### 
  
  glider1 = np.array([[0,   0,   0,   0, 0],
                    [0,   0,   0, 255, 0], 
                    [0, 255,   0, 255, 0], 
                    [0,   0, 255, 255, 0],
                    [0,   0,   0,   0, 0]])
  glider2 = np.array([[0,   0,   0,   0, 0],
                    [0, 255,   0, 255, 0], 
                    [0,   0, 255, 255, 0], 
                    [0,   0, 255,   0, 0],
                    [0,   0,   0,   0, 0]])
  glider3 = np.array([[0,   0,   0,   0, 0],
                    [0,   0, 255,   0, 0], 
                    [0,   0,   0, 255, 0], 
                    [0, 255, 255, 255, 0],
                    [0,   0,   0,   0, 0]])
  glider4 = np.array([[0,   0,   0,   0, 0],
                    [0, 255,   0,   0, 0], 
                    [0,   0, 255, 255, 0], 
                    [0, 255, 255,   0, 0],
                    [0,   0,   0,   0, 0]])
  ######################  L W spaceship ##############################
  
  LWS1 = np.array([[0,   0,   0,   0,   0,   0,   0],
                 [0, 255,   0,   0, 255,   0,   0], 
                 [0,   0,   0,   0,   0, 255,   0], 
                 [0, 255,   0,   0,   0, 255,   0],
                 [0,   0, 255, 255, 255, 255,   0],
                 [0,   0,   0,   0,   0,   0,   0]])
  LWS2 = np.array([[0,   0,   0,   0,   0,   0,   0],
                 [0,   0,   0, 255, 255,   0,   0], 
                 [0, 255, 255,   0, 255, 255,   0], 
                 [0, 255, 255, 255, 255,   0,   0],
                 [0,   0, 255, 255,   0,   0,   0],
                 [0,   0,   0,   0,   0,   0,   0]])
  LWS3 = np.array([[0,   0,   0,   0,   0,   0,   0],
                 [0,   0, 255, 255, 255, 255,   0], 
                 [0, 255,   0,   0,   0, 255,   0], 
                 [0,   0,   0,   0,   0, 255,   0],
                 [0, 255,   0,   0, 255,   0,   0],
                 [0,   0,   0,   0,   0,   0,   0]])
  LWS4 = np.array([[0,   0,   0,   0,   0,   0,   0],
                 [0,   0, 255, 255,   0,   0,   0], 
                 [0, 255, 255, 255, 255,   0,   0], 
                 [0, 255, 255,   0, 255, 255,   0],
                 [0,   0,   0, 255, 255,   0,   0],
                 [0,   0,   0,   0,   0,   0,   0]])
  ######################  blinker ##############################
  
  blinker1 = np.array([[0,   0,   0],
                 	 [0, 255,   0], 
                 	 [0, 255,   0], 
                 	 [0, 255,   0],
                 	 [0,   0,   0]])
  blinker2 = np.array([[0,   0,   0,   0,   0],
                 	 [0, 255, 255, 255,   0],
                 	 [0,   0,   0,   0,   0]])
  #################### Toad ############################
  toad1 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0,   0,   0, 255,   0,   0],
                 	 [0, 255,   0,   0, 255,   0],
                 	 [0, 255,   0,   0, 255,   0],
                 	 [0,   0, 255,   0,   0,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  toad2 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0,   0, 255, 255, 255,   0],
                 	 [0, 255, 255, 255,   0,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  ################### Beacon ######################
  beacon1 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0, 255, 255,   0,   0,   0],
                 	 [0, 255, 255,   0,   0,   0],
                 	 [0,   0,   0, 255, 255,   0],
                 	 [0,   0,   0, 255, 255,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  beacon2 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0, 255, 255,   0,   0,   0],
                 	 [0, 255,   0,   0,   0,   0],
                 	 [0,   0,   0,   0, 255,   0],
                 	 [0,   0,   0, 255, 255,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  ##################### Block #######################
  block1 = np.array([[0,   0,   0,   0],
                 	 [0, 255, 255,   0], 
                 	 [0, 255, 255,   0], 
                 	 [0,   0,   0,   0]])
  #################### Beehive ##################
  beehive1 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0,   0, 255, 255,   0,   0],
                 	 [0, 255,   0,   0, 255,   0],
                 	 [0,   0, 255, 255,   0,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  #################### Loaf ##################
  loaf1 = np.array([[0,   0,   0,   0,   0,   0],
                 	 [0,   0, 255, 255,   0,   0],
                 	 [0, 255,   0,   0, 255,   0],
                 	 [0,   0, 255,   0, 255,   0],
                 	 [0,   0,   0, 255,   0,   0],
                 	 [0,   0,   0,   0,   0,   0]])
  ##################### Boat ######################
  boat1 = np.array([[0,   0,   0,   0, 0],
                    [0, 255, 255,   0, 0], 
                    [0, 255,   0, 255, 0], 
                    [0,   0, 255,   0, 0],
                    [0,   0,   0,   0, 0]])
  ##################### Tub ######################
  tub1 = np.array([[0,   0,   0,   0, 0],
                    [0,   0, 255,   0, 0], 
                    [0, 255,   0, 255, 0], 
                    [0,   0, 255,   0, 0],
                    [0,   0,   0,   0, 0]])
  #open file
  now = datetime.today().strftime('%Y-%m-%d')
  file = open('output.txt','w')
  file.write('Simulation at {}\n'.format(now))
  file.write('Universe size {} x {}\n\n'.format(N, M))
  




  


  for g in range(0,Gen):
  	print('Analyzing gen {} of {}'.format(g+1,Gen))
  	total =0
  	cglider=0
  	cspaceship=0
  	cblink=0
  	ctoad=0
  	cbeacon = 0
  	cblock =0
  	cbee = 0
  	cloaf =0
  	cboat =0
  	ctub =0
  	for i in range(0,N):
  		for j in range(0,M):
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , glider1, equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider1), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider1, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider1, 3), equal_nan=True)):
  				cglider+=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , glider2, equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider2, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider2, 3), equal_nan=True)):
  				cglider+=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , glider3, equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider3), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider3, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider3, 3), equal_nan=True)):
  				cglider+=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , glider4, equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider4), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider4, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(glider4, 3), equal_nan=True)):
  				cglider+=1
  				total+=1
  			# Light weight spaceship
  			if(np.array_equal(allGrid[g, i:i+6, j:j+7] , LWS1, equal_nan=True) or np.array_equal(allGrid[g, i:i+7, j:j+6] , np.rot90(LWS1), equal_nan=True) or np.array_equal( allGrid[g, i:i+6, j:j+7] , np.rot90(LWS1, 2), equal_nan=True) or np.array_equal( allGrid[g, i:i+7, j:j+6] , np.rot90(LWS1, 3), equal_nan=True)):
  				cspaceship +=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+6, j:j+7] , LWS2, equal_nan=True) or np.array_equal(allGrid[g, i:i+7, j:j+6] , np.rot90(LWS2), equal_nan=True) or np.array_equal( allGrid[g, i:i+6, j:j+7] , np.rot90(LWS2, 2), equal_nan=True) or np.array_equal( allGrid[g, i:i+7, j:j+6] , np.rot90(LWS2, 3), equal_nan=True)):
  				cspaceship +=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+6, j:j+7] , LWS3, equal_nan=True) or np.array_equal(allGrid[g, i:i+7, j:j+6] , np.rot90(LWS3), equal_nan=True) or np.array_equal( allGrid[g, i:i+6, j:j+7] , np.rot90(LWS3, 2), equal_nan=True) or np.array_equal( allGrid[g, i:i+7, j:j+6] , np.rot90(LWS3, 3), equal_nan=True)):
  				cspaceship +=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+6, j:j+7] , LWS4, equal_nan=True) or np.array_equal(allGrid[g, i:i+7, j:j+6] , np.rot90(LWS4), equal_nan=True) or np.array_equal( allGrid[g, i:i+6, j:j+7] , np.rot90(LWS4, 2), equal_nan=True) or np.array_equal( allGrid[g, i:i+7, j:j+6] , np.rot90(LWS4, 3), equal_nan=True)):
  				cspaceship +=1
  				total+=1
  			# blinker
  			if(np.array_equal(allGrid[g, i:i+5, j:j+3] , blinker1, equal_nan=True) or np.array_equal(allGrid[g, i:i+3, j:j+5] , blinker2, equal_nan=True)):
  				cblink+=1
  				total+=1
  			#toad
  			if(np.array_equal(allGrid[g, i:i+6, j:j+6] , toad1, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(toad1), equal_nan=True)):
  				ctoad+=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+4, j:j+6] , toad2, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+4] , np.rot90(toad2), equal_nan=True)):
  				ctoad+=1
  				total+=1
  			# beacon
  			if(np.array_equal(allGrid[g, i:i+6, j:j+6] , beacon1, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(beacon1), equal_nan=True)):
  				cbeacon+=1
  				total+=1
  			if(np.array_equal(allGrid[g, i:i+6, j:j+6] , beacon2, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(beacon2), equal_nan=True)):
  				cbeacon+=1
  				total+=1
  			#block
  			if(np.array_equal(allGrid[g, i:i+4, j:j+4] , block1, equal_nan=True) ):
  				cblock+=1
  				total+=1
  			# beehive
  			if(np.array_equal(allGrid[g, i:i+5, j:j+6] , beehive1, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+5] , np.rot90(beehive1), equal_nan=True)):
  				cbee+=1
  				total+=1
  			# loaf
  			if(np.array_equal(allGrid[g, i:i+6, j:j+6] , loaf1, equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(loaf1), equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(loaf1, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+6, j:j+6] , np.rot90(loaf1, 3), equal_nan=True)):
  				cloaf+=1
  				total+=1
  			# boat
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , boat1, equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(boat1), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(boat1, 2), equal_nan=True) or np.array_equal(allGrid[g, i:i+5, j:j+5] , np.rot90(boat1, 3), equal_nan=True)):
  				cboat+=1
  				total+=1
  			# tub
  			if(np.array_equal(allGrid[g, i:i+5, j:j+5] , tub1, equal_nan=True) ):
  				ctub+=1
  				total+=1



  	#print(allGrid[0,:,:])

  	file.write('Iteration: {}\n'.format(g+1))
  	file.write('------------------------------------\n')
  	if(total!=0):
  		file.write(tabulate([['Block', cblock, cblock*100/total], ['Beehive', cbee, cbee*100/total], ['Loaf', cloaf, cloaf*100/total], ['Boat', cboat, cboat*100/total], ['Tub', ctub, ctub*100/total], ['Blinker', cblink, cblink*100/total], ['Toad', ctoad, ctoad*100/total], ['Beacon', cbeacon, cbeacon*100/total], ['Glider', cglider, cglider*100/total], ['LG sp ship', cspaceship, cspaceship*100/total]], headers=[' ','Count', 'Percent'], tablefmt='orgtbl'))
  	else:
  		file.write(tabulate([['Block', cblock, 0], ['Beehive', cbee, 0], ['Loaf', cloaf, 0], ['Boat', cboat, 0], ['Tub', cbee, 0], ['Blinker', cblink, 0], ['Toad', ctoad, 0], ['Beacon', cbeacon, 0], ['Glider', cglider, 0], ['LG sp ship', cspaceship, 0]], headers=[' ','Count', 'Percent'], tablefmt='orgtbl'))
  	file.write('\n')
  	file.write('------------------------------------\n')




  #end
  print('Output document ready!!!')
  file.close()
  sys.exit()




# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments     
    # set animation update interval
    updateInterval = 100

    menu()
    
    #addGlider(1,1,grid)
    #addGlider(60,80,grid)
    #addGlider(90,60,grid)
    
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
    main()
