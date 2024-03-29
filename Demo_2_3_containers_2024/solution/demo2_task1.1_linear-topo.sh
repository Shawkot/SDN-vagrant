#!/usr/bin/env bash


function create_ns() {
echo "Creating the namespace $1"
ip netns add $1
}

function create_ovs_bridge() {
echo "Creating the OVS bridge $1"
ovs-vsctl add-br $1
sudo ovs-vsctl set Bridge $1 protocols=OpenFlow13
}


function attach_ns_to_ovs() {
echo "Attaching the namespace $1 to the OVS $2"
ip link add $3 type veth peer name $4
ip link set $3 netns $1
ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
ip netns exec $1 ip addr add $6/24 dev $3
ip netns exec $1 ip link set dev $3 up
ip link set $4 up
}


function attach_ovs_to_ovs() {
    echo "Attaching the OVS $1 to the OVS $2"
    ip link add name $1-to-$2 type veth peer name $2-to-$1
    ip link set $1-to-$2 up
    ip link set $2-to-$1 up
    ovs-vsctl add-port $1 $1-to-$2 -- set Interface $1-to-$2 ofport_request=$5
    ovs-vsctl add-port $2 $2-to-$1 -- set Interface $2-to-$1 ofport_request=$5
}

function attach_ovs_to_sdn() {
    echo "Attaching the OVS bridge to the ONOS controller"
    CONTROLLER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q --filter ancestor=onosproject/onos))
    ovs-vsctl set-controller $1 tcp:$CONTROLLER_IP:6653
}

# Create namespaces
for i in {1..5}; do
    create_ns "host$i"
done

# Create bridges
for i in {1..5}; do
    create_ovs_bridge "br$i"
    attach_ovs_to_sdn "br$i"
    attach_ns_to_ovs "host$i" "br$i" "veth-host$i" "veth-host$i-br" 2 "10.0.0.$i"
done

# Connect bridges
for i in {1..4}; do
    j=$((i + 1))
    attach_ovs_to_ovs "br$i" "br$j" "br-ovs$i" "br-ovs$j" 1
done

# Test connectivity
for i in {1..4}; do
    j=$((i + 1))
    ip netns exec "host$i" ping -c 1 "10.0.0.$j"
    ip netns exec "host$j" ping -c 1 "10.0.0.$i"
done



