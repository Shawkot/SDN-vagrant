import lxc
import os

# Function to create a container
def create_container(name, ip_address):
    c = lxc.Container(name)
    if not c.defined:
        c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu", "release": "bionic", "arch": "amd64", "keyserver": "keyserver.ubuntu.com"})
    if not c.start():
        return False
    c.wait("RUNNING", 3)
    c.attach_wait(lxc.attach_run_command, ["ip", "addr", "add", "{}/24".format(ip_address), "dev", "eth0"])
    c.attach_wait(lxc.attach_run_command, ["ip", "link", "set", "dev", "eth0", "up"])
    return True

# Function to create a switch
def create_switch(name, controller_ip):
    os.system("ovs-vsctl add-br {}".format(name))
    os.system("ovs-vsctl set bridge {} protocols=OpenFlow13".format(name))
    os.system("ovs-vsctl set-controller {} tcp:{}:6653".format(name, controller_ip))

# Function to connect a container to a switch
def connect_container_to_switch(container_name, switch_name):
    os.system("ip link add name veth{} type veth peer name veth{}_{}".format(container_name, container_name, switch_name))
    os.system("ip link set veth{} up".format(container_name))
    os.system("ip link set veth{}_{} up".format(container_name, switch_name))
    os.system("ovs-vsctl -- --may-exist add-port {} veth{}_{}".format(switch_name, container_name, switch_name))
    os.system("lxc config device add {} eth0 nic nictype=physical parent=veth{}".format(container_name, container_name))

# Create leaf switches and containers
ip_counter = 2
for i in range(1, 9):
    switch_name = "lf{}".format(i)
    create_switch(switch_name, "172.17.0.2")
    for j in range(1, 3):
        container_name = "lf{}_h{}".format(i, j)
        ip_address = "10.0.0.{}".format(ip_counter)
        create_container(container_name, ip_address)
        connect_container_to_switch(container_name, switch_name)
        ip_counter += 1

# Create spine switches and connect them to leaf switches
for i in range(1, 4):
    switch_name = "spine{}".format(i)
    create_switch(switch_name, "172.17.0.2")
    for j in range(1, 9):
        leaf_switch_name = "lf{}".format(j)
        os.system("ovs-vsctl add-port {} patch{} -- set interface patch{} type=patch options:peer=patch{}".format(switch_name, j, j, i))
        os.system("ovs-vsctl add-port {} patch{} -- set interface patch{} type=patch options:peer=patch{}".format(leaf_switch_name, i, i, j))