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

In addition, you will need to configure the `base_hooks` dictionary inside of
the script. For example, if you want to add an email post commit hook, add the
following definition into the `base_hooks` dictionary:

```python
'email': {
    'secret': '',
    'address': 'list@company.com',
    'send_from_author': '0',
}
```

You would likewise do this for other hooks. Then run the script and it will
ensure those all exist on each repo in the organization.
