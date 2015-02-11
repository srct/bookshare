# SRCT Bookshare

SRCT Bookshare is a platform for GMU students to buy and sell their textbooks.

## On Contributing

Bookshare is still in its very early stages and needs all the help it can get. Even if you don't feel like you can be helpful with the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact any SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project lead for this project is **Eric Cawi** ( *ecawi@gmu.edu* ) and lead developer is **Michel Rouly** ( *jrouly@gmu.edu* ).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

## Setting everything up for development

These instructions are for Debian and Ubuntu. Server configuration information adopted from 
Michel Rouly's [research-questions](https://github.com/jrouly/research-questions) documentation.

### Prerequisites

First, install python, Pip, and Git on your system. Python is the programming language used by Django. 'Pip' is the python package manager. Git is the version control system used for SRCT projects.

Open a terminal and run the following commands.

`sudo apt-get update`
`sudo apt-get install python python-dev`
`sudo apt-get install python-pip`
`sudo apt-get install git`

Next, we're going to download a copy of the bookshare codebase from git.gmu.edu, the SRCT code repository.

Navigate to the directory you in which you want to download the project, and run

`git clone git@git.gmu.edu:srct/bookshare.git`

### Package Installation

Next, install these packages from the standard repositories

`$ sudo apt-get install libldap2-dev mysql-server mysql-client libmysqlclient-dev python-mysqldb libsasl2-dev`

If prompted to install additional required packages, install those as well.

### The Virtual Environment

Virtual environments are used to keep separate a projects packages from the main computer system, so you can use different versions of packages across different projects and ease deployment server setup.

It's often recommended to create a special directory to store all of your virtual environments together, but some prefer keeping their virtual environment in the top level of their project's directory. If you choose the latter, make sure to keep the virtual environment folders out of version control.

Run `sudo pip install virtualenv`

to install virtualenv system-wide, and then run

`virtualenv bookshare`

in your virtualenvironment directory to create your virtualenvironment. Activate it by running

`source bookshare/bin/activate`

in the virtualenvironment directory.

Now, the packages you need to install for bookshare are in the top level of the project's directory structure. Run

`pip install -r requirements.txt`

to install all of the packages needed for the project.

### Creating the Database

Bookshare is configured for using a mysql database, (though you can change this in settings.py and secret.py.)
By default, the database is called 'bookshare' in the configurations, and the user, 'bookworm'.

Load up the mysql shell by running

``mysql -u root -p``

Create the database by running

``CREATE DATABASE bookshare;``

You can choose a different name for your database. Double check your database was created

``SHOW DATABASES;``
Though you can use an existing user to access this database, here's how to create a new user and give them the necessary permissions to your newly created database.

``CREATE USER 'bookworm'@'localhost' IDENTIFIED BY 'password';``
For local development, password strength is less important, but use a strong passphrase for deployment. You can choose a different username.

``GRANT ALL ON bookshare.* TO 'bookworm'@'localhost';`` ``FLUSH PRIVILEGES;``
The .\* is to grant access all tables in the database, and 'flush privileges' reloads privileges to ensure that your user is ready to go.

Now, to configure your newly created database with the project settings, copy the secret.py.template in settings/ to secret.py. Follow the comment instructions provided in each file to set your secret key and database info.

Run `python manage.py migrate` to initally set up the tables, and then run `python manage.py createsuperuser` to create an admin account, using the same username and email as you'll access through CAS.

### Haystack Configuration

Note: Using the standard SearchIndex, your search index content is only updated whenever you run either `python manage.py update_index` or start afresh with `python manage.py rebuild_index`.

### Static and Media

Run `python manage.py collectstatic` to ready your static files, like your css and javascript.

A separate directory to manage user-uploaded files.

# Starting up the test server

Now that your environment is configured, you can test out the Django test server to make
sure everything works locally. Simply run the command ``$ python manage.py runserver``

### Servers

You have three options from which to choose to serve your project for deployment. Apache + nginix, pure Apache, or pure nginx.

#### Apache + nginx (option 1)

