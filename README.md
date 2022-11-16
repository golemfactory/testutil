
## Installation

### Initialize the environment

```bash
python3 -m venv ~/.envs/testutil
source ~/.envs/testutil/bin/activate
pip install -U pip poetry
```

### Clone the repo

```bash
git clone https://github.com/golemfactory/testutil.git
cd testutil
```

### Install

```bash
poetry install
```

## Usage

Start in another terminal and keep in the background.

```
$ testutil scan --help
Usage: testutil scan [OPTIONS] [[mainnet|mumbai|polygon|rinkeby]]

Options:
  -a, --address TEXT
  -o, --offset INTEGER  Start that many blocks back.
  -v, --verbose         Display additional info.
  --help                Show this message and exit.
```

### Scan all rinkeby GLM transfers

```
testutil scan rinkeby
```

### Scan GLM transfers for the specific address

```
testutil scan -a 0x2a14f8ae0272bd4c38ed1b40c66e88ed719dab69
```
