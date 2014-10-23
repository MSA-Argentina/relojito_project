#!/bin/bash
# Testea la sintaxis de un playbook
echo "################################"
echo "Testeo de sintaxis de playbooks"
echo "Versiones:"
echo "Ansible Version: $(ansible --version)"
echo "Ansible Playbook Version: $(ansible-playbook --version)"
echo "Vagrant Version: $(vagrant --version)"
echo "################################"

echo localhost > inventory
ansible-playbook --syntax-check --list-tasks -i inventory $1
rm inventory

exit 0
