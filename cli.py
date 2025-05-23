import click
from minivcs.core import init_repo

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize a new MiniVCS repository."""
    init_repo()

if __name__ == "__main__":
    cli()
