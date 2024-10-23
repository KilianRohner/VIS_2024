import numpy as np

class Model:
    def __init__(self, iniState):
        self.state = iniState

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state

    def dydt(self, t, y):
        """Defines the system's dynamics: computes the derivative of the state vector."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SingleMassOscillator(Model):
    def __init__(self, iniState, m, k, d):
        super().__init__(iniState)
        #your implementation here
        self.m = m  # mass
        self.k = k  # spring constant
        self.d = 2*d*np.sqrt(self.k/self.m)  # damping coefficient


    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
               
        position = self.state[0]
        velocity = self.state[1]

        # Compute the acceleration using Newton's second law
        acceleration = (-self.k * position - self.d * velocity) / self.m

        # The derivative of position is velocity
        # The derivative of velocity is acceleration
        return np.array([velocity, acceleration]) 
        #----------------------------------------------------------------------------