One of the main benefits of Apache proxy passing to an nginx application
server is that you retain the flexibility of a front-facing Apache server
along with the easy of configuration of an internal nginx application
server.

Globally install the Apache and/or the nginx webservers.

``sudo apt-get install apache2`` || ``sudo apt-get install nginx``

##### Apache config

    <VirtualHost *:80>
        ServerName bookshare.yourdomain.com
        ProxyRequests Off
        <Proxy *>
            Require all granted
        </Proxy>

        ProxyPass / http://bookshare.yourdomain.com:8000/
        ProxyPassReverse / http://bookshare.yourdomain.com:8000/

        <Location />
            Require all granted
        </Location>
    </VirtualHost>

Note that this configuration requires the module `proxy_http` to be
installed and enabled.

    $ sudo a2enmod proxy_http
    $ sudo service apache2 restart

##### nginx config

    server {
        listen 8000;
        server_name bookshare.yourdomain.com;

        location / {
            proxy_pass     http://127.0.0.1:8001/;
            proxy_redirect http://127.0.0.1:8001/ /;
            server_name_in_redirect off;

            proxy_set_header  Host       $host;
            proxy_set_header  X-Real-IP  $remote_addr;
            proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        }

        location /static/ {
            alias /path/to/install/bookshare/bookshare/static/;
        }

        location /media/ {
            alias /path/to/install/bookshare/bookshare/static/media/;
        }

    }

Note that if your Django application is being hosted in a subdirectory of
the root server (eg. http://yourdomain.com/myapp/) then your config will
need to look like this:

    server {
        ...
        location /myapp/ {
            proxy_pass     http://127.0.0.1:8001/myapp/;
            proxy_redirect http://127.0.0.1:8001/myapp/ /myapp/;
            ...
        }
    }


#### Pure Apache (option 2)

This option is slightly less simple to configure and requires Apache to be
restarted whenever a change is made, since Apache does not handle
`mod_wsgi` threading as well as nginx.

##### Apache config

    <VirtualHost *:80>
        ServerName bookshare.yourdomain.com

        Alias /static/ /path/to/install/bookshare/static/
        Alias /media/  /path/to/install/bookshare/static/media/

        <Directory /path/to/install/bookshare/static>
            Options -Indexes
            Order deny,allow
            Allow from all
        </Directory>

        <Directory /path/to/install/bookshare/media>
            Options -Indexes
            Order deny,allow
            Allow from all
        </Directory>

        WSGIScriptAlias / /path/to/install/bookshare/bookshare/wsgi.py
        WSGIDaemonProcess bookshare.yourdomain.com python-path=/path/to/install/bookshare:/path/to/install/.virtualenv/bookshare/lib/python2.7/site-packages
        WSGIProcessGroup bookshare.yourdomain.com

        <Directory /path/to/install/bookshare/bookshare>
            <Files wsgi.py>
                Options -Indexes
                Order deny,allow
                Allow from all
            </Files>
        </Directory>
    </VirtualHost>

#### Pure nginx (option 3)

This option is very simple to configure. Simply make use of the nginx
configuration from option 1, but direct the server to listen on port 80 for
standard http connections instead of 8000.

### Starting the application server (nginx only)

If you use nginx to proxy pass to an application server on port 8001, you
will need to start that application server.

The project requirements include the `gunicorn` module, so let's use this.

    $ gunicorn bookshare.wsgi -b 127.0.0.1:8001

To send the web server to the background (ie. run it as a daemon) use

    $ gunicorn bookshare.wsgi -b 127.0.0.1:8001 -D

Make sure to execute this command in the same folder containing `manage.py`.

This step is not required for configurations using **only** Apache, since
those configurations use Apache to serve the entire Python application.
Note, however, that you will need to restart Apache entirely every time a
modification is made to the application / system.

### Docker and Deployment

For server deployment, not for most local work

## To-do

The list of to-do items is kept track of on the gitlab bookshare issues page. https://git.gmu.edu/srct/bookshare/issues Ask the project manager if you have any questions!
