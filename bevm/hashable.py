from eth_hash.auto import keccak


class Hashable:
    def rlp_encode(self):
        raise NotImplemented()

    def hash(self):
        return keccak(self.rlp_encode())
