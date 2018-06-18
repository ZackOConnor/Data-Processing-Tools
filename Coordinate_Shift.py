import numpy as np
import pandas as pd

class Coordinate_Shift(object):

    def cart_to_polar(self, coordinates):
        coordinates['radius'] = np.sqrt(coordinates['y']*coordinates['y']+coordinates['x']*coordinates['x'])
        coordinates['theta'] = np.tan(np.divide(coordinates['y'],coordinates['x']))**-1
        return(coordinates)
    
    def cart_to_cycl(self,coordinates,z ='z',x='x',y='y'):
        coordinates['row'] = np.sqrt(coordinates[y]*coordinates[y]+coordinates[x]*coordinates[x])
        coordinates['theta'] = np.tan(np.divide(coordinates[y],coordinates[x]))**-1
        coordinates['z'] = np.[z]
        return(coordinates)
    
    def cart_to_sph(self,coordinates,z='z',x='x',y='y'):
        coordinates['radius'] = np.sqrt(coordinates[y]*coordinates[y]+coordinates[x]*coordinates[x]+coordinates[z]*coordinates[z])
        coordinates['theta'] = np.tan(np.divide(coordinates[y],coordinates[x]))**-1
        coordinates['phi'] = np.tan(np.true_divide(np.sqrt(coordinates[y]*coordinates[y]+coordinates[x]*coordinates[x]),coordinates[z]))**-1
        return(coordinates)  
    
    def polar_to_cart(self, coordinates):
        coordinates['x'] = np.multiply(coordinates['radius'],np.cos(coordinates['theta']))
        coordinates['y'] = np.multiply(coordinates['radius'],np.sin(coordinates['theta']))
        return(coordinates)
    
    def cycl_to_cart(self,coordinates):
        coordinates['x'] = np.multiply(coordinates['row'],np.cos(coordinates['theta']))
        coordinates['y'] = np.multiply(coordinates['row'],np.sin(coordinates['theta']))
        return(coordinates)
    
    def sph_to_cart(self, coordinates):
        coordinates['x'] = np.multiply(np.multiply(coordinates['radius'],np.sin(coordinates['phi'])),np.cos(coordinates['theta']))
        coordinates['y'] = np.multiply(np.multiply(coordinates['radius'],np.sin(coordinates['phi'])),np.sin(coordinates['theta']))
        coordinates['z'] = np.multiply(coordinates['radius'],np.cos(coordinates['phi']))
        return(coordinates)
    
    def sph_to_polar(self,coordinates):
        Coordinate_Shift.cart_to_polar(Coordinate_Shift.sph_to_cart(coordinates))
        return(coordinates)
    
    def polar_to_sph(self,coordinates):
        Coordinate_Shift.cart_to_sph(Coordinate_Shift.polar_to_cart(coordinates))
        return(coordinates)
    
    def polar_to_cycl(self,coordinates):
        Coordinate_Shift.cart_to_cycl(Coordinate_Shift.polar_to_cart(coordinates))
        return(coordinates)
    
    def cycle_to_polar(self,coordinates):
        Coordinate_Shift.cart_to_polar(Coordinate_Shift.cycle_to_cart(coordinates))
        return(coordinates)
    
    def sph_to_cycl(self,coordinates):
        Coordinate_Shift.cart_to_cycl(Coordinate_Shift.sph_to_cart(coordinates))
        return(coordinates)
    
    def cycl_to_sph(self,coordinates):
        Coordinate_Shift.cart_to_sph(Coordinate_Shift.cycl_to_cart(coordinates))
        return(coordinates)
