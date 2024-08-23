from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
print(f"Dispenser Address: {dispenser.address}")

creator = algorand.account.random()
print(f"Creator Address: {creator.address}")

# Fund creator account
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000 #10 algos
    )
)

print(algorand.account.get_information(creator.address))


sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T"
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
print(f"Asset ID: {asset_id}")

receiver_acct = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000 #10 algos
    )
)

asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acct.address
        asset_id=asset_id
        amount=10
    )
)

group_txn = algorand.new_group()
group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=creator.address
        amount=1_000_000 #1 algo
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=10
    )
)

# Execute group txn
group_txn.execute()

