import click
from minivcs.core import init_repo, add_file

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize a new MiniVCS repository."""
    init_repo()

@cli.command()
@click.argument("filename")
def add(filename):
    """Add a file to the staging area."""
    add_file(filename)

@cli.command()
@click.argument("message")
def commit(message):
    """Commit the staged files with a message."""
    from minivcs.core import commit_changes
    commit_changes(message)

if __name__ == "__main__":
    cli()
