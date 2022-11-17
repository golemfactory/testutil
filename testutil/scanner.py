import asyncio
from pathlib import Path
from typing import Optional

from web3 import Web3
from web3.middleware import geth_poa_middleware


ERC20_ABI_FILE = Path(__file__).parent / "erc20abi.json"

from .eth import wei_to_ether

BLOCK_QUERY_INTERVAL = 5.0


def debug_middleware(make_request, w3):  # noqa
    def middleware(method, params):
        print("request", method, params)
        response = make_request(method, params)
        print("response", response)
        return response
    return middleware


class Scanner:
    address: Optional[str] = None

    def __init__(self, config: dict, address: Optional[str], verbose: bool=False, debug: bool=False):
        self.config = config
        if address:
            self.address = address.lower()
        self.verbose = verbose

        self.w3 = Web3(Web3.HTTPProvider(self.config["geth_address"]))
        if debug:
            self.w3.middleware_onion.inject(debug_middleware, layer=0)
        self.contract = self.w3.eth.contract(
            self.config["glm_contract_address"],
            abi=open(ERC20_ABI_FILE, "r").read()
        )

    async def scan_blocks(self, from_block: int, to_block: int):
        if self.verbose:
            print("blocks: ", list(range(from_block, to_block+1)))
        for e in self.contract.events.Transfer.getLogs(fromBlock=from_block, toBlock=to_block):
            tx_hash = e["transactionHash"].hex()
            args = e["args"]
            if (
                not self.address
                or self.address == args["to"].lower()
                or self.address == args["from"].lower()
            ):
                print("transaction: \n", {
                          "from": args["from"],
                          "to": args["to"],
                          "amount": f"{wei_to_ether(args['value']):.16}",
                          "hash": tx_hash,
                })

    async def run(self, offset: int):
        previous_block_number = self.w3.eth.get_block_number() - offset

        while True:
            new_block_number = self.w3.eth.get_block_number()
            if new_block_number != previous_block_number:
                await self.scan_blocks(previous_block_number + 1, new_block_number)

            previous_block_number = new_block_number
            await asyncio.sleep(BLOCK_QUERY_INTERVAL)


async def run_scanner(config, address: Optional[str], offset: int, verbose: bool, debug: bool):
    scanner = Scanner(config, address, verbose=verbose, debug=debug)
    await scanner.run(offset)
