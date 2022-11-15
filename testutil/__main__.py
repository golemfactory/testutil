import asyncio
import click
import os.path
from pathlib import Path

from .config import CONFIG
from .scanner import run_scanner


@click.group
def _cli():
    pass


@_cli.command()
@click.argument(
    "payment-network",
    default="rinkeby",
    type=str,
)
@click.argument(
    "logfile",
    default=Path("~/.local/share/yagna/yagna_rCURRENT.log"),
    type=Path,
)
def scan(payment_network: str, logfile: Path):
    config = CONFIG.get(payment_network)
    logfile = os.path.expanduser(logfile)

    asyncio.run(run_scanner(config, logfile))


if __name__ == "__main__":
    _cli()
