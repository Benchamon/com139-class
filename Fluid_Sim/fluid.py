"""
Based on the Jos Stam paper https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games
and the mike ash vulgarization https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
https://github.com/Guilouf/python_realtime_fluidsim
"""
import numpy as np
import math


class Fluid:

    def __init__(self):
        self.rotx = 1
        self.roty = 1
        self.cntx = 1
        self.cnty = -1

        self.size = 60  # map size
        self.dt = 0.2  # time interval
        self.iter = 2  # linear equation solving iteration number

        self.diff = 0.0000  # Diffusion
        self.visc = 0.0000  # viscosity

        self.s = np.full((self.size, self.size), 0, dtype=float)        # Previous density
        self.density = np.full((self.size, self.size), 0, dtype=float)  # Current density

        # array of 2d vectors, [x, y]
        self.velo = np.full((self.size, self.size, 2), 0, dtype=float)
        self.velo0 = np.full((self.size, self.size, 2), 0, dtype=float)

    def step(self):
        self.diffuse(self.velo0, self.velo, self.visc)

        # x0, y0, x, y
        self.project(self.velo0[:, :, 0], self.velo0[:, :, 1], self.velo[:, :, 0], self.velo[:, :, 1])

        self.advect(self.velo[:, :, 0], self.velo0[:, :, 0], self.velo0)
        self.advect(self.velo[:, :, 1], self.velo0[:, :, 1], self.velo0)

        self.project(self.velo[:, :, 0], self.velo[:, :, 1], self.velo0[:, :, 0], self.velo0[:, :, 1])

        self.diffuse(self.s, self.density, self.diff)

        self.advect(self.density, self.s, self.velo)

    def lin_solve(self, x, x0, a, c):
        """Implementation of the Gauss-Seidel relaxation"""
        c_recip = 1 / c

        for iteration in range(0, self.iter):
            # Calculates the interactions with the 4 closest neighbors
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[2:, 1:-1] + x[:-2, 1:-1] + x[1:-1, 2:] + x[1:-1, :-2])) * c_recip

            self.set_boundaries(x)

    def set_boundaries(self, table):
        """
        Boundaries handling
        :return:
        """

        if len(table.shape) > 2:  # 3d velocity vector array
            # Simulating the bouncing effect of the velocity array
            # vertical, invert if y vector
            table[:, 0, 1] = - table[:, 0, 1]
            table[:, self.size - 1, 1] = - table[:, self.size - 1, 1]

            # horizontal, invert if x vector
            table[0, :, 0] = - table[0, :, 0]
            table[self.size - 1, :, 0] = - table[self.size - 1, :, 0]

        table[0, 0] = 0.5 * (table[1, 0] + table[0, 1])
        table[0, self.size - 1] = 0.5 * (table[1, self.size - 1] + table[0, self.size - 2])
        table[self.size - 1, 0] = 0.5 * (table[self.size - 2, 0] + table[self.size - 1, 1])
        table[self.size - 1, self.size - 1] = 0.5 * table[self.size - 2, self.size - 1] + \
                                              table[self.size - 1, self.size - 2]

    def diffuse(self, x, x0, diff):
        if diff != 0:
            a = self.dt * diff * (self.size - 2) * (self.size - 2)
            self.lin_solve(x, x0, a, 1 + 6 * a)
        else:  # equivalent to lin_solve with a = 0
            x[:, :] = x0[:, :]

    def project(self, velo_x, velo_y, p, div):
        # numpy equivalent to this in a for loop:
        # div[i, j] = -0.5 * (velo_x[i + 1, j] - velo_x[i - 1, j] + velo_y[i, j + 1] - velo_y[i, j - 1]) / self.size
        div[1:-1, 1:-1] = -0.5 * (
                velo_x[2:, 1:-1] - velo_x[:-2, 1:-1] +
                velo_y[1:-1, 2:] - velo_y[1:-1, :-2]) / self.size
        p[:, :] = 0

        self.set_boundaries(div)
        self.set_boundaries(p)
        self.lin_solve(p, div, 1, 6)

        velo_x[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * self.size
        velo_y[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * self.size

        self.set_boundaries(self.velo)

    def advect(self, d, d0, velocity):
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                tmp1 = dtx * velocity[i, j, 0]
                tmp2 = dty * velocity[i, j, 1]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5:
                    x = 0.5
                if x > (self.size - 1) - 0.5:
                    x = (self.size - 1) - 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0

                if y < 0.5:
                    y = 0.5
                if y > (self.size - 1) - 0.5:
                    y = (self.size - 1) - 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                try:
                    d[i, j] = s0 * (t0 * d0[i0i, j0i] + t1 * d0[i0i, j1i]) + \
                              s1 * (t0 * d0[i1i, j0i] + t1 * d0[i1i, j1i])
                except IndexError:
                    # tmp = str("inline: i0: %d, j0: %d, i1: %d, j1: %d" % (i0, j0, i1, j1))
                    # print("tmp: %s\ntmp1: %s" %(tmp, tmp1))
                    raise IndexError
        self.set_boundaries(d)

    def turn(self):
        self.cntx += 1
        self.cnty += 1
        if self.cntx == 3:
            self.cntx = -1
            self.rotx = 0
        elif self.cntx == 0:
            self.rotx = self.roty * -1
        if self.cnty == 3:
            self.cnty = -1
            self.roty = 0
        elif self.cnty == 0:
            self.roty = self.rotx
        return self.rotx, self.roty



def readconf(inst):
  c = 0
  color=""
  densities=[]
  velocities=[]
  pulsatingvel=[]
  rotatingvel=[]
  solids=[]
  
  with open("config.txt","r") as file:
    for line in file:
      line = line.strip()
      if(c == 0):
        color = line
      else:
        a, b = line.split(" ")
        if(a=='D'):
            n,m=b.split(",")
            na,nb=n.split(":")
            ma,mb=m.split(":")
            inst.density[int(na):int(nb),int(ma):int(mb)]+=100
            densities.append([na,nb,ma,mb])
        elif(a=='V'):
            s,d=b.split(":")
            sa,sb=s.split(",")
            da,db=d.split(",")
            inst.velo[int(sa),int(sb)] = [int(da),int(db)]
            velocities.append([sa,sb,da,db])
        elif(a=='PV'):
            s,d=b.split(":")
            sa,sb=s.split(",")
            da,db=d.split(",")
            inst.velo[int(sa),int(sb)] = [int(da),int(db)]
            pulsatingvel.append([sa,sb,da,db])
        elif(a=='RV'):
            s,d=b.split(":")
            sa,sb=s.split(",")
            da,db=d.split(",")
            inst.velo[int(sa),int(sb)] = [int(da),int(db)]
            rotatingvel.append([sa,sb,da,db])
        elif(a=='S'):
            n,m=b.split(",")
            na,nb=n.split(":")
            ma,mb=m.split(":")
            inst.density[int(na):int(nb),int(ma):int(mb)]=0
            inst.velo[int(na):int(nb),int(ma):int(mb)]=0
            solids.append([na,nb,ma,mb])


      c+=1
  file.close()
  return color, densities, velocities, pulsatingvel, rotatingvel, solids


def prevDenVel(frame, inst,den_array, vel_array, pvel_array, rvel_array, solids_array):
    for den in den_array:
        inst.density[int(den[0]):int(den[1]),int(den[2]):int(den[3])]+=100
    for vel in vel_array:
        inst.velo[int(vel[0]),int(vel[1])] = [int(vel[2]),int(vel[3])]
    for pvel in pvel_array:
        x=int(pvel[2])
        y=int(pvel[3])
        if(x>0 and y>0):
            a=math.atan(y/x)
        elif(x==0 and y>0):
            a=math.pi/2
        elif(x<0):
            a=math.atan(y/x)+math.pi
        elif(x==0 and y<0):
            a=3*math.pi/2
        elif(x>0 and y<0):
            a=math.atan(y/x)+2*math.pi
        r=math.sqrt(x**2 + y**2)
        r=r-r*((math.sin(frame)+1)/2)
        x=r*math.cos(a)
        y=r*math.sin(a)
        inst.velo[int(pvel[0]),int(pvel[1])] = [x,y]
    #Rotating
    for rvel in rvel_array:
        x=int(rvel[2])
        y=int(rvel[3])
        if(x>0 and y>0):
            a=math.atan(y/x)
        elif(x==0 and y>0):
            a=math.pi/2
        elif(x<0):
            a=math.atan(y/x)+math.pi
        elif(x==0 and y<0):
            a=3*math.pi/2
        elif(x>0 and y<0):
            a=math.atan(y/x)+2*math.pi
        r=math.sqrt(x**2 + y**2)
        a+=(frame*0.1)
        x=r*math.cos(a)
        y=r*math.sin(a)
        inst.velo[int(rvel[0]),int(rvel[1])] = [x,y]
    for sol in solids_array:
        inst.density[int(sol[0]):int(sol[1]),int(sol[2]):int(sol[3])]=0
        inst.velo[int(sol[0]):int(sol[1]),int(sol[2]):int(sol[3])]=0


def addSolids(fig, solids_array):
    for sol in solids_array:
        plt.gca().add_patch(Rectangle((int(sol[2]),int(sol[0])),int(sol[3])-int(sol[2]),int(sol[1])-int(sol[0]),fill=True,color='gray',alpha=0.5,zorder=1000,figure=fig))
        


if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        from matplotlib import animation
        from matplotlib.patches import Rectangle

        inst = Fluid()

        #Read config.txt
        col, den_array, vel_array, pvel_array, rvel_array, solids_array= readconf(inst)

        

        def update_im(i, den_array, vel_array, pvel_array, rvel_array, solids_array):
            # We add new density creators in here
            #inst.density[14:17, 14:17] += 100  # add density into a 3*3 square
            # We add velocity vector values in here
            #inst.velo[20, 20] = [-2, -2]
            prevDenVel(i, inst,den_array, vel_array, pvel_array, rvel_array, solids_array)
            inst.step()
            im.set_array(inst.density)
            q.set_UVC(inst.velo[:, :, 1], inst.velo[:, :, 0])
            # print(f"Density sum: {inst.density.sum()}")
            im.autoscale()

        fig = plt.figure()

        # plot density
        im = plt.imshow(inst.density, vmax=100, interpolation='bilinear', cmap=col)
        addSolids(fig, solids_array)
        # plot vector field
        q = plt.quiver(inst.velo[:, :, 1], inst.velo[:, :, 0], scale=10, angles='xy')
        anim = animation.FuncAnimation(fig, update_im, fargs=(den_array,vel_array,pvel_array,rvel_array, solids_array), interval=0, save_count=300)
        #anim.save("Video5.mp4", fps=30, extra_args=['-vcodec', 'libx264'])
        
        plt.show()

    except ImportError:
        import imageio

        frames = 30

        flu = Fluid()

        video = np.full((frames, flu.size, flu.size), 0, dtype=float)

        for step in range(0, frames):
            flu.density[4:7, 4:7] += 100  # add density into a 3*3 square
            flu.velo[5, 5] += [1, 2]

            flu.step()
            video[step] = flu.density

        imageio.mimsave('./video.gif', video.astype('uint8'))
