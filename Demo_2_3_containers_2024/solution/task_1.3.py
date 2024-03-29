import subprocess

def create_ns(name):
    subprocess.run(["ip", "netns", "add", name])

def create_ovs_bridge(name):
    subprocess.run(["ovs-vsctl", "add-br", name])
    subprocess.run(["sudo", "ovs-vsctl", "set", "Bridge", name, "protocols=OpenFlow13"])

def attach_ns_to_ovs(ns, ovs, veth1, veth2, ofport, ip):
    subprocess.run(["ip", "link", "add", veth1, "type", "veth", "peer", "name", veth2])
    subprocess.run(["ip", "link", "set", veth1, "netns", ns])
    subprocess.run(["ovs-vsctl", "add-port", ovs, veth2, "--", "set", "Interface", veth2, "ofport_request="+ofport])
    subprocess.run(["ip", "netns", "exec", ns, "ip", "addr", "add", ip+"/24", "dev", veth1])
    subprocess.run(["ip", "netns", "exec", ns, "ip", "link", "set", "dev", veth1, "up"])
    subprocess.run(["ip", "link", "set", veth2, "up"])

def attach_ovs_to_ovs(ovs1, ovs2, veth1, veth2, ofport):
    subprocess.run(["ip", "link", "add", "name", veth1, "type", "veth", "peer", "name", veth2])
    subprocess.run(["ip", "link", "set", veth1, "up"])
    subprocess.run(["ip", "link", "set", veth2, "up"])
    subprocess.run(["ovs-vsctl", "add-port", ovs1, veth1, "--", "set", "Interface", veth1, "ofport_request="+ofport])
    subprocess.run(["ovs-vsctl", "add-port", ovs2, veth2, "--", "set", "Interface", veth2, "ofport_request="+ofport])

def attach_ovs_to_sdn(ovs):
    subprocess.run(["ovs-vsctl", "set-controller", ovs, "tcp:127.0.0.1:6653"])

def create_topology():
    topology_type = input("Enter topology type (tree or linear): ")
    if topology_type == "tree":
        depth = int(input("Enter tree depth: "))
        fanout = int(input("Enter tree fanout: "))
        # Create bridges and attach them to the ONOS controller
        for i in range(1, fanout**depth):
            create_ovs_bridge("br"+str(i))
            attach_ovs_to_sdn("br"+str(i))

        # Connect bridges to form a tree topology
        for i in range(1, fanout**(depth-1)):
    	    for j in range(1, fanout+1):
                attach_ovs_to_ovs("br"+str(i), "br"+str((i-1)*fanout+j+1), "br"+str(i)+"-to-br"+str((i-1)*fanout+j+1), "br"+str((i-1)*fanout+j+1)+"-to-br"+str(i), "1")

        # Create namespaces and attach them to leaf bridges
        for i in range(fanout**(depth-1), fanout**depth):
    	    for j in range(1, fanout+1):
                create_ns("host"+str((i-fanout**(depth-1))*fanout+j))
                attach_ns_to_ovs("host"+str((i-fanout**(depth-1))*fanout+j), "br"+str(i), "veth-host"+str((i-fanout**(depth-1))*fanout+j), "veth-host"+str((i-fanout**(depth-1))*fanout+j)+"-br", "2", "10.0.0."+str((i-fanout**(depth-1))*fanout+j))

    elif topology_type == "linear":
        num_switches = int(input("Enter number of switches: "))
        # Create namespaces, bridges and attach them to the ONOS controller
        for i in range(1, num_switches+1):
            create_ns("host"+str(i))
            create_ovs_bridge("br"+str(i))
            attach_ovs_to_sdn("br"+str(i))
            attach_ns_to_ovs("host"+str(i), "br"+str(i), "veth-host"+str(i), "veth-host"+str(i)+"-br", "2", "10.0.0."+str(i))

        # Connect bridges to form a linear topology
        for i in range(1, num_switches):
            attach_ovs_to_ovs("br"+str(i), "br"+str(i+1), "br"+str(i)+"-to-br"+str(i+1), "br"+str(i+1)+"-to-br"+str(i), "1")

create_topology()
