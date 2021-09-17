from dataclasses import dataclass
from rlp import encode, decode
from eth.vm.forks.berlin.transactions import BerlinTransactionBuilder


ZERO_ADDRESS = b'\x00' * 20


@dataclass
class MintAction:
    to: bytes
    value: int

    def rlp_encode(self):
        return encode((
            b'\x01',
            self.to,
            self.value.to_bytes(32, 'big'),
        ))

    @classmethod
    def rlp_decode(cls, data):
        (_, to, encoded_value) = decode(data)
        return cls(
            to,
            int.from_bytes(encoded_value, 'big')
        )


@dataclass
class TransactionAction:
    nonce: int
    to: bytes
    value: int
    gas: int
    gas_price: int
    v: int
    r: int
    s: int
    data: bytes

    def as_signed_tx(self):
        return BerlinTransactionBuilder.new_transaction(
            self.nonce, self.gas_price, self.gas, self.to, self.value, self.data,
            self.v, self.r, self.s,
        )

    def pack(self):
        return (
            self.nonce.to_bytes(8, 'big') +
            (self.to if len(self.to) else ZERO_ADDRESS) +
            self.value.to_bytes(16, 'big') +
            self.gas.to_bytes(4, 'big') +
            self.gas_price.to_bytes(8, 'big') +
            self.v.to_bytes(1, 'big') +
            self.r.to_bytes(32, 'big') +
            self.s.to_bytes(32, 'big') +
            self.data
        )

    @classmethod
    def unpack(cls, data):
        return cls(
            int.from_bytes(data[:8], 'big'),
            data[8:28] if data[8:28] != ZERO_ADDRESS else b'',
            int.from_bytes(data[28:44], 'big'),
            int.from_bytes(data[44:48], 'big'),
            int.from_bytes(data[48:56], 'big'),
            int.from_bytes(data[56:57], 'big'),
            int.from_bytes(data[57:89], 'big'),
            int.from_bytes(data[89:121], 'big'),
            data[121:],
        )

    def rlp_encode(self):
        return encode((
            b'\x02',
            self.nonce.to_bytes(8, 'big'),
            self.to,
            self.value.to_bytes(16, 'big'),
            self.gas.to_bytes(4, 'big'),
            self.gas_price.to_bytes(8, 'big'),
            self.v.to_bytes(1, 'big'),
            self.r.to_bytes(32, 'big'),
            self.s.to_bytes(32, 'big'),
            self.data,
        ))

    @ classmethod
    def rlp_decode(cls, data):
        (_, nonce, to, value, gas, gas_price, v, r, s, data) = decode(data)
        return cls(
            int.from_bytes(nonce, 'big'),
            to,
            int.from_bytes(value, 'big'),
            int.from_bytes(gas, 'big'),
            int.from_bytes(gas_price, 'big'),
            int.from_bytes(v, 'big'),
            int.from_bytes(r, 'big'),
            int.from_bytes(s, 'big'),
            data,
        )


@dataclass
class SetGasPriceAction:
    gas_price: int

    def rlp_encode(self):
        return encode((b'\x03', self.gas_price))

    @classmethod
    def rlp_decode(cls, data):
        (_, gas_price) = decode(data)
        return cls(int.from_bytes(gas_price, 'big'))


class Action:
    @staticmethod
    def rlp_decode(data):
        kind = decode(data)[0]
        if kind == b'\x01':
            return MintAction.rlp_decode(data)
        elif kind == b'\x02':
            return TransactionAction.rlp_decode(data)
        elif kind == b'\x03':
            return SetGasPriceAction.rlp_decode(data)
        else:
            raise ValueError('unknown action kind')
