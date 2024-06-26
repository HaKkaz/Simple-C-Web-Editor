from flask import request, jsonify
from __main__ import app

@app.route('/detect', methods=['POST'])
def detect_code():
    data = request.get_json()
    code = data['content']
    lines = code.split('\n')

    error_messages = ""

    with open('error.txt', 'r') as f:
        data = f.read().split('\n')
        for line in data:
            error_data = line[1:len(line)-1:].replace(' ', '').split(',')
            if len(error_data) != 4:
                continue
            errorplace = []
            with open('error_place_map.txt', 'r') as ff:
                temp = ff.read().split('\n')
                for place_map in temp:
                    errorplace.append(place_map.split('|'))
            for i in range(len(errorplace)):
                if errorplace[i][0] == error_data[2]:
                    first_place = errorplace[i][1]
                    first_minor_place = errorplace[i][2]
                if errorplace[i][0] == error_data[3]:
                    second_place = errorplace[i][1]
                    second_minor_place = errorplace[i][2]
            if error_data[0] == 'CNA1':
                #KILL - READ
                first_error = 'KILL'
                second_error = 'READ'
            if error_data[0] == 'CNA2':
                #KILL - KILL
                first_error = 'KILL'
                second_error = 'KILL'
            if error_data[0] == 'CNA3':
                #WRITE - KILL
                first_error = 'WRITE'
                second_error = 'KILL'
            if error_data[0] == 'CNA4':
                #WRITE - WRITE
                first_error = 'WRITE'
                second_error = 'WRITE'
            
            error_messages += f'Data flow anomaly occur when variable {error_data[1]} {first_error} in line {first_place} {first_minor_place}'
            error_messages += f' and {second_error} in line {second_place} {second_minor_place}\n'
            print(error_messages)
    
    return jsonify({'status': 'success', 'content': ''.join(lines), 'error_messages': error_messages})
