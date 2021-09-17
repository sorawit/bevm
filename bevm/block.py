from dataclasses import dataclass
from os import times
from eth_hash.auto import keccak
from rlp import encode, decode
from rlp.sedes import big_endian_int
from bevm import action

from bevm.action import MintAction, TransactionAction
from bevm.hashable import Hashable


@dataclass
class Block(Hashable):
    timestamp: int
    action_hash: bytes
    state_root: bytes

    def rlp_encode(self):
        return encode((
            big_endian_int.serialize(self.timestamp),
            self.action_hash,
            self.state_root,
        ))

    @classmethod
    def rlp_decode(cls, data):
        (timestamp, action_hash, state_root) = decode(data)
        return cls(
            big_endian_int.deserialize(timestamp),
            action_hash,
            state_root,
        )
