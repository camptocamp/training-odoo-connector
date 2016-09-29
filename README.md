# Training Odoo Trello Connector

## Prerequisite

Install dependencies (debian/ubuntu):

    sudo apt-get install libxml2-dev libxslt1-dev python-dev \
      libpq-dev libjpeg-dev zlib1g-dev libsasl2-dev \
      libldap2-dev postgresql

## Installation:

Steps:

1. Go in the folder and bootstrap

        ./bootstrap.sh

1. Build

        bin/buildout

## Start Odoo:

For development:

    $ bin/start_openerp -d <db_name> 

Run the tests:

    $ bin/test_openerp -d <db_name> -u <module_to_test>

Start as a service:

    $ bin/supervisord
