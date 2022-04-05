import paramiko

host = "squirtle"
port = 22
username = "pi"
password = "r00t"

command = "cd Desktop; cat home.txt"


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command(command)
lines = stdout.readlines()
data = lines[0]
print(data)