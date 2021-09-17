from dataclasses import dataclass
from rlp import encode, decode
from rlp.sedes import big_endian_int
from eth.constants import BLANK_ROOT_HASH
from bevm.hashable import Hashable


@dataclass
class BlockMeta(Hashable):
    action_count: int
    block_hash: bytes

    def rlp_encode(self):
        return encode((
            big_endian_int.serialize(self.action_count),
            self.block_hash,
        ))

    @classmethod
    def rlp_decode(cls, data):
        (action_count, block_hash) = decode(data)
        return cls(
            big_endian_int.deserialize(action_count),
            block_hash,
        )


@dataclass
class Block(Hashable):
    timestamp: int
    prev_block_hash: bytes
    action_hash: bytes
    min_gas_price: int
    state_root: bytes

    @classmethod
    def default(cls):
        return cls(0, b'\x00'*32, b'\x00'*32, 10**9, BLANK_ROOT_HASH)

    def rlp_encode(self):
        return encode((
            big_endian_int.serialize(self.timestamp),
            self.prev_block_hash,
            self.action_hash,
            big_endian_int.serialize(self.min_gas_price),
            self.state_root,
        ))

    @classmethod
    def rlp_decode(cls, data):
        (timestamp,  prev_block_hash, action_hash, min_gas_price, state_root) = decode(data)
        return cls(
            big_endian_int.deserialize(timestamp),
            prev_block_hash,
            action_hash,
            big_endian_int.deserialize(min_gas_price),
            state_root,
        )
