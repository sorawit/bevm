from bevm import BEVM
from eth_account.account import Account


ONE_ADDRESS = b'\x11' * 20
TWO_ADDRESS = b'\x22' * 20


def main():
    bevm = BEVM()
    a = Account.create('ACCOUNT_A')
    data = {
        'chainId': 494,
        'data': b'',
        'nonce': 0,
        'to': ONE_ADDRESS,
        'gas': 30000,
        'gasPrice': 1,
        'value': 10**17,
    }
    sig = Account.sign_transaction(data, a.key)
    bevm.apply_mint(bytes.fromhex(a.address[2:]), 10**18)
    bevm.apply_mint(ONE_ADDRESS, 10**18)
    bevm.apply_mint(TWO_ADDRESS, 10**18)
    bevm.apply_transaction(
        500, data['nonce'],
        data['gasPrice'],
        data['gas'],
        data['to'],
        data['value'],
        data['data'],
        v=sig.v, r=sig.r, s=sig.s)
    bevm.try_transaction(
        500,
        TWO_ADDRESS,
        data['nonce'],
        data['gasPrice'],
        data['gas'],
        data['to'],
        data['value'],
        data['data']
    )
    print(bevm.get_balance(bytes.fromhex(a.address[2:])))
    print(bevm.get_balance(ONE_ADDRESS))
    print(bevm.get_balance(TWO_ADDRESS))
    print(bevm.action_count)


if __name__ == '__main__':
    main()
