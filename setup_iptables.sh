#!/bin/bash

# Allow traffic from internal to DMZ
iptables -A FORWARD -i internal_net -o dmz_net -j ACCEPT

# Block traffic from external to internal
iptables -A FORWARD -i external_net -o internal_net -j DROP

# Block traffic between containers in the same network
iptables -A FORWARD -i internal_net -o internal_net -j DROP
iptables -A FORWARD -i dmz_net -o dmz_net -j DROP
iptables -A FORWARD -i external_net -o external_net -j DROP

# Log dropped packets
iptables -A FORWARD -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
