from typing import Literal

class Operation:
    """
    5 parameters:
    1. edt_actv = {INSERT, DELETE}
    2. var_name = the modified variable 
    3. op = {WRITE, READ, KILL}
    4. mod_node= id of the modified node 
    5. Order = the order of modified variable in mod_node
    """
    def __init__(
            self, 
            edt_actv: Literal['INSERT', 'DELETE'], 
            var_name: str, 
            op: Literal['WRITE', "READ", "KILL"], 
            mod_node: int, 
            Order: int
        ):
        self.edt_actv = edt_actv
        self.var_name = var_name
        self.op = op
        self.mod_node = mod_node
        self.Order = Order

    def to_dict(self):
        return {
            'edt_actv': self.edt_actv,
            'var_name': self.var_name,
            'op': self.op,
            'mod_node': self.mod_node,
            'Order': self.Order
        }