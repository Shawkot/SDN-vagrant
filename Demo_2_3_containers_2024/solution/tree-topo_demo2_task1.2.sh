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
for i in {1..8}; do
    create_ns "host$i"
done

# Create bridges
for i in {1..7}; do
    create_ovs_bridge "br$i"
    attach_ovs_to_sdn "br$i"
done

# Attach namespaces (hosts) to leaf bridges
for i in {1..4}; do
    attach_ns_to_ovs "host$((2*i-1))" "br$((i+3))" "veth-host$((2*i-1))" "veth-host$((2*i-1))-br" 2 "10.0.0.$((2*i-1))"
    attach_ns_to_ovs "host$((2*i))" "br$((i+3))" "veth-host$((2*i))" "veth-host$((2*i))-br" 3 "10.0.0.$((2*i))"
done

# Connect bridges to form a tree topology
attach_ovs_to_ovs "br1" "br2" "br1-to-br2" "br2-to-br1" 1
attach_ovs_to_ovs "br1" "br3" "br1-to-br3" "br3-to-br1" 1
attach_ovs_to_ovs "br2" "br4" "br2-to-br4" "br4-to-br2" 1
attach_ovs_to_ovs "br2" "br5" "br2-to-br5" "br5-to-br2" 1
attach_ovs_to_ovs "br3" "br6" "br3-to-br6" "br6-to-br3" 1
attach_ovs_to_ovs "br3" "br7" "br3-to-br7" "br7-to-br3" 1

# Test connectivity
#for i in {1..8}; do
 #   for j in {1..8}; do
  #      if [ $i -ne $j ]; then
   #         ip netns exec "host$i" ping -c 1 "10.0.0.$j"
    #    fi
    # done
# done