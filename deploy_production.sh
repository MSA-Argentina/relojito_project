##!/bin/bash

ansible-playbook -i /opt/relojito_project/provisioning/ansible_hosts /opt/relojito_project/provisioning/relojito-production.yml --tags deploy,restart,requirements -K
