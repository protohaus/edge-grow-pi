#!/bin/bash

set -e

DATA_DIR="/data/dhcp"
DHCPD_LEASE_FILE="$DATA_DIR/dhcpd.leases"
DHCPD_CONF_FILE="$DATA_DIR/dhcpd.conf"

# Single argument to command line is interface name
if [ -n "$DHCPD_IFACE" ]; then
    # skip wait-for-interface behavior if found in path
    if ! which "$DHCPD_IFACE" >/dev/null; then
        # loop until interface is found, or we give up
        NEXT_WAIT_TIME=1
        until [ -e "/sys/class/net/$DHCPD_IFACE" ] || [ $NEXT_WAIT_TIME -eq 4 ]; do
            sleep $(( NEXT_WAIT_TIME++ ))
            echo "Waiting for interface '$DHCPD_IFACE' to become available... ${NEXT_WAIT_TIME}"
        done
        if [ -e "/sys/class/net/$DHCPD_IFACE" ]; then
            IFACE="$DHCPD_IFACE"
        fi
    fi
fi

# No arguments mean all interfaces
if [ -z "$DHCPD_IFACE" ]; then
    IFACE=" "
fi

if [ -n "$IFACE" ]; then
    # Run dhcpd for specified interface or all interfaces


    if [ ! -r "$DHCPD_CONF_FILE" ]; then
        echo "Please ensure '$DHCPD_CONF_FILE' exists and is readable."
        echo "Run the container with arguments 'man dhcpd.conf' if you need help with creating the configuration."
        exit 1
    fi

    uid=$(stat -c%u "$DATA_DIR")
    gid=$(stat -c%g "$DATA_DIR")
    if [ $gid -ne 0 ]; then
        groupmod -g $gid dhcpd
    fi
    if [ $uid -ne 0 ]; then
        usermod -u $uid dhcpd
    fi

    # Inform the user if any existing leases have been stored
    if [[ -f "$DHCPD_LEASE_FILE" ]]; then
        dhcp-lease-list --lease "$DHCPD_LEASE_FILE" --all
    fi
    
    [ -e "$DHCPD_LEASE_FILE" ] || touch "$DHCPD_LEASE_FILE"
    chown dhcpd:dhcpd "$DHCPD_LEASE_FILE"
    if [ -e "$DHCPD_LEASE_FILE~" ]; then
        chown dhcpd:dhcpd "$DHCPD_LEASE_FILE~"
    fi

    container_id=$(grep docker /proc/self/cgroup | sort -n | head -n 1 | cut -d: -f3 | cut -d/ -f3)
    if perl -e '($id,$name)=@ARGV;$short=substr $id,0,length $name;exit 1 if $name ne $short;exit 0' $container_id $HOSTNAME; then
        echo "You must add the 'docker run' option '--net=host' if you want to provide DHCP service to the host network."
    fi

    /usr/sbin/dhcpd -4 -f -d --no-pid -cf "$DHCPD_CONF_FILE" -lf "$DHCPD_LEASE_FILE" $IFACE
fi

