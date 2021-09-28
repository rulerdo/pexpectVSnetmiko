from netmiko import ConnectHandler
import pexpect
import sys


def pe_show_command(device,command):

    enable_prompt = device["host"] + '#'
    ssh = pexpect.spawn(f'ssh -l {device["username"]} -p {device["port"]} {device["ip"]}',encoding='utf-8')

    # ssh.logfile_read = sys.stdout.buffer  # This line will show output while connecting
    
    ssh.expect('Password:')
    ssh.sendline(device["password"])
    ssh.expect_exact(enable_prompt)
    ssh.sendline(command)
    patterns = ['--More--', enable_prompt]
    result = str()

    while True:
        ret = ssh.expect(patterns)
        if ret == 0:
            result = result + ssh.before
            ssh.send(' ')
        elif ret == 1:
            result = result + ssh.before
            break
    
    ssh.close()

    return result


def nm_show_command(device,command):

    ssh = ConnectHandler(**device)
    result = ssh.send_command(command)
    ssh.disconnect()

    return result


if __name__ == '__main__':

    device  = {
            'device_type': 'cisco_ios',
            'ip': '10.88.255.98',
            'port': 22051,
            'username': 'admin',
            'password': 'admin',
            'host': 'c8000v_Flask',
        }

    
    print('\nTest device:')
    for k,v in device.items():
        print(k + ': ' + str(v))

    command = input('\nType your command: ')

    print('\nUsing PEXPECT')
    print('=====================\n')
    output = pe_show_command(device,command)
    print(output)

    print('\nUsing NETMIKO')
    print('=====================\n')
    output = nm_show_command(device,command)
    print(output)
