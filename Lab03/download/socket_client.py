import socket

HOST = "192.168.128.1"  # The server's hostname or IP address
PORT = 80            # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.settimeout(1) # timeout 1s

	while True:
		try:
			buffer = b''
			while b'\r\n' not in buffer:
				data = s.recv(1024)
				buffer += data
			# print(buffer)
			st = buffer.decode('utf-8')
			l = st.split('\r\n')
			# print(l)
			print('Received', l[0])#(data.decode('utf-8')))#[2:].replace("\r\n", "\n"))
		except KeyboardInterrupt:
			exit()
		except:
			pass
