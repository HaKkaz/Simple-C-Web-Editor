class OperationNode:
    def __init__(self):
        self.operations = []
        self.id = 0
    
    def add_operation(self, operation):
        self.operations.append(operation)
        # self.operations[-1].Order = len(self.operations)-1