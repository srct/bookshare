SRCT Bookshare
===

SRCT Bookshare is a platform for GMU students to buy and sell their textbooks.

Setting everything up for development
---
You'll need to create a mysql database 'bookshare' with username 'bookshare' and password 'password' to run it out of the box locally. (Otherwise, you'll need to configure it for the database of your choice in the `settings.py` file.)

Make sure to install everything you need in your virtual environment from the requirements file.

Then `python manage.py syncdb` and `python manage.py runserver` your way to happiness.

To-do
---

* Set up Haystack with ElasticSearch
* CSRF tokens!!
* Save searches, and display saved search results on user's home page
* Display comments on user's listings, or the comments on listings for which the user has bid.
* Make links more prevalent on the site.
* Form validation
* Seller's rating
* Comment system customization-- comment submission contingent on submission of bid (in fact, just a comment system to begin with)
* Fix the damn grid system on the create listing template so the dropdown doesn't extend across the whole stupid page
* Have title, etc fields autopopulate when user inputs ISBN
* User accounts! (and GMU authentication)
