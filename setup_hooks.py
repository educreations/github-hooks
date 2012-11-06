#!/usr/bin/env python

import os
from github import Github


base_hooks = {
#   'hook_name': {'config1': 'value1', 'config2': 'value2'},
}


if __name__ == '__main__':

    for v in ('GITHUB_USER', 'GITHUB_PASSWORD', 'GITHUB_ORGANIZATION'):
        if os.environ.get(v) is None:
            print "%s is a required environment variable. Set and re-run" % v
            exit(-1)

    # Create the API client
    gh = Github(
        os.environ.get('GITHUB_USER'),
        os.environ.get('GITHUB_PASSWORD')
    )

    org = gh.get_organization(os.environ.get('GITHUB_ORGANIZATION'))

    repos = org.get_repos()

    for repo in repos:
        # Get a mapping of the hooks for the repo
        hooks = dict(
            (hook.name, hook)
            for hook in repo.get_hooks()
            if hook.active
        )

        print "Configuring hooks for " + repo.name + ":"

        for name, config in base_hooks.items():
            # Set up any hooks that aren't set up
            if name not in hooks:
                print "  - creating %s hook..." % name
                repo.create_hook(
                    name=name,
                    config=config,
                    active=True,
                )
            else:
                print "  - editing %s hook..." % name
                # Make sure hooks are configured correctly
                hook = hooks.get(name)
                hook.edit(name=name, config=config)

    # List any hooks not in the base set
    for repo in repos:
        hooks = [h for h in repo.get_hooks() if h.name not in base_hooks]
        if not hooks:
            continue
        print "The following hooks exist in %s, but are not part of" \
            " the base set" % repo.name
        for hook in hooks:
            if hook.name in base_hooks:
                continue
            print "    %s" % hook.name
            #hook.delete()
