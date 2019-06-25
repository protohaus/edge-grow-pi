#!/bin/bash

dnsmasq --keep-in-foreground --conf-file=/data/dnsmasq.conf --dhcp-leasefile=/data/dnsmasq.leases
