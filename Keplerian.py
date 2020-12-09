# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:09:12 2020

@author: cedri
"""
#imports
import numpy as np
import functionsKeplerian as f
import matplotlib.pyplot as plt

class Keplerian:
    def __init__(self, eccentricity):
        self.e = eccentricity
        

        
    def runLeapfrog(self, dt, tmax, printBool = False, printLim = None):
        
        #plotArray indexing:
        #0    1 2 3 4  5  6  7  8  9  10 11 12 13 14 15
        #time x y z vx vy vz ax ay az Lx Ly Lz E  KE PE
        self.plotArray = []
        for i in range(16):
            self.plotArray.append([])
            
        self.rundt = None
        self.runtmax = None
        
        
        
        x=np.array([1.0-self.e, 0.0, 0.0])
        v=np.array([0.0, np.sqrt((1.0+self.e)/(1.0-self.e)), 0.0])
        a=f.getAcceleration(x)
        
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
            
        initEnergy = f.getEnergy(x,v)
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
            localxva = f.step_leapfrog(x,v,a,dt)
            x = localxva[0]
            v = localxva[1]
            a = localxva[2]
            time = float(step)*dt
            step += 1
            
            angMom = f.getAngularMomentum(x, v)
            energy = f.getEnergy(x,v)
            
            
            
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
        plt.title(xvar+' vs '+yvar+' , dt == '+str(self.rundt)+' , e == '+str(self.e)+', tmax == '+str(self.runtmax))
        if equal:
            plt.axis('equal')
        if legend:
            plt.legend()
        plt.grid()
        if endPlot:
            plt.show()



#fullCircle = Keplerian(0.)
#fullCircle.runLeapfrog(0.02, 6.*np.pi, True)
#fullCircle.plot('t','x')
#fullCircle.plot('x','y',True)
#fullCircle.plot('x','vx')


#ohNineNine = Keplerian(0.99)
#ohNineNine.runLeapfrog(0.0001, 4.*np.pi)
#ohNineNine.plot('x','y',True)
#ohNineNine.plot('x','vx')
#ohNineNine.plot('y','vy')
        
ohSeven = Keplerian(0.7)
ohSeven.runLeapfrog(0.01, 10.*np.pi)
ohSeven.plot('t','PE', endPlot = False)
ohSeven.plot('t','E', endPlot = False)
ohSeven.plot('t','KE', legend = True, endPlot = True)



