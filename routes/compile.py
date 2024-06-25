from flask import request, jsonify
from classes.operation import Operation
from classes.node import OperationNode
from __main__ import app
import re

variable_pattern = r'\b[a-zA-Z_]\w*\b'
operator_pattern = r'[=+\-*/]'

variables = {} # {var_name: line_id}
vars = []

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data['content']

    opt_nodes: list[OperationNode] = []
    
    CurNode = OperationNode()
    lines = code.split('\n')
    for i in range(len(lines)):
        

        # Find all variables (words starting with a letter or underscore)
        line_variables = re.findall(variable_pattern, lines[i])

        # Find all operators (characters that are operators)
        line_operators = re.findall(operator_pattern, lines[i])

        # simple statement should contain a assignment operator
        if len(line_variables) > 0 and line_operators[0] != '=':
            return jsonify({'status': 'error', 'content': f'Syntax error: Line: {i} Expected assignment operator'})

        written_variable = line_variables[0]

        for j in range(len(line_variables)-1, 0, -1):
            if line_variables[j] in vars:
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=line_variables[j], 
                        op='READ', 
                        mod_node=len(opt_nodes),
                    )
                )
                variables[line_variables[j]] = i
                vars.append(line_variables[j])

        print("vars:", vars)
        print("kill", written_variable)
        #if written_variable in vars:
        CurNode.add_operation(
            Operation(
                edt_actv='INSERT', 
                var_name=written_variable, 
                op='KILL', 
                mod_node=len(opt_nodes),
            )
        )
        variables[written_variable] = i
        CurNode.add_operation(
            Operation(
                edt_actv='INSERT', 
                var_name=line_variables[0], 
                op='WRITE', 
                mod_node=len(opt_nodes),
            )
        )
        vars.append(line_variables[0])
    
    # with open('operations.txt', 'w') as f:
    #     for operation in :
    #         f.write(str(operation.to_tuple()) + '\n')

    opt_nodes.append(CurNode)
    for operation in opt_nodes[0].operations:
        print(operation.to_tuple())

    return jsonify({'status': 'success', 'content': ''.join(lines)})

