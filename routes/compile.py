from flask import request, jsonify
from classes.operation import Operation
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

    operations: list[Operation] = []
    
    lines = code.split('\n')
    for i in range(len(lines)):
        # Find all variables (words starting with a letter or underscore)
        line_variables = re.findall(variable_pattern, lines[i])

        # Find all operators (characters that are operators)
        line_operators = re.findall(operator_pattern, lines[i])

        print()
        print(line_variables)
        print(line_operators)
        print()

        # simple statement should contain a assignment operator
        if len(line_variables) > 0 and line_operators[0] != '=':
            return jsonify({'status': 'error', 'content': f'Syntax error: Line: {i} Expected assignment operator'})

        order_id = 0
        if line_variables[0] in vars:
            operations.append(
                Operation(
                    edt_actv='INSERT', 
                    var_name=line_variables[0], 
                    op='KILL', 
                    mod_node=i, 
                    Order=order_id
                )
            )
            variables[line_variables[0]] = i
            order_id += 1
        
        for j in range(1, len(line_variables)):
            if line_variables[j] in vars:
                operations.append(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=line_variables[j], 
                        op='READ', 
                        mod_node=i, 
                        Order=order_id
                    )
                )
                variables[line_variables[j]] = i
                vars.append(line_variables[j])
                order_id += 1
        

        operations.append(
            Operation(
                edt_actv='INSERT', 
                var_name=line_variables[0], 
                op='WRITE', 
                mod_node=i, 
                Order=order_id
            )
        )
        vars.append(line_variables[0])
    
    with open('operations.txt', 'w') as f:
        for operation in operations:
            f.write(str(operation.to_dict()) + '\n')

    return jsonify({'status': 'success', 'content': ''.join(lines)})