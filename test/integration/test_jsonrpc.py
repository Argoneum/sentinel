import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from argoneumd import ArgoneumDaemon
from argoneum_config import ArgoneumConfig


def test_argoneumd():
    config_text = ArgoneumConfig.slurp_config_file(config.argoneum_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000019913c8bb39636467e961b8c0f4d3d656437de2cd876f2da6a05cc8d393'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000e91f3a63b1b81797a52348931a7078c0eba642bb79e64090cdf38764e83'

    creds = ArgoneumConfig.get_rpc_creds(config_text, network)
    argoneumd = ArgoneumDaemon(**creds)
    assert argoneumd.rpc_command is not None

    assert hasattr(argoneumd, 'rpc_connection')

    # Argoneum testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = argoneumd.rpc_command('getinfo')
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
    assert argoneumd.rpc_command('getblockhash', 0) == genesis_hash
