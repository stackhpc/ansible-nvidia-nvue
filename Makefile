test:
	mkdir -p ansible_collections/nvidia/nvue
	rsync -av . ansible_collections/nvidia/nvue --exclude ansible_collections/nvidia/nvue
	cd ansible_collections/nvidia/nvue && ansible-test sanity -v --color --docker