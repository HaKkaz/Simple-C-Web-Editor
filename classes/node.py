class OperationNode:
    def __init__(self):
        self.operations = []
        self.id = 0
    
    def add_operation(self, operation):
        self.operations.append(operation)