#!/bin/bash

function create_ns() {
    echo "Creating the namespace $1"
    sudo ip netns add $1 || echo "Failed to create namespace $1"
}

function create_ovs_bridge() {
    echo "Creating the OVS bridge $1"
    sudo ovs-vsctl add-br $1 || echo "Failed to create OVS bridge $1"
    sudo ovs-vsctl set bridge $1 protocols=OpenFlow13
}

function attach_ns_to_ovs() {
    echo "Attaching the namespace $1 to the OVS $2"
    sudo ip link del $3 || true  # Delete the veth pair if it exists
    sudo ip link add $3 type veth peer name $4
    sudo ip link set $3 netns $1
    sudo ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
    sudo ip netns exec $1 ip addr add $6/24 dev $3
    sudo ip netns exec $1 ip link set dev $3 up
    sudo ip link set $4 up
}

function attach_ovs_to_ovs() {
    echo "Attaching the OVS $1 to the OVS $2"
    sudo ip link del $3 || true  # Delete the veth pair if it exists
    sudo ip link add name $3 type veth peer name $4
    sudo ip link set $3 up
    sudo ip link set $4 up
    sudo ovs-vsctl add-port $1 $3 -- set Interface $3 ofport_request=$5
    sudo ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
}

function attach_ovs_to_sdn() {
    echo "Attaching the OVS bridge to the ONOS controller"
    sudo ovs-vsctl set-controller $1 tcp:$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q  --filter ancestor=onosproject/onos)):6653 || echo "Failed to set controller for OVS $1"
}

create_ns red
create_ns blue

create_ovs_bridge br-1
create_ovs_bridge br-2

attach_ovs_to_ovs br-1 br-2 br-ovs1 br-ovs2 1
attach_ns_to_ovs red br-1 veth-red veth-red-br 2 10.0.0.2
attach_ns_to_ovs blue br-2 veth-blue veth-blue-br 2 10.0.0.3

attach_ovs_to_sdn br-1
attach_ovs_to_sdn br-2

sudo ip netns exec red ping -c 1 10.0.0.3
sudo ip netns exec blue ping -c 1 10.0.0.2
