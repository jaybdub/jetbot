import inspect

class Model(object):
    """A machine learning model."""
    
    def check_input(self, input: dict):
        """Checks whether the input is valid for the model
        
        This function checks whether an input dict is valid.  It may also perform
        data transformations in order to make the input valid if appropriate.
        The overloaded method is responsible for doing these checks, and
        returning the validated data, or throwing an error if the data is invalid.
        By default this method will simply pass through the input data as valid.
        """
        return input
        
    def check_output(self, output: dict):
        """Checks whether the output is valid for the model
        
        This function checks whether an output dict is valid.  It may also perform
        data transformations in order to make the output valid if appropriate.
        The overloaded method is responsible for doing these checks, and
        returning the validated data, or throwing an error if the data is invalid.
        By default this method will simply pass through the output data as valid.
        """
        return output
    
    def train(self, *args, **kwargs):
        """Trains the model using the current dataset state."""
        raise NotImplementedError
    
    def evaluate(self):
        """Evaluates the model using the current hyperparameters"""
        raise NotImplementedError
    
    def save(self):
        """Saves the model data and hyperparameters to the specified path."""
        raise NotImplementedError
    
    def load(self):
        """Loads the model data and hyperparameters from the specified path"""
        raise NotImplementedError
    
    def execute(self, input):
        """Executes the model on input data to perform output inference
        """
        raise NotImplementedError
    
    def __call__(self, input):
        input = self.check_input(input)
        output = self.execute(input)
        output = self.check_output(output)
        return output
        
    def insert(self):
        """Inserts a data sample into the model dataset"""
        raise NotImplementedError
    
    def remove(self):
        """Removes a sample from the model dataset"""
        raise NotImplementedError
    
    def __len__(self):
        """Returns the length of the model dataset"""
        raise NotImplementedError
    
    def __getitem__(self, idx):
        """Returns an item from the model dataset"""
        raise NotImplementedError