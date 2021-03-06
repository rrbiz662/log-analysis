# log-analysis
This project uses the `pyscopg2` library to query a mock PostgreSQL database for information on fictional news articles. 
The queries provide data on the top articles, top authors, and daily requests error percentage.

## Getting Started
These instructions will get you a copy of the project on your local machine for development and/or testing purposes.

### Prerequisites
To use the `VirtualBox` virtual machine (VM) the user will require [VirtualBox 5.1.34](https://www.virtualbox.org/wiki/Downloads)
or higher and [Vagrant 1.9.2](https://www.vagrantup.com/downloads.html) or higher . 

To run the python script the user will require `Python 3.6.4` or higher.

### Installing
To get a copy of the project to work on locally, the user can either `download the zip` or `clone the repository`.

### Initial Setup
In order for the python script to run correctly, two views need to be created on the `news` database. To create these views:
1) Open Terminal/Powershell.
2) Using the `cd` command, navigate to the directory where the project `Vagrantfile` is located.
3) Start the VM by using the `vagrant up` command.
4) Connect to the VM using the `vagrant ssh` command.
5) Navigate to the directory in the VM where the `newsdata.sql` file is located using the command `cd`.
6) Load the data into `news` database using the command `psql -d news -f newsdata.sql`.
7) Connect to the `news` database using the command `psql -d news`.
8) Create first view using the command: 
```sql
CREATE VIEW log_requests AS SELECT log.time::date as date, COUNT(*) as total FROM log GROUP BY log.time::date ORDER BY log.time::date;
```
9) Create second view using command
```sql
CREATE VIEW log_errors AS SELECT log.time::date as date, COUNT(*) as errors FROM log WHERE log.status != '200 OK' GROUP BY log.time::date  ORDER BY log.time::date;
```
10) Disconnect from the database using the command `\q`.

## Run the Project
In order to run the project:
1) Open Terminal/Powershell.
2) Using the `cd` command, navigate to the directory where the project `Vagrantfile` is located.
3) Start the VM by using the command `vagrant up`.
4) Connect to the VM using the command `vagrant ssh`.
5) Navigate to the directory in the VM where the python script is located using the command `cd`.
6) Run the python script using the command `python3 news_data_analysis.py`.

## Built with
* `Python 3.6.4`
* PostgreSQL database adapter - `psycopg 2.7`

## Authors
* Ricardo Rivera
