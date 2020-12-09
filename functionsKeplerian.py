# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:45:43 2020

@author: cedri
"""
import numpy as np



def getAcceleration(x):
    r2=np.dot(x,x)
    r=np.sqrt(r2)
    r3=r2*r
    a=x*(-1./r3)
    return a
#output is a = acceleration
    
#input position, velocity, (current) acceleration and dt
def step_leapfrog(x,v,a,dt):
    v += 0.5*dt*a
    x += dt*v
    a = getAcceleration(x) #update acceleration
    v += 0.5*dt*a
    return x,v,a #return updates position, velocity and acceleration

def getAngularMomentum(positionVec, velocityVec):
    return np.cross(positionVec, velocityVec)

#return KE, PE
def getEnergy(positionVec, velocityVec):
    KE = 0.5*np.dot(velocityVec, velocityVec)
    r2 = np.dot(positionVec, positionVec)
    r = np.sqrt(r2)
    PE = -1./r
    
    return KE, PE