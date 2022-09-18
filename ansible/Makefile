install:
	ansible-playbook -i inventory -e @secrets.yml install.yml
uninstall:
	ansible-playbook -i inventory uninstall.yml
redeploy: uninstall install
