### iupds-appscale is a Django application

*NOTE: Requires [Virtualbox](https://www.virtualbox.org/),[Vagrant](https://www.vagrantup.com/docs/installation/index.html), [Virtualenv](http://virtualenv.readthedocs.org/en/latest/), [Node.js](http://nodejs.org/), [AppScale](https://github.com/AppScale/appscale/wiki/AppScale-on-VirtualBox),[Django](https://www.djangoproject.com/), and [Ansible](http://docs.ansible.com/ansible/intro_installation.html#installation).*

#### Setup AppScale - Full details [here](https://github.com/AppScale/appscale/wiki/AppScale-on-VirtualBox)
* `$ mkdir -p ~/appscale`
* `$ cd ~/appscale   # appscale working directory`
* `$ git clone https://github.com/AppScale/appscale-tools.git`
* `$ cd appscale-tools`
* `$ wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python` # If Python Setuptools is not install already
* `$ sudo python setup.py install`  # Detailed [AppScale-tools installation](https://github.com/AppScale/appscale-tools/wiki/Installing-the-AppScale-Tools)
* `$ cd ../`    # go back to AppScale working directory
 
### Clone this repository into AppScale working directory.
* `$ git clone https://github.com/Sunnepah/iupds-appscale.git pds`
* `$ mv pds/AppScalefile .`
* `$ mv pds/Vagrantfile .`
* `$ sudo pip install ansible` # [Ansible Installation](http://docs.ansible.com/ansible/intro_installation.html#installation), If `pip` is not yet installed [install pip](https://pip.pypa.io/en/stable/installing/)

Note: the next step will install MySQL,create db and import pds db in the VM. 
db_user, db_name and db_password can be changed here `pds/ansible/roles/ansible-mysql/defaults/main.yml`

* `$ vagrant up`
* `$ appscale up`
* `$ cd pds/`
Update the database credentials in iupds/settings.py to what you set in `pds/ansible/roles/ansible-mysql/defaults/main.yml`
* `$ sudo pip install virtualenv` 
* `$ virtualenv venv` 
* `$ source venv/bin/activate`
* `$ pip install -r requirements-local.txt`
* `$ pip install -r requirements-vendor.txt -t lib` # for AppScale deployment
* `$ npm install -g bower`
* `$ npm install`
* `$ bower install`
* `$ gulp default`
* `$ python manage.py collectstatic`

#### Cloning forked libraries
* `$ git clone https://github.com/Sunnepah/python-virtuoso.git virtuoso`
* `$ git clone https://github.com/Sunnepah/sparqlwrapper.git sparqlwrapper`

#### Deploy pds to AppScale!
* `$ cd ../`    # Return to AppScale working directory
* `$ appscale deploy pds`
You will see the deployed app url.
