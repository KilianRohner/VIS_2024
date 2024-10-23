import model

class Solver:
    def __init__(self, model2Solve):
        if not isinstance(model2Solve, model.Model):
            raise TypeError("Expected an instance of model or its subclass.")
        self.__model__ = model2Solve

    def step(self, t, dt):
        """Should be implemented in derived classes."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class SolverExplicit(Solver):
    def __init__(self, model2Solve):
        super().__init__(model2Solve)

    def step(self, t, dt):
        
        """Perform one step of numerical integration."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
    
        #Get the current state of the system
        current_state = self.__model__.get_state()

        # Compute the derivative (velocity and acceleration) at the current time
        derivative = self.__model__.dydt(t)

        # Update the state using Euler's method
        new_state = current_state + dt * derivative

        # Set the new state in the model
        self.__model__.set_state(new_state)
        #----------------------------------------------------------------------------
        
class SolverImplicit(Solver):
    def __init__(self, model2Solve):
        super().__init__(model2Solve)

    def step(self, t, dt):
        
        """Perform one step of numerical integration."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
        
        #----------------------------------------------------------------------------
        
