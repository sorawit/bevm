ZERO_ADDRESS = b'\x00' * 20


def pack_tx(tx):
    '''Convert tx dictionary into raw bytes.'''
    assert tx['to'] == b'' or (len(tx['to']) == 20 and tx['to'] != ZERO_ADDRESS)
    return (
        tx['nonce'].to_bytes(8, 'big') +
        (tx['to'] if len(tx['to']) else ZERO_ADDRESS) +
        tx['value'].to_bytes(16, 'big') +
        tx['gas'].to_bytes(4, 'big') +
        tx['gas_price'].to_bytes(8, 'big') +
        tx['v'].to_bytes(1, 'big') +
        tx['r'].to_bytes(32, 'big') +
        tx['s'].to_bytes(32, 'big') +
        tx['data']
    )


def unpack_tx(data):
    '''Convert raw bytes into tx dictionary.'''
    return {
        'nonce': int.from_bytes(data[:8], 'big'),
        'to': data[8:28] if data[8:28] != ZERO_ADDRESS else b'',
        'value': int.from_bytes(data[28:44], 'big'),
        'gas': int.from_bytes(data[44:48], 'big'),
        'gas_price': int.from_bytes(data[48:56], 'big'),
        'v': int.from_bytes(data[56:57], 'big'),
        'r': int.from_bytes(data[57:89], 'big'),
        's': int.from_bytes(data[89:121], 'big'),
        'data': data[121:],
    }
