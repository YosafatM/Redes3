import paramiko, getpass, time
from flask import Flask

devices = {
  'R4': {
    'ip': "10.0.1.254"
  }
}

commands = [
  "config t\n"
  "ip route 10.0.5.0 255.255.255.0 10.0.2.253\n",
  "router rip\n",
  "no auto-summary\n",
  "version 2\n",
  "network 10.0.0.0\n"
  "router ospf 1\n",
  "network 10.0.4.0 0.0.0.255 area 0\n",
  "exit\n",
  "router rip\n",
  "redistribute rip\n",
  "redistribute ospf 1 metric 12\n",
  "router ospf 1\n",
  "redistribute static metric 200 subnets\n",
  "redistribute rip metric 200 subnets\n"
  "exit\n"
]

max_buffer = 2**14

def clear_buffer(connection):
  if connection.recv_ready():
    return connection.recv(max_buffer)
	  

app = Flask(__name__)

@app.route("/configurar")
def configurar():
	username = input ("Usuario: ")
	password = getpass.getpass("Password: ")

	for device in devices.keys():
	  outputFilename = device + "_salida.txt"
	  connection = paramiko.SSHClient()
	  connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	  connection.connect(devices[device]["ip"], username=username, password=password, look_for_keys=False, allow_agent=True)
	  new_connection = connection.invoke_shell()
	  output = clear_buffer(new_connection)
	  time.sleep(2)
	  new_connection.send("Terminal length 0\n")
	  output = clear_buffer(new_connection)
	  with open(outputFilename, "wb") as f:
	    for command in commands:
	      new_connection.send(command)
	      time.sleep(2)
	      output = new_connection.recv(max_buffer)
	      print(output)
	      f.write(output)
