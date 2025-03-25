# Ansible K3s with Cilium

An Ansible playbook for deploying a K3s Kubernetes cluster with Cilium networking.

## Features

- Installs K3s on a user-defined cluster (configurable master and worker nodes)
- Disables installation of Traefik, Flannel, and other default K3s components
- Installs Cilium as the CNI with Ingress and LoadBalancer support
- Optional BGP mode configuration

## Requirements

- Ansible 2.9+ installed on the control node
- SSH access to all target nodes
- Python installed on all target nodes
- Internet access on all nodes for package installation

## Usage

1. Clone this repository
   ```bash
   git clone https://github.com/sudoflux/ansible-k3s-cilium.git
   cd ansible-k3s-cilium
   ```

2. Update the inventory file with your hosts or use the included `inventory_generator.py` script to create one
   ```bash
   python inventory_generator.py
   ```

3. Review and modify `group_vars/all.yml` to match your environment

4. Run the playbook
   ```bash
   ansible-playbook site.yml -i inventory/hosts.yml
   ```

## Configuration

The main configuration variables are in `group_vars/all.yml`. Key options include:

- `k3s_version`: Version of K3s to install
- `cilium_version`: Version of Cilium to install
- `cilium_enable_bgp`: Whether to enable BGP mode for Cilium
- `cilium_enable_ingress`: Whether to enable Cilium Ingress Controller
- `cilium_enable_loadbalancer`: Whether to enable LoadBalancer support

See the comments in `group_vars/all.yml` for more options and details.

## License

MIT