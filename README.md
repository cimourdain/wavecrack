Wavecrack
=========

# Description
A user-friendly Web interface to share an hashcat cracking box among multiple users with some pre-defined options.  
  
# Screenshots
* The homepage ![The homepage](screenshots/1_homepage.png?raw=true)  
* Adding an hash to crack ![Adding an hash to crack](screenshots/2_adding_an_hash.png?raw=true)  
* Seeing the results and some stats ![Seeing the results and some stats](screenshots/3_seeing_results_and_stats.png?raw=true)  
  
  
# Outine
* This Web application can be used to launch **asynchronous password cracks with hashcat**.  
* The interface tries to be as **user-friendly** as possible and facilitates the password cracking method choice and to **automate the succession of various attack modes**.  
* It also displays **statistics regarding the cracked passwords** and allows to **export the cracked password list in CSV**.  
* The application is designed to be used in a multi-user environment with a **strict segregation between the cracking results of different users**: the user authentication can be done through an **LDAP directory or basic auth**.  
  
  
# Usage
Wavecrack can be used to do the following:
* Add new password hashes, choose the **attack mode and the crack duration**
* View the **past and current cracks** for your user with **statistics and graphs**
* View the **overall load** of the platform
* Upload a **password-protected file** and extract its hash

The **attack modes** are followed in the order they are displayed on the hash submit form.  
It is also possible to stop a crack. However, **every cancelation is final.**  
A limit to the amount of **concurrent cracks** can be defined in the settings in order not to reduce the current cracks performance.  
  
# Install
## Pre-requisites
* python 2.7 (not compatible with python 3)
* LDAP
* RabbitMQ Server (for celery)
* [hashcat](https://hashcat.net/hashcat/)

### Hashcat install
Either install hashcat with your system package manager or directly download hashcat source.

If necessary:  follow [these instructions](https://bugs.kali.org/view.php?id=3432#c6062) for CPU only usage on a Kali linux host 

### LDAP
Install LDAP requirements
```
# apt-get install libsasl2-dev libldap2-dev libssl-dev 
```

### rabbitmq-server (for Celery)
Install RabbitMQ server
```
# apt-get install rabbitmq-server
```

Start the RabbitMQ server
```
# service rabbitmq-server start
```
or
```
# systemctl enable rabbitmq 
# systemctl start rabbitmq
```

### Python modules
Install project python modules
```
$ pip install -r requirements.txt
```


## Setup
### General
Setup your project var in config.py

Mandatory configurations to update:
* APP_LOCATIONS: update with your hashcat app location
* DIR_LOCATIONS: Directories locations (rules, wordlists, output etc.). See not below to use default.

Optional but recommended configurations to update (or at least to check):
* SQLALCHEMY_DATABASE_URI : Database location
* CELERY_BROKER_URL and CELERY_RESULT_BACKEND: Celery database location
* DEFAULT_USERS: users created with db create (see database section)

#### Create default locations
Instead of creating manually the required directories by the DIR_LOCATIONS config options. The manager script can automatically create all of them.

```
$ sh manager.sh init_dirs
```


### Database
First initialization

```
$ sh manager.sh init_db
```

Reset database
```
$ sh manager.sh reset_db
```

Update db (after model update)
```
$ sh manager.sh update_db
```


### Words dictionaries
#### Setup Wordlists Folder
Setup words folder in config.py (DIR_LOCATIONS/wordlists)

#### Add Dictionaries
* Download wordlists ([examples](https://hashcat.net/forum/thread-1236.html))
* Add downloaded wordlists files in the config wordlist folder.

# Launch

## Celery
* Start Celery from the application folder
```
$ celery -A worker.celery worker
```

## App
* (optional) Set FLASK_CONFIG environement variable with either "development", "testing" or "production" (development used by default)
* Launch the Flask Web server
    * Directly from the `server.py` file: this mode is not suitable for production purpose
    ```
    $ python server.py
    ```
    * With a [`wsgi script`](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/): an example of [`app.wsgi.example`](setup_resources/app.wsgi.example) is provided
    * Similarly, [`supervisorctl`](http://supervisord.org/) can be used to manage celery with a configuration file example in [`supervisorcelery.conf.example`](setup_resources/supervisorcelery.conf.example)  
  
* In order to stop the cracks after a certain amount of time, you can use the [`provided cron script`](setup_resources/cronscript.py).
  
* If you want to update the list of hashes supported, you can use the [`dedicated script`](setup_resources/extract_hashcat_examples.py) which will parse [hashcat's wiki](https://hashcat.net/wiki/doku.php?id=example_hashes) and generate an updated [hashcat_hashes.py](cracker/hashcat_hashes.py). To do so, you need to have BeautifulSoup installed on your system.

Finally, if you don't want to setup your own VM, you can use the Docker-based process described in the [`docker`](Docker/) folder.  


# Testing (in progress)

Current tested:
* Application is running
* Hashcat application can be launched
* Login

## Run testing
```
$ py.test /app/tests -x
```

# TODO
* Dict naming
* Enable LDAP login
* Crack files containing usernames
* Crack with rules
* Handle pwdump format cracking
* NTDS Upload
* Upload protected file
* Prevent hashcat launch if server is saturated
* Update readme screenshots
* Unit testing
* Archiving (with celery cron)
* Stats
* ...