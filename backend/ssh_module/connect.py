from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()

# Known_host policy
client.set_missing_host_key_policy(AutoAddPolicy())

# There is the connection to remote server. Enter path to public ssh key
client.connect('mongodb.tech', username='ubuntu',  key_filename='/home/vadim/.ssh/id_rsa.pub')


stdin, stdout, stderr = client.exec_command("sudo ls", get_pty=True)
print(type(stdin))
print(type(stdout))
print(type(stderr))

# Print output of command. Will wait for command to finish.
print(f'STDOUT: {stdout.read().decode("utf8")}')
print(f'STDERR: {stderr.read().decode("utf8")}')

# Get return code from command (0 is default for success)
print(f'Return code: {stdout.channel.recv_exit_status()}')

# Because they are file objects, they need to be closed
stdin.close()
stdout.close()
stderr.close()

# Close the client itself
client.close()
