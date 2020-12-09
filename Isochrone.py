# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:09:12 2020

@author: cedri
"""
#imports
import numpy as np
import functionsIsochrone as f
import matplotlib.pyplot as plt

class Isochrone:
    def __init__(self, initr,  b, vmult = 1):
        self.b = b
        self.initr = initr
        self.vmult = vmult
        
        

        
    def runLeapfrog(self, dt, tmax, printBool = False, printLim = None):
        
        #plotArray indexing:
        #0    1 2 3 4  5  6  7  8  9  10 11 12 13 14 15
        #time x y z vx vy vz ax ay az Lx Ly Lz E  KE PE
        self.plotArray = []
        for i in range(16):
            self.plotArray.append([])
            
        self.rundt = None
        self.runtmax = None
        
        x, v = f.calculateInit(self.initr, self.b, self.vmult)
        

        a=f.getAcceleration(x,self.b)
        
        if printBool:
            print('Initial position x,y,z = ',x)
            print('Initial velocity x,y,z = ',v)
            print('Initial accelern x,y,z = ',a)  
        
        self.plotArray[0].append(0.)
        
        #store init
        for i in range(1,4):
            self.plotArray[i].append(x[i-1])
        
        for i in range(4,7):
            self.plotArray[i].append(v[i-4])
        
        for i in range(7,10):
            self.plotArray[i].append(a[i-7])
            
        initEnergy = [f.getKineticEnergy(x,v),f.getPotentialEnergy(x, self.b)]
        initAngMom = f.getAngularMomentum(x,v)
        
        for i in range(10, 13):
            self.plotArray[i].append(initAngMom[i-10])
        
        self.plotArray[13].append(initEnergy[0]+initEnergy[1])
        self.plotArray[14].append(initEnergy[0])
        self.plotArray[15].append(initEnergy[1])
 
        
            
        step = 1
        time = 0
        
        columnHeader = 'Step    t       x      y      z       vx      vy     vz    Lx      Ly    Lz       E      KE      PE'
        
        if printBool:
            print(columnHeader)


        if printLim is None:
            printCounter = 1
        else: 
            printCounter = printLim

        #LOOP STEP BEGINS HERE
        while (time<=tmax):
            localxva = f.step_leapfrog(x,v,a,dt,self.b)
            x = localxva[0]
            v = localxva[1]
            a = localxva[2]
            time = float(step)*dt
            step += 1
            
            angMom = f.getAngularMomentum(x, v)
            energy = [f.getKineticEnergy(x,v),f.getPotentialEnergy(x,self.b)]
            
            
            
            if printBool and printCounter > 0:
                print('%.4d %.5f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f' % (step,time,localxva[0][0],localxva[0][1],localxva[0][2],localxva[1][0],localxva[1][1],localxva[1][2], angMom[0], angMom[1], angMom[2], energy[0]+energy[1], energy[0], energy[1]))
                if printLim is not None:
                    printCounter -= 1
            
            self.plotArray[0].append(time)
            
            for i in range(1,4):
                self.plotArray[i].append(localxva[0][i-1])
        
            for i in range(4,7):
                self.plotArray[i].append(localxva[1][i-4])
        
            for i in range(7,10):
                self.plotArray[i].append(localxva[2][i-7])
                
                    
            for i in range(10, 13):
                self.plotArray[i].append(angMom[i-10])
            
            self.plotArray[13].append(energy[0]+energy[1])
            self.plotArray[14].append(energy[0])
            self.plotArray[15].append(energy[1])
     
                
        
        if printBool:
            print(columnHeader)
        
        self.rundt = dt
        self.runtmax = tmax
    
    def charToIndex(self, char):
        if char == "t" or char == "time":
            return 0
        elif char == "x":
            return 1
        elif char == "y":
            return 2
        elif char == "z":
            return 3        
        elif char == "vx":
            return 4   
        elif char == "vy":
            return 5
        elif char == "vz":
            return 6        
        elif char == "ax":
            return 7        
        elif char == "ay":
            return 8        
        elif char == "az":
            return 9      
        elif char == "lx" or char == "Lx":
            return 10    
        elif char == "ly" or char == "Ly":
            return 11    
        elif char == "lz" or char == "Lz":
            return 12    
        elif char.upper() == "E":
            return 13    
        elif char.upper() == "KE":
            return 14    
        elif char.upper() == "PE":
            return 15            
        else:
            raise Exception("inputted char is not valid")
        
    #xvar: character string for x variable
    #yvar: character string for y variable
    #equal: whether to make equal the grid spacing
    #legend: display legend? Note, if plotting multiple yvars, calling this on the last
            #call to plot() is sufficient
    #endPlot: by default, this is True, and will terminate the 'instance' of this plot
            #calling plot() again will start a new plot with a new set of axis
            #if set to False, it allows calling plot() again to add more y variables
            #to the same set of axis
            #
            #note: make sure that the x variables are the same, otherwise unpredictable
            #things will happen
    def plot(self, xvar, yvar, equal = False, legend = False, endPlot = True, legendLabel = None):
        if legendLabel is None:
            legendLabel = yvar
        plt.plot(self.plotArray[self.charToIndex(xvar)],self.plotArray[self.charToIndex(yvar)], label = legendLabel)
        plt.xlabel(xvar)
        plt.ylabel(yvar)
        plt.title(xvar+' vs '+yvar+' , dt == '+str(self.rundt)+' , b == '+str(self.b)+', tmax == '+str(np.round(self.runtmax, 3))+', initr == '+str(self.initr)+', vmult== '+str(self.vmult))
        if equal:
            plt.axis('equal')
        if legend:
            plt.legend()
        plt.grid()
        if endPlot:
            plt.show()



#vohfive = Isochrone(1., 0.1, 0.5)
#vohfive.runLeapfrog(0.001, 10.*np.pi)
#vohfive.plot('x','y',True)

#vohone = Isochrone(1., 0.1, 0.1)
#vohone.runLeapfrog(0.001, 10.*np.pi)
#vohone.plot('x','y',True)

#vohohone = Isochrone(1., 0.1, 0.01)
#vohohone.runLeapfrog(0.001, 10.*np.pi)
#vohohone.plot('x','y',True)

#voneone= Isochrone(1., 0.1, 1.1)
#voneone.runLeapfrog(0.001, 10.*np.pi)
#voneone.plot('x','y',True)

#vonefour= Isochrone(1., 0.1, 1.4)
#vonefour.runLeapfrog(0.001, 10.*np.pi)
#vonefour.plot('x','y',True)




