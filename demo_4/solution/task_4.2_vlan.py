import os

# Define the VLAN IDs for the Red and Blue slices
red_vlan = 100
blue_vlan = 200

# Define the bridges
bridges = ["br1", "br2", "br3", "br4", "br5"]

# Define the ports for the Red and Blue slices
red_ports = [1, 3, 5, 7, 9]
blue_ports = [2, 4, 6, 8, 10]

# Add VLAN tags to the ports
for bridge, red_port, blue_port in zip(bridges, red_ports, blue_ports):
    # Add the Red VLAN tag to the Red port
    os.system(f"ovs-vsctl set Port {bridge}-eth{red_port} tag={red_vlan}")
    # Add the Blue VLAN tag to the Blue port
    os.system(f"ovs-vsctl set Port {bridge}-eth{blue_port} tag={blue_vlan}")

# Isolate the VLANs
for bridge in bridges:
    # Drop traffic between the Red and Blue VLANs
    os.system(f"ovs-ofctl add-flow {bridge} priority=100,dl_vlan={red_vlan},actions=drop")
    os.system(f"ovs-ofctl add-flow {bridge} priority=100,dl_vlan={blue_vlan},actions=drop")
