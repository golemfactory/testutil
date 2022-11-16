import asyncio
import click
from typing import Optional

from .config import CONFIG
from .scanner import run_scanner


@click.group
def _cli():
    pass


@_cli.command()
@click.argument("payment-network", default="rinkeby", type=click.Choice(CONFIG.keys()))
@click.option("--address", "-a",type=str, default=None)
@click.option("--offset", "-o", type=int, default=100, help="Start that many blocks back.")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display additional info.")
def scan(payment_network: str, address: Optional[str], offset: int, verbose: bool):
    config = CONFIG.get(payment_network)
    asyncio.run(run_scanner(config, address, offset, verbose))


if __name__ == "__main__":
    _cli()
