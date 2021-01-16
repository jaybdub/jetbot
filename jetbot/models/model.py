class Model(object):
    
    def inputs(self):
        """Gets the schema describing the format of input data to the model"""
        raise NotImplementedError
    
    def outputs(self):
        """Gets the schema describing the format of output data to the model"""
        raise NotImplementedError
    
    def train(self):
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
    
    def execute(self, data):
        """Executes the model on input data to perform output inference"""
        raise NotImplementedError
    
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