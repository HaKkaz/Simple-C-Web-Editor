from typing import Literal
from dataclasses import dataclass

@dataclass
class Operation:
    edt_actv: Literal['INSERT', 'DELETE'] 
    var_name: str 
    op: Literal['WRITE', "READ", "KILL"]
    mod_node: int | None = None
    Order: int | None = None

    def to_dict(self):
        return {
            'edt_actv': self.edt_actv,
            'var_name': self.var_name,
            'op': self.op,
            'mod_node': self.mod_node,
            'Order': self.Order
        }
    
    def to_tuple(self):
        return (self.edt_actv, self.var_name, self.op, self.mod_node, self.Order)