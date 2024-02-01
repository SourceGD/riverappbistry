.. _gitlab_runner:

################################
How to install the gitlab runner
################################

Option 1 : Using Docker
#######################

Install Docker in a linux environment: ubuntu
---------------------------------------------

Add Docker's official GPG key:
==============================

.. code-block:: console

    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

Add the repository to Apt sources:
==================================

.. code-block:: console

    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update


Running the gitlab-runner in a docker container
-----------------------------------------------
.. code-block:: console

    docker run -d --name gitlab-runner --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v gitlab-runner-config:/etc/gitlab-runner \
    gitlab/gitlab-runner:latest

Register the runner
===================

.. code-block:: console

    docker exec -it gitlab-runner gitlab-runner register

After completing the register the runner is now available. Look at the ci/cd setting in the runner section

Configure your pipeline
=======================

.. note::
    
    Add the .gitlab-ci.yml file in the repository

.. code-block:: javascript
    
    image : python:3.10

    stages:
        - code-check

    before_script:
        - apt update
        - python3.10 -m pip install pylint
        - cd ..


    code-analysis:
        stage: code-check
        script :
            - pylint --recursive=y riverapp --disable=R0901,W0613,C0114,E0611 --fail-under=3 --class-attribute-naming-style=snake_case



