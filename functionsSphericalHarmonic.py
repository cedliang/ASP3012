# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:45:43 2020

@author: cedri
"""
import numpy as np



def getAcceleration(x,omega):
    return a_sphericalharmonic(x,omega)


def a_sphericalharmonic(x,omega):
        
    a = -1.*(omega**2)*x
    
    return a

def vcirc(x,omega):
    rmag=np.sqrt(np.dot(x,x))
    
    vc = rmag * omega
    
    return vc

    
#input position, velocity, (current) acceleration and dt
def step_leapfrog(x,v,a,dt,omega):
    v += 0.5*dt*a
    x += dt*v
    a = getAcceleration(x,omega) #update acceleration
    v += 0.5*dt*a
    return x,v,a #return updates position, velocity and acceleration




def getAngularMomentum(positionVec, velocityVec):
    return np.cross(positionVec, velocityVec)

#return KE, PE
def getKineticEnergy(positionVec, velocityVec):
    KE = 0.5*np.dot(velocityVec, velocityVec)
    
    return KE

def getPotentialEnergy(xvec, omega):
    rmag=np.sqrt(np.dot(xvec,xvec))
    
    PE = (-1./2)* (omega**2)*(rmag**2)
    
    return PE



def calculateInit(r,omega, vmult):
    initx = np.array([r, 0, 0])
    initv = np.array([0, vmult*vcirc(initx, omega), 0])
    
    return initx, initv