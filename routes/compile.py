from flask import request, jsonify
from classes.operation import Operation
from classes.node import OperationNode
from __main__ import app
import re

decision_pattern = ['if', 'else', 'while', 'for']
variable_pattern = r'\b[a-zA-Z_]\w*\b'
operator_pattern = r'[=+\-*/]'

variables = {} # {var_name: line_id}
vars = []

@app.route('/compile', methods=['POST'])
def compile_code():
    ff = open("error_place_map.txt", "w")
    data = request.get_json()
    code = data['content']

    opt_nodes: list[OperationNode] = []
    
    CurNode = OperationNode()
    lines = code.split('\n')
    node_number = 0
    node_order = 0
    decision = False
    if_it_is_for_loop = False
    change = False
    for i in range(len(lines)):

        # Find all variables (words starting with a letter or underscore)
        line_variables = re.findall(variable_pattern, lines[i])

        # Find all operators (characters that are operators)
        line_operators = re.findall(operator_pattern, lines[i])

        # simple statement should contain a assignment operator
        #if len(line_variables) > 0 and line_operators[0] != '=':
        #    return jsonify({'status': 'error', 'content': f'Syntax error: Line: {i} Expected assignment operator'})
        if len(line_variables) == 0:
            if lines[i][0] == '{':
                node_number += 1
                node_order = 0
            if lines[i][0] == '}':
                change = True
            continue
        #print('line_variables:', line_variables)   
        if line_variables[0] in decision_pattern:
            if line_variables[0] != 'else':
                if i != 0:
                    node_number += 1
                    node_order = 0
                decision = True
                if line_variables[0] == 'for':
                    if_it_is_for_loop = True
            change = False
            line_variables.pop(0)
            if len(line_variables) == 0:
                continue
        #print('node_number', node_number)
        written_variable = line_variables[0]
        # decision not include else
        if change and not decision:
            change = False
            node_number += 1
            node_order = 0
        

        #print("vars:", vars)
        #print("kill", written_variable)
        #if written_variable in vars:
        if decision:
            if if_it_is_for_loop:
                for_text = lines[i][lines[i].find('(')+1:lines[i].find(')'):]
                for_init = for_text.split(';')
                first = re.findall(variable_pattern, for_init[0])
                if first[0] == 'int':
                    first.pop(0)
                if len(first) > 1:
                    for j in range(len(first)-1,0,-1):
                        CurNode.add_operation(
                            Operation(
                                edt_actv='INSERT', 
                                var_name=first[j], 
                                op='READ', 
                                mod_node=node_number,
                                Order=node_order
                            )
                        )
                        ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop initial-expression part'+'\n')
                        node_order += 1
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=first[0], 
                        op='KILL', 
                        mod_node=node_number,
                        Order=node_order
                    )
                )
                ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop initial-expression part'+'\n')
                node_order += 1
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=first[0], 
                        op='WRITE', 
                        mod_node=node_number,
                        Order=node_order
                    )
                )
                ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop initial-expression part'+'\n')
                node_order += 1
                second = re.findall(variable_pattern, for_init[1])
                for j in reversed(range(len(second))):
                    CurNode.add_operation(
                        Operation(
                            edt_actv='INSERT', 
                            var_name=second[j], 
                            op='READ', 
                            mod_node=node_number,
                            Order=node_order
                        )
                    )
                    ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop condition-expression part'+'\n')
                    node_order += 1
                third = re.findall(variable_pattern, for_init[2])
                if len(third) > 1:
                    CurNode.add_operation(
                        Operation(
                            edt_actv='INSERT', 
                            var_name=third[1], 
                            op='READ', 
                            mod_node=node_number,
                            Order=node_order
                        )
                    )
                    ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop loop-expression part'+'\n')
                    node_order += 1
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=third[0], 
                        op='READ', 
                        mod_node=node_number,
                        Order=node_order
                    )
                )
                ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop loop-expression part'+'\n')
                node_order += 1
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=third[0], 
                        op='KILL', 
                        mod_node=node_number,
                        Order=node_order
                    )
                )
                ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop loop-expression part'+'\n')
                node_order += 1
                CurNode.add_operation(
                    Operation(
                        edt_actv='INSERT', 
                        var_name=third[0], 
                        op='WRITE', 
                        mod_node=node_number,
                        Order=node_order
                    )
                )
                ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+'for loop loop-expression part'+'\n')
                node_order += 1
                if_it_is_for_loop = False
            else:
                for j in reversed(range(len(line_variables))):
                    CurNode.add_operation(
                        Operation(
                            edt_actv='INSERT', 
                            var_name=line_variables[j], 
                            op='READ', 
                            mod_node=node_number,
                            Order=node_order
                        )
                    )
                    ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+line_variables[j]+'\n')
                    node_order += 1
            decision = False
        else:
            for j in range(len(line_variables)-1, 0, -1):
                if line_variables[j] in vars:
                    CurNode.add_operation(
                        Operation(
                            edt_actv='INSERT', 
                            var_name=line_variables[j], 
                            op='READ', 
                            mod_node=node_number,
                            Order=node_order
                        )
                    )
                    ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+line_variables[j]+'\n')
                    node_order += 1
                    variables[line_variables[j]] = i
                    vars.append(line_variables[j])
            CurNode.add_operation(
                Operation(
                    edt_actv='INSERT', 
                    var_name=written_variable, 
                    op='KILL', 
                    mod_node=node_number,
                    Order=node_order
                )
            )
            ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+written_variable+'\n')
            node_order += 1
            variables[written_variable] = i
            CurNode.add_operation(
                Operation(
                    edt_actv='INSERT', 
                    var_name=line_variables[0], 
                    op='WRITE', 
                    mod_node=node_number,
                    Order=node_order
                )
            )
            ff.write(str(node_number)+':'+str(node_order)+'|'+str(i+1)+'|'+line_variables[0]+'\n')
            node_order += 1
            vars.append(line_variables[0])
    
    opt_nodes.append(CurNode)
    previous_node = 0
    with open('operations.txt', 'w') as f:
        for operation in opt_nodes[0].operations:
            #print(operation.to_tuple())
            if operation.mod_node != previous_node:
                f.write('\n')
                previous_node = operation.mod_node
            f.write(str(operation.to_tuple()) + '\n')
            
    ff.close()
    return jsonify({'status': 'success', 'content': ''.join(lines)})

