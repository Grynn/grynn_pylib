#!/usr/bin/env python3
import toml
import subprocess
import click

@click.command()
@click.argument('version', type=click.Choice(['major', 'minor', 'patch']), default='patch')
def bump_version(version):
    with open('pyproject.toml', 'r') as f:
        data = toml.load(f)

    current_version = data['project']['version']
    major, minor, patch = map(int, current_version.split('.'))

    if version == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    data['project']['version'] = new_version

    with open('pyproject.toml', 'w') as f:
        toml.dump(data, f)

    subprocess.run(['git', 'add', 'pyproject.toml'])
    subprocess.run(['git', 'commit', '-m', f"Bump version to {new_version}"])
    subprocess.run(['git', 'tag', '-a', f"v{new_version}", '-m', f"Bump version to {new_version}"])

    print(new_version)

if __name__ == "__main__":
    bump_version()
