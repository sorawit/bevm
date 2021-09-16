from bevm import BEVM
from bevm.codec import pack_tx, unpack_tx
from eth_account.account import Account
from eth._utils.address import generate_contract_address


ZERO_ADDRESS = b'\x00' * 20
ONE_ADDRESS = b'\x11' * 20
TWO_ADDRESS = b'\x22' * 20


PK = b'3_\xaa\xe75\x0e_\xf3\xf9!\x10}\xdb\x1d\xe6%\xedI\xb8\xb7\xa6%\xa88oA\xc2\xef\xfe\xcf\xb29'
ACCOUNT = Account.privateKeyToAccount(PK)
ADDRESS = bytes.fromhex(ACCOUNT.address[2:])


txs = [{
    'type': 'mint',
    'data': {
        'to': ADDRESS,
        'value': 10 * 10**18,
    },
}, {
    'type': 'tx',
    'data': {
        'data': bytes.fromhex(
            '6080604052600160005534801561001557600080fd5b5060cd806100246000396000f3fe608060405'
            '2348015600f57600080fd5b506004361060325760003560e01c80630dbe671f14603757806326121f'
            'f0146051575b600080fd5b603f60005481565b60405190815260200160405180910390f35b603f600'
            '06001600080828254606591906072565b9091555050600054919050565b6000821982111560925763'
            '4e487b7160e01b600052601160045260246000fd5b50019056fea264697066735822122082dffa335'
            'e83d98686e32913d895c036794b1e622f2efdd7f765709db7d3502c64736f6c63430008070033',
        ),
        'nonce': 0,
        'to': b'',
        'gas': 200000,
        'gasPrice': 10**9,
        'value': 0,
        'v': 28,
        'r': 73055308187715820777495770797145639813982829386239956306302679420640191105825,
        's': 20241563366778946265093829596501884984985003012837858540191810790166056138348,
    },
}, {
    'type': 'tx',
    'data': {
        'data': bytes.fromhex('26121ff0'),
        'nonce': 1,
        'to': generate_contract_address(ADDRESS, 0),
        'gas': 200000,
        'gasPrice': 10**9,
        'value': 0,
        'v': 27,
        'r': 18844848182414713279722883788987374244597365989955746541046388714706669738070,
        's': 2844719216955992928291971831696279864260081229602310533148354655207276528596,
    },
}]


def main():
    bevm = BEVM()
    for tx in txs:
        kind = tx['type']
        data = tx['data']
        if kind == 'mint':
            bevm.apply_mint(data['to'], data['value'])
        elif kind == 'tx':
            bevm.apply_transaction(
                500, data['nonce'], data['gasPrice'], data['gas'], data['to'],
                data['value'], data['data'], data['v'], data['r'], data['s'],
            )
        print(bevm.get_balance(txs[0]['data']['to']))
    print(bevm.try_transaction(
        500,
        ONE_ADDRESS,
        0,
        100000,
        txs[2]['data']['to'],
        0,
        bytes.fromhex('0dbe671f')
    ).output.hex())
    print(len(pack_tx(txs[1]['data'])), pack_tx(txs[1]['data']).hex())
    print('---')
    print(txs[2]['data'])
    print(unpack_tx(pack_tx(txs[2]['data'])))
    print(txs[2]['data'] == unpack_tx(pack_tx(txs[2]['data'])))

    # print(bevm.action_count)
    # bevm.apply_transaction(
    #     500,
    #     txs[2]['data']['nonce'],
    #     txs[2]['data']['gasPrice'],
    #     txs[2]['data']['gas'],
    #     txs[2]['data']['to'],
    #     txs[2]['data']['value'],
    #     txs[2]['data']['data'],
    #     txs[2]['data']['v'],
    #     txs[2]['data']['r'],
    #     txs[2]['data']['s'],
    # )
    # print(sig0.v, sig0.r, sig0.s)
    # tx1 = txs[2]['data']
    # tx1['to'] = generate_contract_address(bytes.fromhex(a.address[2:]), 0)
    # print(tx1['to'].hex())
    # sig1 = Account.sign_transaction(tx1, a.key)
    # print(sig1.v, sig1.r, sig1.s)

    # data = {
    #     'chainId': 494,
    #     'data': b'',
    #     'nonce': 0,
    #     'to': ONE_ADDRESS,
    #     'gas': 30000,
    #     'gasPrice': bevm.min_gas_price,
    #     'value': 10**17,
    # }
    # data2 = {
    #     'chainId': 494, 'data': bytes.fromhex(
    #         '6080604052600160005534801561001557600080fd5b5060cd806100246000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630dbe671f14603757806326121ff0146051575b600080fd5b603f60005481565b60405190815260200160405180910390f35b603f60006001600080828254606591906072565b9091555050600054919050565b60008219821115609257634e487b7160e01b600052601160045260246000fd5b50019056fea264697066735822122082dffa335e83d98686e32913d895c036794b1e622f2efdd7f765709db7d3502c64736f6c63430008070033'),
    #     'nonce': 1, 'to': b'', 'gas': 200000, 'gasPrice': bevm.min_gas_price, 'value': 0, }
    # sig = Account.sign_transaction(data, a.key)
    # sig2 = Account.sign_transaction(data2, a.key)
    # bevm.apply_mint(bytes.fromhex(a.address[2:]), 10**18)
    # bevm.apply_mint(ONE_ADDRESS, 10**18)
    # bevm.apply_mint(TWO_ADDRESS, 10**18)
    # bevm.apply_transaction(
    #     500, data['nonce'],
    #     data['gasPrice'],
    #     data['gas'],
    #     data['to'],
    #     data['value'],
    #     data['data'],
    #     v=sig.v, r=sig.r, s=sig.s)
    # created_address = generate_contract_address(bytes.fromhex(a.address[2:]), 1)
    # bevm.apply_transaction(
    #     500, data2['nonce'],
    #     data2['gasPrice'],
    #     data2['gas'],
    #     data2['to'],
    #     data2['value'],
    #     data2['data'],
    #     v=sig2.v, r=sig2.r, s=sig2.s)
    # res = bevm.try_transaction(
    #     500,
    #     TWO_ADDRESS,
    #     0,
    #     100000,
    #     created_address,
    #     0,
    #     bytes.fromhex('0dbe671f')
    # )
    # print(res.output.hex())
    # print(bevm.get_balance(bytes.fromhex(a.address[2:])))
    # print(bevm.get_balance(ONE_ADDRESS))
    # print(bevm.get_balance(TWO_ADDRESS))
    # print(bevm.min_gas_price)
    # print(bevm.action_count)


if __name__ == '__main__':
    main()
