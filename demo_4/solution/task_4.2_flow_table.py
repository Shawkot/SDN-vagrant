import os

# Define the IP ranges for the Red and Blue slices
red_ips = ["10.0.0.2", "10.0.0.4", "10.0.0.6", "10.0.0.8", "10.0.0.10"]
blue_ips = ["10.0.0.3", "10.0.0.5", "10.0.0.7", "10.0.0.9", "10.0.0.11"]

# Define the bridges
bridges = ["br1", "br2", "br3", "br4", "br5"]

# Add flow rules to isolate the Red and Blue slices
for bridge in bridges:
    for ip in red_ips:
        # Allow traffic within the Red slice
        os.system(f"ovs-ofctl add-flow {bridge} ip,nw_src={ip},actions=output:1")
        # Drop traffic from the Red slice to the Blue slice
        for blue_ip in blue_ips:
            os.system(f"ovs-ofctl add-flow {bridge} ip,nw_src={ip},nw_dst={blue_ip},actions=drop")

    for ip in blue_ips:
        # Allow traffic within the Blue slice
        os.system(f"ovs-ofctl add-flow {bridge} ip,nw_src={ip},actions=output:2")
        # Drop traffic from the Blue slice to the Red slice
        for red_ip in red_ips:
            os.system(f"ovs-ofctl add-flow {bridge} ip,nw_src={ip},nw_dst={red_ip},actions=drop")
