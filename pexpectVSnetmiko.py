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
    ssh.expect_exact(enable_prompt)
    result = ssh.before
    ssh.close()

    return result


def nm_show_command(device,command):

    ssh = ConnectHandler(**device)
    result = ssh.send_command(command)
    ssh.disconnect()

    return result


if __name__ == '__main__':

    c8000v  = {
            'device_type': 'cisco_ios',
            'ip': '10.88.255.98',
            'port': 22051,
            'username': 'admin',
            'password': 'admin',
            'host': 'c8000v_Flask',
        }

    print('\nTesting device:')
    for k,v in c8000v.items():
        print(k + ': ' + str(v))

    print('\nUsing PEXPECT')
    print('=====================\n')
    output = pe_show_command(c8000v,'show ip int brief')
    print(output)

    print('\nUsing NETMIKO')
    print('=====================\n')
    output = nm_show_command(c8000v,'show ip int brief')
    print(output)
