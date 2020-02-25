# SRCT Bookshare

SRCT Bookshare is a platform for GMU students to buy and sell their textbooks.

## On Contributing

While Bookshare has made its way into a beta release, it still needs all the help it can get. Even if you don't feel like you can be helpful with the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

The beta release was tagged April 26, 2015 in the master branch. All development aside from emergency exception handling and security vulnerabilities, additional test cases, and supplemental documentation should be made in the 1.0 release branch.

If you need help at all please contact any SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project lead for this project is **Daniel Bond** (*dbond2@gmu.edu* ).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

## Setting everything up for development

These instructions are for Debian and Ubuntu. Server configuration information adopted from 
Michel Rouly's [research-questions](https://github.com/jrouly/research-questions) documentation.

### Prerequisites

First, install python, Pip, and Git on your system. Python is the programming language used by Django. 'Pip' is the python package manager. Git is the version control system used for SRCT projects.

Open a terminal and run the following commands.

`sudo apt-get update`

`sudo apt-get install python python-dev python-pip git`

Next, we're going to download a copy of the bookshare codebase from git.gmu.edu, the SRCT code repository.

Configure your ssh keys by following the directions at git.gmu.edu/help/ssh/README.

Now on your computer, navigate to the directory you in which you want to download the project, and run

`git clone git@git.gmu.edu:srct/bookshare.git`

### Package Installation

Next, install these packages from the standard repositories

`$ sudo apt-get install libldap2-dev mysql-server mysql-client libmysqlclient-dev python-mysqldb libsasl2-dev libjpeg-dev redis-server`

If prompted to install additional required packages, install those as well.

When prompted to set your mysql password, it's advisable to set it as the same as your normal superuser password.

### The Virtual Environment

Virtual environments are used to keep separate a projects packages from the main computer system, so you can use different versions of packages across different projects and ease deployment server setup.

It's often recommended to create a special directory to store all of your virtual environments together, but some prefer keeping their virtual environment in the top level of their project's directory. If you choose the latter, make sure to keep the virtual environment folders out of version control.

(For example, `mkdir ~/venv`, `cd ~/venv`)

With Python 2, you had to install an additional package to create these virtual environments, but now, with Python 3, virtual environments are built in.

Run `python3 -m venv bookshare`

in your virtual environment directory to create your virtual environment. Activate it by running

`source bookshare/bin/activate`

in the virtualenvironment directory.

There are a variety of packages, from django itself to a project that helps us connect to Mason's central authentication service, that you need to install. The python package management tool is called 'pip'.

Outside of your virtual environment, depending on what operating system you are running, you may have multiple versions of python installed on your machine, which require you to specify 'python3' when excuting files. Inside your virtual environment, you should not need to run `python3` or `pip3`. If you wish to verify this, run `python --version` or `pip3 --version`.

Now, the packages you need to install for bookshare are in the top level of the project's directory structure. Run

`pip install -r requirements.txt`

to install all of the packages needed for the project.

### Creating the Database

Bookshare is configured for using a mysql database, (though you can change this in settings.py and secret.py.)
By default, the database is called 'bookshare' in the configurations, and the user, 'bookworm'.

Load up the mysql shell by running

``mysql -u root -p``

and putting in your mysql password.

Create the database by running

``CREATE DATABASE bookshare;``

You can choose a different name for your database. Double check your database was created

``SHOW DATABASES;``

Though you can use an existing user to access this database, here's how to create a new user and give them the necessary permissions to your newly created database.

``CREATE USER 'bookworm'@'localhost' IDENTIFIED BY 'password';``
For local development, password strength is less important, but use a strong passphrase for deployment. You can choose a different username.

``GRANT ALL ON bookshare.* TO 'bookworm'@'localhost';``
This allows your database user to create all the tables it needs on the bookshare database. (Each model in each app's models.py is a separate table, and each attribute a column, and each instance a row.)

``GRANT ALL ON test_bookshare.* TO 'bookworm'@'localhost';`` and then ``FLUSH PRIVILEGES;``
When running test cases, django creates a test database so your 'real' database doesn't get screwed up. This database is called 'test_' + whatever your normal database is named. Note that for permissions it doesn't matter that this database hasn't yet been created.

The .\* is to grant access all tables in the database, and 'flush privileges' reloads privileges to ensure that your user is ready to go.

Exit the mysql shell by typing `exit`.

Now, to configure your newly created database with the project settings, copy the secret.py.template in settings/ to secret.py, `cp secret.py.template secret.py`. Follow the comment instructions provided in each file to set your secret key and database info.

Run `python manage.py makemigrations` and `python manage.py migrate` to configure something called 'migrations', which allow you to make changes to the tables in your database without screwing up existing information.

The first time you run this command, you may have to specify each of the 'apps' associated with the project. The three apps that have database models are core, lookouts, and trades. Run `python manage.py makemigrations <app_name>` for each of the three.

The command generates sql syntax so you don't have to worry about the database yourself. If you wish what's created, run, for instance, `python manage.py sqlmigrate trades 0001`.

Then run `python manage.py createsuperuser` to create an admin account, using the same username and email as you'll access through CAS. Finally, run `python manage.py syncdb` to set up all the tables in your empty database.

### Configuring the Cache

#### Notes on Cacheing

Bookshare's urls are set to be cached for periods of time set so that ordinary user experience will not be impacted, but a substantial load will be lifted from a deployment server. However, this can be annoying when you're making and want to check small changes rapidly on development. You can edit the respective apps' urls.py files and remove the cacheing configurations, but make sure that you do not include such edits in any pushes!



### Email

Note: if you do not set this, the app will work 95% fine, except you will not be able to test sending email.

Amazon's Simple Email Service (SES) is set to the default on Bookshare, but these are actually generic settings that can handle any smtp server. Simply change the EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD in secret.py, and change the EMAIL_PORT if necessary in settings.py.

You will also need to change the default recipient email addresses in trades/views.py; these are set by default to Amazon's testing email address with the actual user email addresses commented out above. (The same holds for deployment; change the recipent address to send emails to the actual recipients!)

### API Keys

Optional: sending email with Amazon's SES is set to the default on Bookshare. Create an SES account and set the host, user, and password in secret.py.

Optional: if you want to upload user media files to Amazon's Simple Storage Service (S3), you can add API keys for an S3 bucket to secret.py and set MEDIA_S3 to True in settings.py.

### Haystack Configuration

When your database is empty, this won't do much good, but once you've created a few objects, run 'python manage.py update_index' to set up your database objects for search.

### Starting up the test server

Now that your environment is configured, you can test out the Django test server to make
sure everything works locally. Simply run the command ``$ python manage.py runserver``

### Docker and Deployment

For server deployment, not for most local work

This project involves the uploading of files. While any images larger than five
megapixels are automatically scaled down on upload, this does not prevent
malicious individuals from uploading a massive file first. Nginx (or your
favorite server) MUST be configured to halt upload streaming once a particular
threshold is reached.

### Servers

You have three options from which to choose to serve your project for deployment. Apache + nginix, pure Apache, or pure nginx.

### Cacheing

Bookshare is in the process of being configured to use Redis for its cacheing.

## To-do

The list of to-do items is kept track of on the gitlab bookshare issues page. https://git.gmu.edu/srct/bookshare/issues Ask the project manager if you have any questions!

## License

Copyright (C) 2013 Mason SRCT: Daniel Bond, Michel Rouly, Eric Cawi, and contributors

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See the LICENSE file in the root directory of this project for more information.
