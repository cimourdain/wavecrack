# !/usr/bin/python
# coding: utf8
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    # Running options
    HOST = 'localhost'
    PORT = 7777

    # Complex random value use to sign cookies and other things by Flask
    SECRET_KEY = "xxx"
    WTF_CSRF_SECRET_KEY = 'zzz'

    # SQL Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CELERY
    # please harden your RabbitMQ installation by removing the default "admin" and "guest" user credentials
    CELERY_BROKER_URL = 'amqp://guest:guest@0.0.0.0:5672//'
    CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite'
    CELERY_TRACK_STARTED = True
    CELERY_IGNORE_RESULT = False

    # ???
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024

    # app locations
    # in case of concat with BASE_DIR, folder values must start and end with separator "/"
    DIR_LOCATIONS = {
        # Hashcat rules directory path, by default '/usr/share/hashcat/rules/' on Kali
        'hashcat_rules': BASE_DIR + '/hashcat/rules/',
        # Wordlist directory path, by default '/usr/share/wordlists/' on Kali
        'wordlists': BASE_DIR + '/sources/words/',
        'rules': BASE_DIR + '/sources/rules/',
        # hashes
        'hashes': BASE_DIR + '/sources/hashes/',
        # Output hashcat directory path
        'hashcat_outputs': BASE_DIR + '/outputs/hashcat/',
        # Output logfiles directory path
        # 'log': BASE_DIR + '/outputs/logs/',
        # Upload user files directory
        # 'upload': BASE_DIR + '/outputs/uploads/',
        # John executable path (only used to extract the hash from uploaded encrypted files)
        # by default '/usr/sbin/john' on Kali
        # 'john': BASE_DIR + '/john/',
        'tmp': BASE_DIR + '/tmp/'

    }

    APP_LOCATIONS = {
        "hashcat": BASE_DIR + '/hashcat/hashcat64.bin',
    }

    # Hashcat rules list
    rule_name_list = ["rockyou-30000.rule"]

    """
    ADDITIONAL SETTINGS
    Default values work, but can be adjusted to your needs
    """

    # Authentication settings, choose between "None", "Basic" and "LDAP"
    AUTH_TYPE = "None"

    # Basic Auth settings, define the sha256 password of the allowed users
    DEFAULT_USERS = [{
        "name": "admin",
        "email": "admin@admin.com",
        "password": "strong_password",
        "admin": True
    }]

    # LDAP settings
    LDAP_HOST = "1.1.1.1"
    LDAP_TLS = True
    LDAP_PORT = 636
    LDAP_NAME = "My LDAP"
    LDAP_BASE_DN = "OU=xxx, OU=xxx, DC=xxx, DC=xxx"
    LDAP_SEARCH_FILTER = "(&(sAMAccountName=%s)(memberOf=CN=xxx,OU=xxx,OU=xxx,DC=xxx,DC=xxx))"

    # Separator char for hashlists/outfile
    HASHLIST_FILE_SEPARATOR = '~'

    # Maximal parallel cracking sessions
    MAX_CRACKSESSIONS = 8

    # Sleeping time when an Out Of Memory exception occured
    OOM_DELAY_SLEEP = 15 * 60

    # John dictionary/Useful to extract hash from files protected by password
    extensions_dictionary = {
        '7z': '7z2john.py',
        'pdf': 'pdf2john.py', 'doc': 'office2john.py',
        'docm': 'office2john.py',
        'dotx': 'office2john.py',
        'dotm': 'office2john.py',
        'xls': 'office2john.py',
        'xlsx': 'office2john.py',
        'ppt': 'office2john.py',
        'pptx': 'office2john.py',
        'docx': 'office2john.py',
        'odf': 'odf2john.py',
        'zip': 'zip2john'
    }
    ALLOWED_EXTENSIONS = set(extensions_dictionary.keys())

    # Crack durations timeout, in days
    CRACK_DURATIONS = [3, 7, 30]

    # Disable hashcat pot file, add "--potfile-disable" to hashcat command
    HASHCAT_DISABLE_POT_FILE = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')
    DEFAULT_USERS = [{
        "name": "admin",
        "email": "admin@admin.com",
        "password": "toto",
        "admin": True
        },
            {
            "name": "admin2",
            "email": "admin2@admin.com",
            "password": "toto",
            "admin": True
        },
        {
            "name": "user",
            "email": "user@user.com",
            "password": "toto",
            "admin": False
        },
        {
            "name": "user2",
            "email": "user2@user.com",
            "password": "toto",
            "admin": False
        }
    ]


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')


class ProductionConfig(Config):
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

