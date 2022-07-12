from web3 import Web3, HTTPProvider
import utils.web3.abi.raffle_contract


client = Web3(HTTPProvider('https://rpc.onechain.services'))
address_raffle_token = '0x430CA8b9121b52140D271FC3589f1157c707b518'

raffle_contract = client.eth.contract(
    address=address_raffle_token,
    abi=utils.web3.abi.raffle_contract.abi
)


def fetch_events(contract, eventType, start_block, end_block, event_processor):
    addresses = {}

    filter = contract.events[eventType].createFilter(
        fromBlock=start_block,
        toBlock=end_block
    )

    events = filter.get_all_entries()

    for event in filter.get_all_entries():
        event_processor(event, addresses)

    print(f'Processed {len(events)} events from block {start_block} to {end_block}')

    return addresses


def get_block_tuples(start_block, end_block):
    iteration_block = start_block
    increments = 2000

    blocks = []

    while iteration_block < end_block:
        from_block = iteration_block
        to_block = iteration_block + increments

        if(to_block > end_block):
            to_block = end_block

        blocks.append((from_block, to_block))

        iteration_block += increments + 1

    return blocks
