# iupds-appscale is a Django application
## Setup Instructions

*NOTE: Requires [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/), [Node.js](http://nodejs.org/), [AppScale](https://github.com/AppScale/appscale/wiki/AppScale-on-VirtualBox) and 
[Django](https://www.djangoproject.com/).*

* Fork this repository.
* `$ git clone  git@github.com:<your username>/iupds-appscale.git`
* `$ mkvirtualenv iupds-appscale`
* `$ cd iupds-appscale/`
* `$ pip install -r requirements-local.txt`  # for local
* `$ pip install -r requirements-vendor.txt -t lib` # for AppScale deployment
* `$ npm install -g bower`
* `$ npm install`
* `$ bower install`
* `$ gulp default`
* `$ python manage.py collectstaticfiles`

# Cloning forked libraries
* `$ git clone git@github.com:Sunnepah/python-virtuoso.git virtuoso`
* `$ git clone git@github.com:Sunnepah/sparqlwrapper.git sparqlwrapper`

# Install MySQL in AppScale Server
* Create database and modify the database details in iupds/settings.py
* ...

# To deploy to AppScale - AppScale must be running!
* `$ appscale deploy /path/to/iupds-appscale`
You will see the deployed app url.