"""
    Set up defaults and read Watchman.conf
"""
import sys
import os
from biblepay_config import BiblepayConfig

default_Watchman_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../Watchman.conf')
)
Watchman_config_file = os.environ.get('WATCHMAN_CONFIG', default_Watchman_config)
Watchman_cfg = BiblepayConfig.tokenize(Watchman_config_file)
watchman_version="1.1.0"
min_biblepayd_proto_version_with_watchman_ping = 70207


def get_biblepay_conf():
    home = os.environ.get('HOME')

    biblepay_conf = os.path.join(home, ".biblepaycore/biblepay.conf")
    if sys.platform == 'darwin':
        biblepay_conf = os.path.join(home, "Library/Application Support/BiblepayCore/biblepay.conf")

    biblepay_conf = Watchman_cfg.get('biblepay_conf', biblepay_conf)

    return biblepay_conf


def get_network():
    return Watchman_cfg.get('network', 'mainnet')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('WATCHMAN_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = Watchman_cfg.get('db_host', '127.0.0.1')
    db_port = Watchman_cfg.get('db_port', None)
    db_name = Watchman_cfg.get('db_name', 'Watchman')
    db_user = Watchman_cfg.get('db_user', 'Watchman')
    db_password = Watchman_cfg.get('db_password', 'Watchman')
    db_charset = Watchman_cfg.get('db_charset', 'utf8mb4')
    db_driver = Watchman_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db


biblepay_conf = get_biblepay_conf()
network = get_network()
db = get_db_conn()
