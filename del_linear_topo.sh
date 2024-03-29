#!/usr/bin/env bash

function delete_ns() {
    echo "Deleting the namespace $1"
    ip netns del $1
}

function delete_ovs_bridge() {
    echo "Deleting the OVS bridge $1"
    ovs-vsctl del-br $1
}

# Delete namespaces
for i in {1..5}; do
    delete_ns "host$i"
done

# Delete bridges
for i in {1..5}; do
    delete_ovs_bridge "br$i"
done

echo "Topology deleted successfully"
