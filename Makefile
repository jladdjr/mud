test:
	venv/bin/python3 -m unittest discover -s tests

system_requirements:
	cat system_requirements.txt | xargs -I{} sudo apt -y install {}

venv:
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip3 install -U -r requirements.txt
