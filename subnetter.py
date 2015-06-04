#!/usr/bin/python3


#################################
# programmed by Florian Schauer #
#################################


def ip2number(raw_ip):


	ip_in_numbers = 0
	
	#First Octet
	dot1 = raw_ip.find(".")
	ip_in_numbers = ip_in_numbers + int(raw_ip[:dot1]) * (2 ** 24)
	raw_ip = raw_ip[(dot1 + 1): ]
	
	#Second Octet
	dot2 = raw_ip.find(".")
	ip_in_numbers = ip_in_numbers + int(raw_ip[:dot2]) * (2 ** 16)
	raw_ip = raw_ip[(dot2 + 1): ]
	
	#Third Octet
	dot3 = raw_ip.find(".")
	ip_in_numbers = ip_in_numbers + int(raw_ip[:dot3]) * (2 ** 8)
	raw_ip = raw_ip[(dot3 + 1): ]
	
	#Last Octet
	ip_in_numbers = ip_in_numbers + int(raw_ip)
	
	return ip_in_numbers

def number2ip(number): 
	first_octet = int(number / (2 ** 24))
	number -= first_octet * (2 ** 24)
	
	second_octet = int(number / (2 ** 16))
	number -= second_octet * (2 ** 16)
	
	third_octet = int(number / (2 ** 8))
	number -= third_octet * (2 ** 8)
	
	last_octet = int(number)
	
	return str(first_octet) + "." + str(second_octet) + "." + str(third_octet) + "." + str(last_octet)

def iprange(iprange):
	start = int(ip2number(iprange[:iprange.find("/")]))
	
	cdr = int(iprange[(iprange.find("/") +1) :])
	end = start + (2 **(32 - cdr))
	
	diff = end - start
	
	return {"start" : start, "end" : end, "diff" : diff}
	
def host2subnetsize(hosts): 
	passes = 0
	fit = 0
	while fit != 1: 
		if (((2 ** passes ) -1 ) - hosts) >= 1: 
			fit = 1
		else: 
			passes += 1
	return {"host_size" : (2 ** passes), "cdr_size" : 32 - passes}


#Get the information from the user

input_iprange = str(input("IP Range: "))

passes = 1
choice = "yes"
hosts  = [] 

while choice != "no": 
	if choice == "yes":
		input_host_size   = str(input(str(passes) +". Host Size: "))
		input_host_amount = str(input(str(passes) +". Host Amount: "))
		
		#add input to an array
		if input_host_size != "" and input_host_amount != "": 
			hosts.append({'size' : input_host_size, 'amount' : input_host_amount})
		else: 
			print("one or more inputs are wrong")
		
		
		print("add another hosts?")
	
		choice = str(input("yes/no: "))
	
		passes += 1
	else: 
		print("Please try it again")
		choice = str(input("yes/no: "))


start_iprange = iprange(input_iprange)["start"]
end_iprange = iprange(input_iprange)["end"]
passes = 1
for subnetdata in hosts: 
	print(str(passes) + ".")

	print("\t 1. NA: " + str(number2ip(int(start_iprange))) + "/" + str(host2subnetsize(int(subnetdata["size"]))["cdr_size"]))
	print("\t 1. BC: " + str(number2ip(int(start_iprange + host2subnetsize(int(subnetdata["size"]))["host_size"] - 1))))
	
	if int(subnetdata["amount"]) > 1:
	
		print("\t " + subnetdata["amount"] + ". NA: " + str(number2ip(int(start_iprange)  + int(host2subnetsize(int(subnetdata["size"]))["host_size"] * (int(subnetdata["amount"]) -1) )     )) + "/" + str(host2subnetsize(int(subnetdata["size"]))["cdr_size"])) 
		print("\t " + subnetdata["amount"] + ". NC: " + str(number2ip(int(start_iprange)  + int(host2subnetsize(int(subnetdata["size"]))["host_size"] * int(subnetdata["amount"]) -1  ))))
		
		start_iprange = int(start_iprange)  + int(host2subnetsize(int(subnetdata["size"]))["host_size"] * int(subnetdata["amount"]))
	
	else: 
		start_iprange = int(start_iprange + host2subnetsize(int(subnetdata["size"]))["host_size"])
	passes += 1


if (start_iprange -1 ) >= end_iprange: 
	print("Error! Ip range is to small!")

