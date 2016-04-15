##!/bin/bash

ansible-playbook -i /opt/relojito_project/provisioning/ansible_hosts /opt/relojito_project/provisioning/relojito-staging.yml --tags deploy,restart,requirements -K
