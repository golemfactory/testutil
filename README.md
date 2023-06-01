
## Installation

```
$ pipx install git+https://github.com/golemfactory/testutil.git
 installed package testutil 0.1.0, installed using Python 3.10.6
  These apps are now globally available
    - testutil
done! ✨ 🌟 ✨

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
