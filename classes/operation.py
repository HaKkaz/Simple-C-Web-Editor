from typing import Literal

class Operation:
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