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

@cli.command()
def log():
    """Show commit logs."""
    from minivcs.core import show_log
    show_log()

@cli.command()
def status():
    """Show the status of the working directory."""
    from minivcs.core import show_status
    show_status()

@cli.command()
@click.argument("filename")
def remove(filename):
    """Remove a file from the staging area."""
    from minivcs.core import remove_file
    remove_file(filename)

@cli.command()
@click.argument("commit_id")
def checkout(commit_id):
    """Restore files from a specific commit."""
    from minivcs.core import checkout_commit
    checkout_commit(commit_id)

@cli.command()
def diff():
    """Show differences between last commit and current staged files."""
    from minivcs.core import show_diff
    show_diff()

if __name__ == "__main__":
    cli()
