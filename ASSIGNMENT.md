# Chef Assignment
by Aiden Keating (20058454)

## Cookbooks
There are four chef cookbooks used in the assignment, these are.
- todo-node
- mongodb
- haproxy
- upskill

### mongodb
The `mongodb` cookbook is a community cookbook available at https://supermarket.chef.io/cookbooks/mongodb. Attributes were modified to allow the database to be accessed remotely.

The `mongodb` node uses the role `webserver`.

### todo-node
The `todo-node` cookbooks utilizes the `nodejs` cookbook to install Node.js, it then pulls the GitHub repository of the same name, installs the `forever` npm package, performs an npm install and runs the server using `forever`.

The `todo-node` default recipe dynamically finds a mongodb database with the role name of `mongo` and uses it as the database for the application.

All nodes using `todo-node` use the role `webserver` in order to be found by the loadbalancer.

###  haproxy
The `haproxy` cookbook is basically just a `haproxy.cfg` file that is updated by search results looking for any nodes with the `webserver` role.

The haproxy node uses the role `loadbalancer`.

### upskill
The `upskill` cookbook is a scheduling tool that is currently only used for calling `chef-client` every once in a while (There is a cookbook that does this already). However, it can also be used to call any command such as updating packages/updating Node.js every once in a while also. It was mostly created to explore Chef more.

## Infrastructure Automation (LaCroix)
LaCroix is a project that can be used to automate the creation of AWS infrastructure inside a VPC using a `config.json` file. The repository for this project is available at: https://github.com/aidenkeating/lacroix

## Issues
The main issues experienced during the project were that the `haproxy` cookbook was not automatically running even though the recipe calls `service haproxy start`. The reason for this is that the `/etc/default/haproxy` file contains a setting called `ENABLED` which is set to 0 by default. A template was created that defaults this setting to 1 and haproxy started working properly.

Another issue was that `mongodb` by default does not allow remote access, however allowing complete remote access is not a great idea in terms of security. Due to this remote access is allowed to the database, but only from machines within the same subnet in the VPC using LaCroix. Although it would be better to allow access only to nodes with the role `webserver` but I was restricted by time.

A final issue was that by default in the Python `boto` library instances are not created with public IP addresses. The following snippet fixes this issue.
```python
interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=subnet.id,
																	groups=[sg.id],
																	associate_public_ip_address=True)
interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
reservation = vpc_conn.run_instances(settings['ami'], key_name=config['keyName'],
								instance_type='t2.micro',
								network_interfaces=interfaces)
```
