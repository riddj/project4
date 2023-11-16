import ipaddress
from argparse import ArgumentParser
from gooey import Gooey

@Gooey(show_success_modal=False, program_name="Subnet Calculator")
def main():
    parser = ArgumentParser()
    parser.add_argument("ip", help="Provide an IP address.")
    parser.add_argument("subnet", help="The network mask or number of network bits.")
    args = parser.parse_args()

    if "." in args.ip:
        ip_version = 4
    elif ":" in args.ip:
        ip_version = 6
    else:
        raise TypeError("Could not parse the provided IP.")

    # calculate network mask
    try:
        # parse subnets entered as # of network bits
        subnet_bits = int(args.subnet)
        if ip_version == 4:
            host_bits = 32 - subnet_bits
            network_mask = ipaddress.IPv4Network(f"0.0.0.0/{subnet_bits}").netmask
        else:
            host_bits = 128 - subnet_bits
            network_mask = ipaddress.IPv6Network(f"0::0/{subnet_bits}").netmask
    except ValueError:
        # entered subnet was a mask - count number of consecutive zeros in network mask
        if ip_version == 4:
            network_mask = ipaddress.IPv4Address(args.subnet)
        else:
            network_mask = ipaddress.IPv6Address(args.subnet)
        binary_mask = bin(int(network_mask))
        host_bits = str(binary_mask)[::-1].index("1")

    # create network based on mask for reference, calculate usable ip range and # of hosts
    if ip_version == 4:
        network = ipaddress.IPv4Network(f"{args.ip}/{network_mask}", strict=False)
        usable_ip_range = str(network.network_address + 1) + ' to ' + str(network.broadcast_address - 1)
        hosts_on_subnet = (2 ** host_bits) - 2
    else:
        network = ipaddress.IPv6Network(f"{args.ip}/{host_bits}", strict=False)
        usable_ip_range = str(network.network_address) + ' to ' + str(network.broadcast_address)
        hosts_on_subnet = 2 ** host_bits

    print(f"Network Mask: {network_mask}")
    print(f"Network Address: {network.network_address}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"Usable IP Range: {usable_ip_range}")
    print(f"Number of Hosts on Subnet: {hosts_on_subnet}\n")

if __name__ == "__main__":
    main()