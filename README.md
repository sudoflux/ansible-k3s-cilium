# Ansible K3s with Cilium

An Ansible playbook for deploying a K3s Kubernetes cluster with Cilium networking.

## Features

- Installs K3s on a user-defined cluster (configurable master and worker nodes)
- Disables installation of Traefik, Flannel, and other default K3s components
- Installs Cilium as the CNI with Ingress and LoadBalancer support
- Optional BGP mode configuration
- Automatically installs all prerequisites on target nodes

## Requirements

### Control Node Requirements
This playbook should be run from a control node, which can be:
- Your local workstation
- One of the future cluster nodes
- A dedicated management server

The control node requires:
- Ansible 2.9+ installed
- SSH access to all target nodes
- Internet access for downloading packages

### Target Node Requirements
The playbook automatically installs all required dependencies on target nodes. The minimum requirements are:
- Compatible Linux distribution (Ubuntu, Debian, CentOS, RHEL, etc.)
- SSH server running and accessible
- A user with sudo privileges (the playbook will configure this if needed)

## Usage

1. Clone this repository
   ```bash
   git clone https://github.com/sudoflux/ansible-k3s-cilium.git
   cd ansible-k3s-cilium
   ```

2. Update the inventory file with your hosts or use the included `inventory_generator.py` script to create one
   ```bash
   python3 inventory_generator.py
   ```

3. Review and modify `group_vars/all.yml` to match your environment

4. Run the playbook
   ```bash
   ansible-playbook site.yml -i inventory/hosts.yml
   ```

## Where to Run the Playbook

You can run this playbook from any machine that has:
1. Ansible installed
2. Network connectivity to all the target nodes
3. Proper SSH credentials configured

The playbook handles installing all prerequisites on the target machines, so they don't need any special configuration beforehand.

## Configuration

The main configuration variables are in `group_vars/all.yml`. Key options include:

- `k3s_version`: Version of K3s to install
- `cilium_version`: Version of Cilium to install
- `cilium_enable_bgp`: Whether to enable BGP mode for Cilium
- `cilium_enable_ingress`: Whether to enable Cilium Ingress Controller
- `cilium_enable_loadbalancer`: Whether to enable LoadBalancer support

See the comments in `group_vars/all.yml` for more options and details.

## Automatic Prerequisites Installation

The playbook includes a `prerequisites` role that will:
1. Check SSH connectivity
2. Install Python if not present
3. Configure sudo access
4. Ensure the SSH server is properly configured
5. Install necessary packages for Ansible management

This means you can run the playbook against fresh servers with minimal configuration.

## License

MIT