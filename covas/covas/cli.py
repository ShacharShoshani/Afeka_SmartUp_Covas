import click
from covas.manager import switch_profile, initialize, inspect_environment
from covas.state import load_active_profile

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Covas: Manage Claude Code profiles with ease.
    """
    pass

@cli.command()
def status():
    """Show the currently active profile."""
    active_profile = load_active_profile()
    if active_profile:
        click.echo(f"Active profile: {click.style(active_profile, fg='cyan', bold=True)}")
    else:
        click.secho("No active profile set. Use 'covas switch <profile>' to set one.", fg="yellow")

@cli.command()
@click.argument("profile")
def switch(profile):
    """Switch to a specific profile."""
    switch_profile(profile)

@cli.command()
@click.argument("profile")
def apply(profile):
    """Alias for 'switch'."""
    switch_profile(profile)

@cli.command()
def init():
    """Initialize Covas directories (~/.claude and ~/.covas)."""
    initialize()

@cli.command()
def inspect():
    """Inspect the current environment, links, and secrets."""
    inspect_environment()

if __name__ == "__main__":
    cli()