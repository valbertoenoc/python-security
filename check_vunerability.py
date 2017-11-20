import optparse
import socket
from datetime import datetime

from pymongo import MongoClient

# database/collection initialization
client = MongoClient('localhost', 27017)
db = client.Hosts 
records = db.records

def db_generateId(ip, port):
	''' generate an unique ID for database from IP address and PORT '''
	return ip.replace('.', '') + str(port)

def checkPort(ip, port):
	''' attempts to connect to a host on a specifc port '''
	try:
		socket.setdefaulttimeout(2)

		s = socket.socket()
		s.connect((ip, port))
		response = s.recv(1024)
		return response
	except:
		return


def checkVunerability(ip='127.0.0.1', ports=[21, 22, 25, 80, 110, 443]):
	''' verifies some common ports if it's open for vunerability purposes'''

	for port in ports:
		print 'connecting on: ' + ip + ':' + str(port)
		response = checkPort(ip, port)

		if response:
			ID = db_generateId(ip, port)

			print ip + ':' + str(port) + ' open'
			data = {'ID': ID, 'ip': ip, 'port': port, 'response': response, \
				'access time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


			db_insert(data)

	hosts = records.find({'ID': ID})
	for h in hosts:
		print h

def db_insert(data):
	''' inserts data into database after verifying if already exists, if so, updates 
	only the access time '''
	r = records.find({'ID': data['ID']})

	if r:
		records.update_one({'ID': data['ID']}, \
			{'$set': {'access time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
	else:
		records.insert_one(data)

def main():
	''' The main objective of the application is to verify which ports are
	open on a given host. Host IP is a string, ports is a list of integers.'''
	parser = optparse.OptionParser('usage: -H <target host> -p <target ports>')
	parser.add_option('-H', dest='arg_host', type='string', help='specify target host')
	parser.add_option('-p', dest='arg_ports', type='string', help='specify target ports')

	(options, args) = parser.parse_args()

	host = options.arg_host
	ports = map(int, str(options.arg_ports).split(','))

	checkVunerability(host, ports)

if __name__ == '__main__':
	main()
