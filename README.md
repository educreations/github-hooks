# Configure GitHub Hooks

This script will quickly set up post commit hooks on all repositories in an
organization (or a user if you change a line).

## Requirements

Install the requirements for the script with:

```bash
pip install -r requirements.txt
```

## Running

To run the script, you will need several environment variables defined. These
are:

- `GITHUB_USER`
- `GITHUB_PASSWORD`
- `GITHUB_ORGANIZATION`

You can easily define them when running the script with:

```bash
GITHUB_USER='streeter' GITHUB_PASSWORD='XXXXX' GITHUB_ORGANIZATION='some-org' ./setup_hooks.py
```

Or, you can set them as arguments to the `setup_hooks.py` script. Run the script
with the `-h` option to see them all.
