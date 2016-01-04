# -*- coding: utf-8 -*-
# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
ANSIBLE_CFG = "/etc/ansible/ansible.cfg"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  if Vagrant.has_plugin?("vagrant-cachier")
    # To use vagrant-cachier (a plugin to cache apt packages)
    # install: vagrant plugin install vagrant-cachier
    config.cache.scope = :box
    config.cache.enable :apt
    config.cache.enable :apt_lists
  end

  if Vagrant.has_plugin?("vagrant-triggers")
    # To use vagrant-trigger, and perform a git pull
    # inside the ansible-roles repo before provisioning
     config.trigger.before :provision, :option => "value" do
        f = File.open(ANSIBLE_CFG, "r")
        f.each_line do |line|
            if line.include? "roles_path"
                path_line = line.split '='
                path = path_line[1].strip()
                system("cd #{path}; git pull")
            end
        end
     end
  end

  config.push.define "production", strategy: "local-exec" do |push|
    push.script = "deploy_production.sh"
  end


  config.vm.define "relojito-development", autostart: true do |machine|
      machine.vm.box = "ubuntu/trusty64"
      machine.vm.hostname = "relojito"
      machine.vm.network "forwarded_port", guest: 80, host: 2134
      machine.vm.network "private_network", ip: "192.168.70.10"
      machine.vm.network "public_network", bridge: "wlan0"
      machine.vm.synced_folder "/opt/relojito_project", "/opt/relojito_project"
      machine.vm.provision :ansible do |ansible|
            ansible.playbook = "provisioning/relojito-development.yml"
            ansible.inventory_path = "provisioning/ansible_hosts"
            ansible.host_key_checking = false
            # ansible.tags = "deploy"
      end
      # With this we avoid errors in uwsgi after loading the VM
      machine.vm.provision "shell",
                           inline: "sudo service uwsgi restart"
  end
end
