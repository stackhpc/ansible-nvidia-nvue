sudo apt-get update -y
sudo python3 -m pip install ansible
sudo export PATH=/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ansible --version

mkdir ~/.ansible/collections
mkdir ~/.ansible/collections/ansible_collections
mkdir ~/.ansible/collections/ansible_collections/nvidia
cd ~/.ansible/collections/ansible_collections/nvidia
git clone https://gitlab.com/nvidia-networking/systems-engineering/nvue.git
cd nvue
git checkout develop
