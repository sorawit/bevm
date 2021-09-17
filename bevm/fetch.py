from web3 import Web3
from eth_event import get_topic_map, decode_log


ABI = [{
    'inputs': [
        {'indexed': False, 'internalType': 'address', 'name': 'to', 'type': 'address'},
        {'indexed': False, 'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'},
    ],
    'name': 'Mint',
    'type': 'event',
}, {
    'inputs': [
        {'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'},
        {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'},
    ],
    'name': 'OwnershipTransferred',
    'type': 'event',
}, {
    'inputs': [
        {'indexed': False, 'internalType': 'uint256', 'name': 'gasPrice', 'type': 'uint256'},
    ],
    'name': 'SetGasPrice',
    'type': 'event',
}, {
    'inputs': [
        {'indexed': False, 'internalType': 'bytes', 'name': 'tx', 'type': 'bytes'},
    ],
    'name': 'Tx',
    'type': 'event',
}]


TOPIC_MAP = get_topic_map(ABI)


class Fetcher:
    def __init__(self, rpc, contract):
        if rpc.startswith('http'):
            self.web3 = Web3(Web3.HTTPProvider(rpc))
        elif rpc.startswith('ws'):
            self.web3 = Web3(Web3.WebsocketProvider(rpc))
        else:
            raise ValueError('unknown rpc format: {}'.format(rpc))
        self.contract = contract

    @property
    def block_number(self):
        return self.web3.eth.block_number

    def fetch(self, from_block, to_block=None):
        if to_block is None:
            to_block = self.block_number
        logs = self.web3.eth.get_logs({
            'address': self.contract,
            'fromBlock': from_block,
            'toBlock': to_block,
        })
        return [decode_log(log, TOPIC_MAP) for log in logs]
