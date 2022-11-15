import asyncio
from pathlib import Path

import web3.eth
from web3 import Web3, eth
from web3.middleware import geth_poa_middleware

ERC20_ABI_FILE = Path(__file__).parent / "erc20abi.json"

from .eth import wei_to_ether
from .tail import tailfind

BLOCK_QUERY_INTERVAL = 5.0


class Scanner:
    def __init__(self, config: dict, logfile: str, from_start=False):
        self.config = config
        self.logfile = logfile
        self.from_start = from_start
        self.hashes = list()
        self.w3 = Web3(Web3.HTTPProvider(self.config["geth_address"]))
        self.contract = self.w3.eth.contract(
            self.config["glm_contract_address"],
            abi=open(ERC20_ABI_FILE, "r").read()
        )
        self.verbose = False

    async def find_transaction_hashes(self):
        async for m in tailfind(self.logfile, ".*Send transaction. hash=(.*)", self.from_start):
            transaction_hash = m.group(1)
            print("transaction sent: ", transaction_hash)
            self.hashes.append(transaction_hash)

    async def scan_blocks(self, from_block: int, to_block: int):
        if self.verbose:
            print("blocks: ", list(range(from_block, to_block+1)))
        for e in self.contract.events.Transfer.getLogs(
                {"fromBlock": from_block, "toBlock": to_block}
        ):
            hash = e["transactionHash"].hex()
            if hash in self.hashes or self.verbose:
                args = e["args"]
                print("transaction: ", {
                          "from": args["from"],
                          "to": args["to"],
                          "amount": f"{wei_to_ether(args['value']):.16}",
                          "hash": hash,
                })

    async def run(self):
        asyncio.create_task(self.find_transaction_hashes())

        previous_block_number = self.w3.eth.get_block_number() - 1

        while True:
            new_block_number = self.w3.eth.get_block_number()
            if new_block_number != previous_block_number:
                await self.scan_blocks(previous_block_number + 1, new_block_number)

            previous_block_number = new_block_number
            await asyncio.sleep(BLOCK_QUERY_INTERVAL)


async def run_scanner(config, logfile: str):
    scanner = Scanner(config, logfile)

    await scanner.run()
