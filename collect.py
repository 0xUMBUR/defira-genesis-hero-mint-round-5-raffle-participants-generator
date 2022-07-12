import multiprocessing
import math
import utils.csv.core
import utils.json.core
import utils.web3.core


def collect_participants(start_block, end_block):
    def process_event(event, addresses):
        address = event.args['user']
        lockedTranq = math.floor(event.args['lockedStakingAmount'] / 1e18)

        addresses[address] = lockedTranq

    return utils.web3.core.fetch_events(
        utils.web3.core.raffle_contract,
        'EnterEvent',
        start_block,
        end_block,
        process_event
    )


def merge_results(results):
    merged_results = {}

    for result in results:
        merged_results.update(result)

    return merged_results


def output_to_csv(writer, participants):
    writer.writerow(['address', 'tickets'])

    for participant in participants:
        writer.writerow([participant['address'], participant['tickets']])


if __name__ == '__main__':
    # Contract creation block = 26689760 https://explorer.harmony.one/tx/0x7319260299755b2f935daa98c0fadd32db9613a730f510c6978ee8f046663705
    # Round 5 raffle end block = 26765774 https://explorer.harmony.one/tx/0x7319260299755b2f935daa98c0fadd32db9613a730f510c6978ee8f046663705

    # Initialize variables.
    blocks = utils.web3.core.get_block_tuples(26685760, 26765774)

    # Execute function in parallel.
    pool = multiprocessing.Pool()
    participants_pool = merge_results(pool.starmap(collect_participants, blocks))
    pool.close()
    pool.join()

    participants = []

    for address, lockedTranq in sorted(participants_pool.items(), key=lambda item: item[1], reverse=True):
        participants.append({
            'address': address,
            'tickets': lockedTranq
        })

    # Write results to CSV.
    utils.csv.core.write(f'participants', lambda writer: output_to_csv(writer, participants))

    # Write results to JSON.
    utils.json.core.write(f'participants', participants)
