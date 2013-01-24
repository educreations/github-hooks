#!/usr/bin/env python

import argparse
import json
import os

from github import Github


class Hooks(object):

    def __init__(self, filename='hooks.json'):
        self.filename = filename
        self.hooks = None

    def load(self):
        with open(self.filename, 'r') as f:
            data = f.read()

        self.hooks = json.loads(data)

    def dump(self):
        assert len(self.hooks) > 0, "We have to have some hooks to dump!"
        data = json.dumps(self.hooks, indent=4)
        with open(self.filename, 'w') as f:
            f.write(data)

    @classmethod
    def hooks_for_repo(cls, repo):
        return dict(
            (hook.name, hook)
            for hook in repo.get_hooks()
            if hook.active
        )

    def create_or_update_hooks_for_repo(self, repo):
        print("  Configuring hooks for " + repo.name + ":")
        repo_hooks = self.hooks_for_repo(repo)

        for name, data in self.hooks.items():
            if name not in repo_hooks:
                print("  - creating %s hook..." % name)
                repo.create_hook(
                    name=name,
                    config=data['config'],
                    active=True,
                    events=data['events'],
                )
            else:
                print("    - editing %s hook..." % name)
                # Make sure hooks are configured correctly
                hook = repo_hooks.get(name)
                hook.edit(name=name, config=data['config'], events=data['events'])

    def set_hooks_on_repo(self, repo):
        print("  Setting hooks for " + repo.name + ":")
        repo_hooks = self.hooks_for_repo(repo)

        # Remove all repo hooks
        for name, hook in repo_hooks.items():
            hook.delete()

        # Create / update all hooks on the repo
        self.create_or_update_hooks_for_repo(repo)


if __name__ == '__main__':

    for v in ('GITHUB_USER', 'GITHUB_PASSWORD', 'GITHUB_ORGANIZATION'):
        if os.environ.get(v) is None:
            print("%s is a required environment variable. Set and re-run" % v)
            exit(-1)

    parser = argparse.ArgumentParser(description="Configure repository hooks on GitHub")
    parser.add_argument('-l', '--location', help="The path to the file to store the hooks at.", default="hooks.json")
    parser.add_argument('-d', '--download', help="The name of a repository to download hooks from.")
    parser.add_argument('-f', '--force', action='store_true', help="Overwrite all hooks on all organization repos.")
    parser.add_argument('-u', '--username', default=os.environ.get('GITHUB_USER'), help="A GitHub username.")
    parser.add_argument('-p', '--password', default=os.environ.get('GITHUB_PASSWORD'), help="A GitHub password.")
    parser.add_argument('-o', '--organization', default=os.environ.get('GITHUB_ORGANIZATION'), help="A GitHub organization name.")

    args = parser.parse_args()

    if not args.username or not args.password or not args.organization:
        print("Username, password and organization are required on the command line or environment variables!")
        parser.print_help()
        exit(-1)

    # Create the API client
    gh = Github(args.username, args.password)

    # Get the organization
    org = gh.get_organization(args.organization)

    hooks = Hooks(filename=args.location)

    # Get the list of the repositories
    repos = [r for r in org.get_repos()]

    if args.download:
        print("Downloading hooks from repo {}...".format(args.download))

        # Download the hooks from the repo specified by args.download
        try:
            repo = [r for r in repos if r.name == args.download][0]
        except IndexError:
            print("Could not find the repository {}! Make sure it is correct.".format(args.download))
            parser.print_help()
            exit(-1)

        repo_hooks = Hooks.hooks_for_repo(repo)

        new_hooks = dict(
            (name, {
                'config': hook.config,
                'events': hook.events,
            })
            for name, hook in repo_hooks.items()
        )

        # Save the hooks to the file
        hooks.hooks = new_hooks
        hooks.dump()
    elif args.force:
        hooks.load()
        print("Forcing all hooks to the base set...")

        for repo in repos:
            hooks.set_hooks_on_repo(repo)
    else:
        hooks.load()
        print("Updating the hooks for all repos...")

        # Create or update the hooks on each repo
        for repo in repos:
            hooks.create_or_update_hooks_for_repo(repo)

        # List any hooks not in the base set
        for repo in repos:
            repo_hooks = [h for h in repo.get_hooks() if h.name not in hooks.hooks]
            if not repo_hooks:
                continue
            print("The following hooks exist in %s, but are not part of"
                " the base set" % repo.name)
            for hook in repo_hooks:
                if hook.name in hooks.hooks:
                    continue
                print("    %s" % hook.name)
