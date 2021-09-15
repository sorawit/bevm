from bevm import BEVM
from eth_account.account import Account
from eth._utils.address import generate_contract_address


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
        'gasPrice': bevm.min_gas_price,
        'value': 10**17,
    }
    data2 = {
        'chainId': 494, 'data': bytes.fromhex(
            '6080604052600160005534801561001557600080fd5b5060cd806100246000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630dbe671f14603757806326121ff0146051575b600080fd5b603f60005481565b60405190815260200160405180910390f35b603f60006001600080828254606591906072565b9091555050600054919050565b60008219821115609257634e487b7160e01b600052601160045260246000fd5b50019056fea264697066735822122082dffa335e83d98686e32913d895c036794b1e622f2efdd7f765709db7d3502c64736f6c63430008070033'),
        'nonce': 1, 'to': b'', 'gas': 200000, 'gasPrice': bevm.min_gas_price, 'value': 0, }
    sig = Account.sign_transaction(data, a.key)
    sig2 = Account.sign_transaction(data2, a.key)
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
    created_address = generate_contract_address(bytes.fromhex(a.address[2:]), 1)
    bevm.apply_transaction(
        500, data2['nonce'],
        data2['gasPrice'],
        data2['gas'],
        data2['to'],
        data2['value'],
        data2['data'],
        v=sig2.v, r=sig2.r, s=sig2.s)
    res = bevm.try_transaction(
        500,
        TWO_ADDRESS,
        0,
        100000,
        created_address,
        0,
        bytes.fromhex('0dbe671f')
    )
    print(res.output.hex())
    print(bevm.get_balance(bytes.fromhex(a.address[2:])))
    print(bevm.get_balance(ONE_ADDRESS))
    print(bevm.get_balance(TWO_ADDRESS))
    print(bevm.min_gas_price)
    print(bevm.action_count)


if __name__ == '__main__':
    main()
