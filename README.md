SRCT Bookshare
===

SRCT Bookshare is a platform for GMU students to buy and sell their textbooks.

On Contributing
---

Bookshare is still in its very early stages and needs all the help it can get. Even if you don't feel like you can be helpful with the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact any SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project lead for this project is **Eric Cawi** ( *ecawi@gmu.edu* ) and lead developer is **Michel Rouly** ( *jrouly@gmu.edu* ).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

Setting everything up for development
---
You'll need to create a mysql database 'bookshare' with username 'bookshare' and an appropriate password  to run it out of the box locally. (Otherwise, you'll need to configure it for the database of your choice in the `settings.py` file.)

Make sure to install everything you need in your virtual environment from the requirements file.

When you run `$ pip install -r requirements.txt` to install all Python modules, make sure to run `$ pip migrate website && pip migrate bids && pip migrate easy_thumbnails`.

Make sure you have elasticsearch installed on your machine. (Not pyelasticsearch). Furthermore:

> Using the standard SearchIndex, your search index content is only updated whenever you run either ./manage.py update_index or start afresh with ./manage.py rebuild_index.

Debian and Ubuntu Installation Instructions
---

Add elasticsearch to your repositories by adding the public signing key

`wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -` and adding `deb http://packages.elasticsearch.org/elasticsearch/1.3/debian stable main` to your /etc/apt/sources.list.

Now run

`$ sudo apt-get update && sudo apt-get install libldap2-dev python-dev libmysqlclient-dev python-mysqldb`elasticsearch libsasl2-dev

To-do
---

* Seller's rating
* Report listings
* Admin/moderator interface
* Professor's approval interface
* Refactor listing ui
