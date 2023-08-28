# **Faulty Scenario for EVPN Cluster Troubleshooting**

Here's the virtual lab to work on, majorly focus on the cleaf01 (leaf in the 1st rack). A few fault scenarios have been injected into the formally functional setup, only limited in cleaf01 switch for the interests of time.

## Basic setup: 
1. Topology attached for port-mapping.
2. mlag between ToRs switches
3. leaf/spine runs PTP layer3
4. BGP as underlay and overlay
5. vxlan tunnel for mlag active/active

## Goals to achieve (Rack01)
1. The mlag between ToRs up and running
2. port-channel101 facing computes in mlag formation
3. underlay BGP peering between leaf/spine ptp interface up/running
4. overlay BGP peering between lpbk0 of leaf/spine shall up/running
5. vxlan tunnel up with mlag active/active redundant formation

## Login
cleaf01: ssh admin@172.100.100.2\
cleaf02: ssh admin@172.100.100.3\
spine01: ssh admin@172.100.100.101\
spine02: ssh admin@172.100.100.102\

