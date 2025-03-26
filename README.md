# 🚀 Ansible K3s with Cilium

An Ansible playbook for deploying a production-ready K3s Kubernetes cluster with Cilium networking.

## ✨ Features

- 🌐 Installs K3s on a user-defined cluster (configurable master and worker nodes)
- 🧩 Disables installation of Traefik, Flannel, and other default K3s components
- 🐙 Installs Cilium 1.17.2 as the CNI with proper CRD support
- 🚪 Provides complete Ingress Controller functionality with IngressClass support
- ⚖️ Supports LoadBalancer services with L2 announcements or BGP
- 📡 Optional BGP mode configuration
- 🛠️ Automatically installs all prerequisites on target nodes
- 🧹 Supports clean installation option to remove previous K3s/Cilium deployments
- 🐍 Works on nodes without Python using raw commands for bootstrapping

## 📋 Requirements

### Control Node Requirements
This playbook should be run from a control node, which can be:
- Your local workstation
- One of the future cluster nodes
- A dedicated management server

The control node requires:
- Ansible 2.9+ installed
- Python 3.x installed (for running Ansible and the inventory generator script)
- SSH access to all target nodes
- Internet access for downloading packages

### Target Node Requirements
The playbook automatically installs all required dependencies on target nodes. The minimum requirements are:
- Compatible Linux distribution (Ubuntu, Debian, CentOS, RHEL, etc.)
- SSH server running and accessible
- A user with sudo privileges (the playbook will configure this if needed)

**Note:** Python is NOT required to be pre-installed on target nodes. The playbook uses raw commands for initial setup and installs Python on the target nodes if necessary.

## 🚦 Usage

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

5. For clean installation (removing previous K3s/Cilium):
   ```bash
   # Make sure clean_install is set to true in inventory/hosts.yml
   ansible-playbook site.yml -i inventory/hosts.yml --ask-become-pass
   ```

## 🖥️ Where to Run the Playbook

You can run this playbook from any machine that has:
1. Ansible installed
2. Network connectivity to all the target nodes
3. Proper SSH credentials configured

The playbook handles installing all prerequisites on the target machines, so they don't need any special configuration beforehand.

## ⚙️ Configuration

The main configuration variables are in `group_vars/all.yml`. Key options include:

- `k3s_version`: Version of K3s to install (defaults to latest)
- `cilium_version`: Version of Cilium to install (currently set to 1.17.2)
- `cilium_enable_bgp`: Whether to enable BGP mode for Cilium
- `cilium_enable_ingress`: Whether to enable Cilium Ingress Controller (enabled by default)
- `cilium_enable_loadbalancer`: Whether to enable LoadBalancer support (enabled by default)
- `cilium_enable_hubble`: Whether to enable Hubble observability

See the comments in `group_vars/all.yml` for more options and details.

## 🚦 Python Bootstrapping and Node Preparation

This playbook is designed to work on fresh servers with minimal pre-configuration. Here's how it handles nodes without Python:

1. **Initial Connection**: The playbook uses Ansible's `raw` module for the initial connection and setup, which doesn't require Python on the target hosts.

2. **Python Installation**: It automatically installs Python if it's not already present, using OS-native package managers like apt or yum.

3. **Python Interpreter Paths**: The inventory specifies the Python interpreter path (`ansible_python_interpreter: /usr/bin/python3`) to avoid detection issues.

4. **Error Handling**: The playbook includes robust error handling for Python-related issues, including cases where Python is installed but not in the expected location.

This approach allows you to run the playbook against completely fresh servers without manually installing Python first.

Example inventory configuration:
```yaml
all:
  vars:
    ansible_user: your_user
    ansible_ssh_private_key_file: ~/.ssh/id_ed25519
    ansible_become: true
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
    ansible_python_interpreter: /usr/bin/python3
```

## 🌐 Ingress Configuration

The playbook automatically sets up Cilium as the default IngressClass controller in your cluster. This means:

1. You can create standard Kubernetes Ingress resources without specifying the IngressClass
2. Cilium will handle the routing of external traffic to your services
3. LoadBalancer services will work out of the box

Example Ingress resource:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app
            port:
              number: 80
```

## 🔄 Reinstalling or Upgrading

To reinstall or upgrade an existing cluster:

1. Set `clean_install: true` in your inventory file
2. Run the playbook with sudo access: `ansible-playbook site.yml -i inventory/hosts.yml --ask-become-pass`

This will:
- Uninstall existing K3s installation
- Clean up CNI configuration files
- Remove stale container resources
- Install fresh K3s and Cilium instances

## ⚠️ Known Issues and Gotchas for Cilium 1.17.2

When using Cilium 1.17.2, be aware of the following:

1. **Deprecated `tunnel` Option**: The `tunnel` configuration option was deprecated in Cilium 1.14 and removed in 1.15. If you encounter an error message like:
   ```
   execution error: tunnel was deprecated in v1.14 and has been removed in v1.15
   ```
   This playbook automatically removes this option from the configuration.

2. **kubeProxyReplacement Setting**: In Cilium 1.17.2, `kubeProxyReplacement` must be set to either `true` or `false`, not `strict`. The playbook sets this to `true` by default.

3. **Namespace Termination Issues**: If a previous Cilium installation left a namespace (like `cilium-secrets`) in a "Terminating" state, you may need to force-delete it:
   ```bash
   kubectl get namespace cilium-secrets -o json | jq '.spec.finalizers = []' > temp.json
   kubectl replace --raw "/api/v1/namespaces/cilium-secrets/finalize" -f temp.json
   ```
   The clean installation option attempts to handle this automatically.

4. **KUBECONFIG Environment Variable**: When running helm commands or kubectl manually on the master node, you may need to specify the kubeconfig location:
   ```bash
   KUBECONFIG=/etc/rancher/k3s/k3s.yaml kubectl get pods
   ```

## 🛠️ Automatic Prerequisites Installation

The playbook includes a `prerequisites` role that will:
1. Check SSH connectivity
2. Install Python if not present
3. Configure sudo access
4. Ensure the SSH server is properly configured
5. Install necessary packages for Ansible management

This means you can run the playbook against fresh servers with minimal configuration.

## 📜 License

MIT