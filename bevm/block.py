from eth_hash.auto import keccak
from rlp import encode, decode


class Block:
    __slots__ = (
        'action',
        'state_root',
    )

    def __init__(self, action, state_root):
        self.action = action
        self.state_root = state_root

    def rlp_encode(self):
        return encode((
            self.action.rlp_encode(),
            self.state_root,
        ))

    @classmethod
    def rlp_decode(cls, data):
        pass

    @property
    def blockhash(self):
        return keccak(self.rlp_encode())
