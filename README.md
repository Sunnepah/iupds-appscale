# iupds-appengine-django

## Installation

*NOTE: Requires [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and
[Node.js](http://nodejs.org/).*

* Fork this repository.
* `$ git clone  git@github.com:<your username>/iupds-appscale.git`
* `$ mkvirtualenv iupds-appscale`
* `$ cd iupds-appscale/`
* `$ pip install -r requirements-local.txt`
* `$ pip install -r requirements-vendor.txt -t lib`
* `$ npm install -g bower`
* `$ npm install`
* `$ bower install`
* `$ gulp default`
* `$ python manage.py migrate`
* `$ python manage.py runserver`