#!/usr/bin/env python3

import os
import yaml

def get_input(prompt, default=None):
    if default:
        result = input(f"{prompt} [{default}]: ")
        return result if result else default
    return input(f"{prompt}: ")

def get_int_input(prompt, default=None):
    while True:
        try:
            if default:
                result = input(f"{prompt} [{default}]: ")
                return int(result) if result else int(default)
            return int(input(f"{prompt}: "))
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("\nK3s with Cilium Inventory Generator")
    print("=================================\n")
    
    # Get user info
    ssh_user = get_input("SSH username for all hosts", "ubuntu")
    ssh_key_path = get_input("Path to SSH private key", "~/.ssh/id_rsa")
    require_sudo = get_input("Do nodes require sudo? (yes/no)", "yes").lower() in ["yes", "y"]
    
    # Get master nodes info
    master_count = get_int_input("Number of master nodes", 1)
    master_prefix = get_input("Hostname prefix for master nodes", "k3s-master-")
    master_ips = []
    
    print(f"\nEnter IPs for {master_count} master nodes:")
    for i in range(1, master_count + 1):
        master_ips.append(get_input(f"  {master_prefix}{i} IP address"))
    
    # Get worker nodes info
    worker_count = get_int_input("Number of worker nodes", 2)
    worker_prefix = get_input("Hostname prefix for worker nodes", "k3s-worker-")
    worker_ips = []
    
    if worker_count > 0:
        print(f"\nEnter IPs for {worker_count} worker nodes:")
        for i in range(1, worker_count + 1):
            worker_ips.append(get_input(f"  {worker_prefix}{i} IP address"))
    
    # Create inventory structure
    inventory = {
        "all": {
            "children": {
                "k3s_cluster": {
                    "children": {
                        "k3s_masters": {"hosts": {}},
                        "k3s_workers": {"hosts": {}}
                    }
                }
            },
            "vars": {
                "ansible_user": ssh_user,
                "ansible_ssh_private_key_file": ssh_key_path,
                "ansible_become": require_sudo
            }
        }
    }
    
    # Add master nodes
    for i, ip in enumerate(master_ips, 1):
        inventory["all"]["children"]["k3s_cluster"]["children"]["k3s_masters"]["hosts"][f"{master_prefix}{i}"] = {
            "ansible_host": ip
        }
    
    # Add worker nodes
    for i, ip in enumerate(worker_ips, 1):
        inventory["all"]["children"]["k3s_cluster"]["children"]["k3s_workers"]["hosts"][f"{worker_prefix}{i}"] = {
            "ansible_host": ip
        }
    
    # Create directory if it doesn't exist
    os.makedirs("inventory", exist_ok=True)
    
    # Write inventory file
    with open("inventory/hosts.yml", "w") as f:
        f.write("---\n")
        yaml.dump(inventory, f, default_flow_style=False)
    
    print("\nInventory file generated at inventory/hosts.yml")
    print("You can now run: ansible-playbook site.yml -i inventory/hosts.yml")

if __name__ == "__main__":
    main()