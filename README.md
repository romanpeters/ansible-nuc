# ansible
Ansible configuration files used for my Intel NUC

1. Download and install Ubuntu
1. Find the IP address of your NUC and write it on the second line of `hosts`
1. Copy your SSH public key to the NUC with `ssh-copy-id`
1. SSH to the NUC and copy `<username> ALL=(ALL) NOPASSWD:ALL` to `sudo visudo -f /etc/sudoers.d/custom-users`
1. Change the IP address in `hosts` to the IP used by the remote
1. Run the main playbook: `$ ansible-playbook main.yml -i hosts`
