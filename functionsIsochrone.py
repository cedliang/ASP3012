# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:45:43 2020

@author: cedri
"""
import numpy as np



def getAcceleration(x,b):
    return a_isochrone(x,b)


def a_isochrone(x,b):
    rmag=np.sqrt(np.dot(x,x))
    
    c = np.sqrt(rmag**2 + b**2)
    
    factor = (-1./(c*((b+c)**2)))
    
  
    
    a = factor * x
    
    return a

def vcirc(x,b):
    rmag=np.sqrt(np.dot(x,x))
    c = np.sqrt(rmag**2 + b**2)
    
    
    vc = np.sqrt((rmag**2)/(c*((b+c)**2)))
    return vc

    
#input position, velocity, (current) acceleration and dt
def step_leapfrog(x,v,a,dt,b):
    v += 0.5*dt*a
    x += dt*v
    a = getAcceleration(x,b) #update acceleration
    v += 0.5*dt*a
    return x,v,a #return updates position, velocity and acceleration




def getAngularMomentum(positionVec, velocityVec):
    return np.cross(positionVec, velocityVec)

#return KE, PE
def getKineticEnergy(positionVec, velocityVec):
    KE = 0.5*np.dot(velocityVec, velocityVec)
    
    return KE

def getPotentialEnergy(xvec, b):
    rmag=np.sqrt(np.dot(xvec,xvec))
    
    PE = -1./(b+np.sqrt((b**2) + (rmag**2)))
    
    return PE



def calculateInit(r,b, vmult):
    initx = np.array([r, 0, 0])
    initv = np.array([0, vmult*vcirc(initx, b), 0])
    
    return initx, initv