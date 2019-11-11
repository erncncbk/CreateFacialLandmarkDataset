
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add keys:value 
    def add(self, keys, value): 
        self[keys] = value 