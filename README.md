# Ansible Automation for Arista Network

![Arista CloudVision Automation](https://img.shields.io/badge/Arista-CVP%20Automation-blue) ![Arista EOS Automation](https://img.shields.io/badge/Arista-EOS%20Automation-blue)

## About

This repository is configured to run [`arista.eos`](https://github.com/aristanetworks/ansible-eos) & [`arista.avd`](https://github.com/aristanetworks/ansible-avd) Ansible collections against the ['containerlab'](https://containerlab.dev/) topology, an open famework network topology solution.

## Virtual Lab topology

The diagram below shows that the Containerlab topology has one leaf/spine cluster. To simplify the lab topology, only the cEOS based switch nodes are created without hosts. The virutal lab topolgy meta data is defined in [ceos.clab.yaml](./topology/ceos.clab.yaml).

<p align="center">
  <img src="files/imgs/clab-topo.jpg" alt="Containerlab Topology" width="650"/>
</p>

## Containerlab topology device list

| Device | IP Address |
| ------ | ------------ |
| spine01  |172.100.100.101 |
| spine02  |172.100.100.102 |
| cleaf01  |172.100.100.2 |
| cleaf02  |172.100.100.3 |
| cleaf03  |172.100.100.4 |
| cleaf04  |172.100.100.5 |

## Containerlab topology port-map
| Device  | port | - | Device | port |
| ------  | ---- | - | ------ | ---- |
| spine01 | eth1 | - | cleaf01 | eth31 |
| spine01 | eth2 | - | cleaf02 | eth31 |
| spine01 | eth3 | - | cleaf03 | eth31 |
| spine01 | eth4 | - | cleaf04 | eth31 |
| spine02 | eth1 | - | cleaf01 | eth31 |
| spine02 | eth2 | - | cleaf02 | eth31 |
| spine02 | eth3 | - | cleaf03 | eth31 |
| spine02 | eth4 | - | cleaf04 | eth31 |
| cleaf01 | eth27 | - | cleaf02 | eth27 |
| cleaf01 | eth28 | - | cleaf02 | eth28 |
| cleaf03 | eth27 | - | cleaf04 | eth27 |
| cleaf03 | eth28 | - | cleaf04 | eth28 |
| cleaf01 | eth1 | - | host | bridge |
| cleaf01 | eth2 | - | host | bridge |
| cleaf02 | eth1 | - | host | bridge |
| cleaf02 | eth2 | - | host | bridge |
| cleaf03 | eth1 | - | host | bridge |
| cleaf03 | eth2 | - | host | bridge |
| cleaf04 | eth1 | - | host | bridge |
| cleaf04 | eth2 | - | host | bridge |

> Current repository is built with cEOS management interface (`Management0`). You can update `mgmt_interface` field to `Management1` in the ['lab.yaml'](./group_vars/lab.yaml) `group_vars`.

## Getting Started

### Spawn and inspect the containerlab

- Spawn the containerlab virtual topology
  > spawn a containerlab with a topology yaml

   ```shell
    containerlab deploy -t topology/ceos.clab.yaml --reconfigure
    ```

- Check the virtual topology state
  > inspect the containerlab

   ```shell
    containerlab inspect -t topology/ceos.clab.yaml
    ```

### Connect to your Containerlab environment

- Connect to individual container from the local host
  > ssh the cleaf01, oob-ip is exposed in the inspect check output
  > credential as default (***admin/admin***).

   ```shell
    ssh admin@172.100.100.2
    ```

### Ansible ad hoc
- Run ad hoc Ansible to check the topology

    - Execute the following command:
      > Ansible ad hoc execution, -m module, -a variable, -v verbose

      ```shell
      ansible -m eos_command -a "commands='show version'" lab -v
      ansible -m eos_command -a "commands='show lldp neighbor'" lab -v
      ```

    - Check the end logs of the playbook running. There shall be no errors.

### Ansible Arista Facts Collection
- Collect the Arista Platform information

    - Execute the following command:
      ```shell
      ansible -m eos_facts -a "gather_subset=hardware" smv472 -v
      ```

### Ansible Vault
- Create & Retrieve the encrypted password/keys in Vault

    - Execute the following command:
      ```shell
      ansible-vault encrypt_string 'lab123' --name 'vault_netops_password'
      ansible -m debug -a "var=vault_netops_password" localhost
      ```

### Ansible Playbook
- Run the playbook to prepare deploy EVPN cluster

    - Execute the following command:
      > deploy the evpn cluster from scratch

      ```shell
      ansible-playbook lab_deploy.yaml
      ```

    - Check the end logs of the playbook running. There shall be no errors.

- Run the playbook to collect the logs

    - Execute the following command:
      > day2 operation with log collecting, -t: only the tagged task

      ```shell
      ansible-playbook lab_oper.yaml -t generic
      ```

- Run the playbook to generate the specific configuration

    - Execute the following command:
      > Config generation for the specific function.
      >
      > *-e: extra customerized variable, -l: limit to*

      ```shell
      ansible-playbook lab_cfggen.yaml -e "temp_file=bgp_fabric.j2" -l cleaf01
      ```

- [Arista Ansible AVD Collection](https://github.com/aristanetworks/ansible-avd)
- [Arista CloudVision Collection](https://github.com/aristanetworks/ansible-cvp)
- [Arista AVD documentation](https://avd.arista.com)

## License

This Project is published under Apache License.
