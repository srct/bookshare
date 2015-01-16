# SRCT Bookshare

SRCT Bookshare is a platform for GMU students to buy and sell their textbooks.

## On Contributing

Bookshare is still in its very early stages and needs all the help it can get. Even if you don't feel like you can be helpful with the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact any SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project lead for this project is **Eric Cawi** ( *ecawi@gmu.edu* ) and lead developer is **Michel Rouly** ( *jrouly@gmu.edu* ).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

## Setting everything up for development

These instructions are for Debian and Ubuntu.

### Prerequisites

First, install python, Pip, and Git on your system. Python is the programming language used by Django. 'Pip' is the python package manager. Git is the version control system used for SRCT projects.

Open a terminal and run the following commands.

`sudo apt-get update`
`sudo apt-get install python`
`sudo apt-get install python-pip`
`sudo apt-get install git`

Next, we're going to download a copy of the bookshare codebase from git.gmu.edu, the SRCT code repository.

Navigate to the directory you in which you want to download the project, and run

`git clone git@git.gmu.edu:srct/bookshare.git`

### Package Installation

First, add elasticsearch to your repositories. Edit your repository sources

`sudo nano /etc/apt/sources.list`

by adding

`## elasticsearch`
`deb http://packages.elasticsearch.org/elasticsearch/1.3/debian stable main`

at the end of the file.

Next, add the repository's public signing key by running

`sudo wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -`

Next, install these packages from the standard repositories

`$ sudo apt-get update && sudo apt-get install libldap2-dev python-dev libmysqlclient-dev python-mysqldb`elasticsearch libsasl2-dev`

If prompted to install other required packages, install those as well.

### The Virtual Environment

Virtual environments are used to keep separate a projects packages from the main computer system, so you can use different versions of packages across different projects.

It's often recommended to create a special directory to store all of your virtual environments together, but some prefer keeping their virtual environment in the top level of their project's directory. If you choose the latter, make sure to keep the virtual environment folders out of version control.

Run `sudo pip install virtualenv`

to install virtualenv system-wide, and then run

`virtualenv bookshare`

to create your virtualenvironment. Activate it by running

`source bookshare/bin/activate`

in the virtualenvironment directory.

Now, the packages you need to install for bookshare are in the top level of the project's directory structure. Run

`pip install -r requirements.txt`

to install all of the packages needed for the project.

### Creating the Database

You'll need to create a mysql database 'bookshare' with username 'bookshare' and an appropriate password  to run it out of the box locally. (Otherwise, you'll need to configure it for the database of your choice in the `settings.py` file.)

make sure to run `$ pip migrate website && pip migrate bids && pip migrate easy_thumbnails`.

### Secret Settings

Copy the secret.py.template to secret.py. Follow the comment instructions provided in each file.

### Elasticsearch Configuration

> Using the standard SearchIndex, your search index content is only updated whenever you run either ./manage.py update_index or start afresh with ./manage.py rebuild_index.

### Media

A separate directory to manage user-uploaded files

# Starting up the test server

Now that your environment is configured, you cant test out the Django test server to make
sure everything works locally. Simply run the command ``$ python manage.py runserver``

### Servers

You have two options to choose from to locally serve your project.

*Apache*



*Gunicorn*

### Docker and Deployment

For server deployment, not for most local work

## To-do

The a list of to-do items is kept track of on the gitlab bookshare issues page. https://git.gmu.edu/srct/bookshare/issues
