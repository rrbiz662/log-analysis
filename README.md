# log-analysis-project
Source code for Log Analysis Project.

## Getting Started
These instructions will get you a copy of the project on your local machine for development and/or testing purposes.

### Prerequisites
To use the `VirtualBox` virtual machine (VM) the user will require `VirtualBox 5.1.34` or higher and `Vagrant 1.9.2` or higher . 

To run the python script the user will require `Python 3.6.4` or higher.

### Installing
To get a copy of the project to work on locally, the user can either `download the zip` or `clone the repository`.

### Initial Setup
In order for the python script to run correctly, two views need to be created on the `news` database. To create these views:
1) Open GIT Bash terminal.
2) Using the `cd` command, navigate to the directory where the project is located.
3) Start the VM by using the `vagrant up` command.
4) Connect to the VM using the `vagrant ssh` command.
5) Navigate to the directory in the VM where the python script is located with the command `cd /vagrant`
6) Connect to the `news` database using the command `psql -d news`.
7) Create first view using the command `CREATE VIEW log_requests AS SELECT log.time::date as date, COUNT(*) as total FROM log GROUP BY log.time::date ORDER BY log.time::date;`.
8) Create second view using command `
CREATE VIEW log_errors AS SELECT log.time::date as date, COUNT(*) as errors FROM log WHERE log.status != '200 OK' GROUP BY log.time::date  ORDER BY log.time::date;`.
9) Disconnect from the database using the command `\q`

## Run the Project
In order to run the project:
1) Open GIT Bash terminal.
2) Using the `cd` command, navigate to the directory where the project is located.
3) Start the VM by using the `vagrant up` command.
4) Connect to the VM using the `vagrant ssh` command.
5) Navigate to the directory in the VM where the python script is located with the command `cd /vagrant`
6) Run the python script using the command `python3 news_data_analysis.py`

## Built with
* `Python 3.6.4`
* PostgreSQL database adapter - `psycopg 2.7`

## Authors
* Ricardo Rivera