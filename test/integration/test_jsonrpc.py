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
    genesis_hash = u'00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = BiblepayConfig.get_rpc_creds(config_text, network)
    biblepayd = BiblepayDaemon(**creds)
    assert biblepayd.rpc_command is not None

    assert hasattr(biblepayd, 'rpc_connection')

    # Biblepay testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
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
