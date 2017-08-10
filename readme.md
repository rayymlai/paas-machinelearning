# paas-machinelearning

## Summary
This project provides docker image definitions (dockerfile) for development infrastructure, framework and helper class used in  machine learning.

## Features
* Python3 container with frequently used machine learning libraries, e.g. nltk, numpy, scikit
* SSH access to Python3 container
* Built-in Flask for Web app development and REST API
* Jupyter notebook with password control

## User Guide
### Assumptions
* Ports
Port 3xxx for application, e.g. 3001 for SSH (mapped to port 22 within docker container), 3002 for HTTP REST API (mapped to Flask port 5000), 4001 for Jupyter (mapped to port 888 withi docker container)

* Shared data volume
SSH user provisioning scripts are placed (e.g. git clone from your devops project)  under /mnt/data/docker/devops. You can customize a script to create SSH user, and copy their SSH public keys.

Your Jupyter password file (config file created from --generate-config) mapped to /root/.jupyter/jupyter_notebook_config.py

* Machine learning libraries (e.g. numpy, nltk)
Machine learning libraries are installed using pip for python3.

### Execution sequence
* Build docker image, e.g.
docker build -t rayymlai/jupyter01 .

* Launch docker image, e.g.
docker run -d --name jupyter01 --hostname jupyter01.zebots.io  -v /mnt/data/dev/jupyter01:/opt/src/jupyter01 -p 3001:22 -p 3002:5000 -p 4001:8888 -v /mnt/data/docker/devops:/opt/devops -v /mnt/data/docker/paas-machinelearning/customPassword.txt:/root/.jupyter/jupyter_notebook_config.py rayymlai/jupyter01

* Start Jupyter notebook, e.g.
docker exec -ti jupyter01 jupyter notebook --no-browser --ip='*' --allow-root &

* Login to Jupyter notebook
From Web browser:
http://xxx:4001

Enter password to login (default password is pneumonoultramicroscopicsilicovolcanoconiosis)

* Start flask with REST API
docker exec -ti py02 python3 /app/app.py

You can verify your web app container by opening a browser session with http://xxx:3002 or using "curl http://xxx:3002"

### How to generate password hash for Jupyter notebook
* From python shell (e.g. docker exec -ti py02 bash python)
>>> from IPython.lib import passwd
>>> password = passwd("pneumonoultramicroscopicsilicovolcanoconiosis")
>>> password
'sha1:639c9647638d:7b1fe7a715d20d4c19118be33cebd4dca610c2a6'

Default Jupyter password (if not overriden using docker run with a new password file mapped): pneumonoultramicroscopicsilicovolcanoconiosis


