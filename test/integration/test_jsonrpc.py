import pytest
import sys
import os
import re
os.environ['WATCHMAN_ENV'] = 'test'
os.environ['WATCHMAN_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_watchman.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from biblepayd import BiblepayDaemon
from biblepay_config import BiblepayConfig


def test_biblepayd():
    config_text = BiblepayConfig.slurp_config_file(config.biblepay_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'3b4431310395638c0ed65b40ede4b110d8da70fcc0c2ed4a729fb8e4d78b4452'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'122f423f0912850a871c58f1533dd80be62154bb0c56dfb8cb9ae2b957d1ac10'
                             
    creds = BiblepayConfig.get_rpc_creds(config_text, network)
    biblepayd = BiblepayDaemon(**creds)
    assert biblepayd.rpc_command is not None

    assert hasattr(biblepayd, 'rpc_connection')

    # Biblepay testnet block 0 hash == 3b4431310395638c0ed65b40ede4b110d8da70fcc0c2ed4a729fb8e4d78b4452
    # test commands without arguments
    info = biblepayd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert biblepayd.rpc_command('getblockhash', 0) == genesis_hash
