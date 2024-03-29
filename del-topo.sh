#!/bin/bash

function delete_ns() {
    echo "Deleting the namespace $1"
    sudo ip netns delete $1 || echo "Failed to delete namespace $1"
}

function delete_ovs_bridge() {
    echo "Deleting the OVS bridge $1"
    sudo ovs-vsctl del-br $1 || echo "Failed to delete OVS bridge $1"
}

function delete_ns_to_ovs() {
    echo "Deleting the link from namespace $1 to OVS $2"
    sudo ip link delete $3 || echo "Failed to delete veth pair $3"
}

delete_ns_to_ovs red br-1 veth-red
delete_ns_to_ovs blue br-2 veth-blue

delete_ns red
delete_ns blue

delete_ovs_bridge br-1
delete_ovs_bridge br-2
