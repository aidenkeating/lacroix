import boto
import boto.vpc
import json
import subprocess
import boto.ec2.networkinterface

config = dict()

def main():
	with open('./config.json') as config_file:
		config = json.load(config_file)
	vpc_conn = boto.vpc.connect_to_region(config['region'])

	# Create VPC
	vpc = vpc_conn.create_vpc('10.0.0.0/24')
	print "VPC (%s) created." % (vpc.id,)

	# Update VPC
	vpc_conn.modify_vpc_attribute(vpc.id, enable_dns_support=True)
	vpc_conn.modify_vpc_attribute(vpc.id, enable_dns_hostnames=True)

	# Create an Internet Gateway
	gateway = vpc_conn.create_internet_gateway()

	# Attach the Internet Gateway to our VPC
	vpc_conn.attach_internet_gateway(gateway.id, vpc.id)

	# Create a Route Table
	route_table = vpc_conn.create_route_table(vpc.id)

	# Create a size /16 subnet
	subnet = vpc_conn.create_subnet(vpc.id, '10.0.0.0/24')

	# Associate Route Table with our subnet
	vpc_conn.associate_route_table(route_table.id, subnet.id)

	# Create a Route from our Internet Gateway to the internet
	route = vpc_conn.create_route(route_table.id, '0.0.0.0/0', gateway.id)

	# Create a new VPC security group
	sg_name = "%s_chef" % (config['alias'],)
	sg = vpc_conn.create_security_group(sg_name,
	                                sg_name,
	                                vpc.id)

	# Authorize access to port 22 and 80 from anywhere
	sg.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
	sg.authorize(ip_protocol='tcp', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')
	sg.authorize(ip_protocol='tcp', from_port=27017, to_port=27017, cidr_ip='10.0.0.0/24')

	for name, settings in config['instances'].iteritems():
		interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=subnet.id,
																			groups=[sg.id],
																			associate_public_ip_address=True)
		interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
		reservation = vpc_conn.run_instances(settings['ami'], key_name=config['keyName'],
										instance_type='t2.micro',
										network_interfaces=interfaces)
		instance = reservation.instances[0]
		instance_name = "%s_%s" % (config['alias'], name,)
		vpc_conn.create_tags([instance.id],{'Name': instance_name})
		if settings['public']:
			print "Starting IP address association with %s." % (name,)
			eip = vpc_conn.allocate_address(domain='vpc')
			print "Waiting for %s to be running before associating address." % (name,)
			while instance.state != 'running':
				instance.update()
			vpc_conn.associate_address(instance_id=instance.id,
								allocation_id=eip.allocation_id)
		print "%s started" % (name,)
	print "Build complete."


if __name__ == '__main__':
	main()
