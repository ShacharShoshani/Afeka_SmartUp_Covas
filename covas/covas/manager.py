import os
import shutil
import click
from pathlib import Path
from covas.state import save_active_profile, load_active_profile
from covas.constants import (
    HOME, CLAUDE_DIR, PROFILES_DIR, COVAS_DIR, 
    SECRETS_FILE, MANAGED_ITEMS
)

def switch_profile(profile_name):
    profile_path = PROFILES_DIR / profile_name

    if not profile_path.exists():
        click.secho(f"Error: Profile '{profile_name}' does not exist", fg="red")
        return

    try:
        CLAUDE_DIR.mkdir(exist_ok=True)
    except Exception as e:
        click.secho(f"Error creating directory {CLAUDE_DIR}: {e}", fg="red")
        return

    # Clean up existing managed items
    for item in MANAGED_ITEMS:
        target = CLAUDE_DIR / item
        try:
            if target.is_symlink() or target.is_file():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)
        except Exception as e:
            click.secho(f"Warning: Could not remove {target}: {e}", fg="yellow")

    # Apply new profile items
    for item in MANAGED_ITEMS:
        source = profile_path / item
        target = CLAUDE_DIR / item

        if not source.exists():
            click.secho(f"Warning: {item} does not exist in profile {profile_name}", fg="yellow")
            continue

        try:
            if item == "mcp.json":
                _generate_mcp_json(source, target)
            else:
                _create_link(source, target)
        except Exception as e:
            click.secho(f"Error applying {item}: {e}", fg="red")

    save_active_profile(profile_name)
    click.secho(f"Successfully switched to profile: {profile_name}", fg="green", bold=True)

def _generate_mcp_json(source, target):
    with open(source, "r") as file:
        content = file.read()

    secrets = load_required_secrets(content)

    for key, value in secrets.items():
        placeholder = f"${{{key}}}"
        content = content.replace(placeholder, value)

    with open(target, "w") as file:
        file.write(content)
    click.echo("✔ Generated mcp.json with secrets")

def _create_link(source, target):
    try:
        os.symlink(source, target)
        click.echo(f"✔ Linked {target.name}")
    except OSError:
        # Fallback to copying if symlink fails (common on Windows without dev mode)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        click.echo(f"✔ Copied {target.name} (fallback from symlink)")

def initialize():
    try:
        CLAUDE_DIR.mkdir(exist_ok=True)
        COVAS_DIR.mkdir(exist_ok=True)
        click.secho("Covas initialized successfully", fg="green")
    except Exception as e:
        click.secho(f"Initialization failed: {e}", fg="red")

def load_secrets():
    secrets = {}
    if not SECRETS_FILE.exists():
        return secrets

    try:
        with open(SECRETS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    secrets[key.strip()] = value.strip()
    except Exception as e:
        click.secho(f"Error loading secrets: {e}", fg="yellow")
    return secrets

def inspect_environment():
    click.echo("\n" + click.style("COVAS INSPECT", bold=True, reverse=True).center(40))
    
    active_profile = load_active_profile()
    if not active_profile:
        click.secho("\nNo active profile set.", fg="yellow")
        return

    click.echo(f"\nActive Profile: {click.style(active_profile, fg='cyan', bold=True)}")
    click.echo("-" * 20)

    for item in MANAGED_ITEMS:
        target = CLAUDE_DIR / item
        status = click.style("missing", fg="red")
        info = ""

        if target.exists():
            if target.is_symlink():
                source = os.readlink(target)
                status = click.style("linked", fg="green")
                info = f" -> {source}"
            else:
                status = click.style("generated/copied", fg="blue")
        
        click.echo(f"{item:12}: {status}{info}")

    click.echo("\nSecrets Status:")
    click.echo("-" * 20)
    
    mcp_template = PROFILES_DIR / active_profile / "mcp.json"
    if mcp_template.exists():
        with open(mcp_template, "r") as file:
            content = file.read()
        
        secrets = load_required_secrets(content)
        all_secrets = load_secrets()
        
        # Find all placeholders in template
        import re
        placeholders = re.findall(r"\$\{(.+?)\}", content)
        
        for p in placeholders:
            if p in all_secrets:
                click.echo(f"✔ {p}: {click.style('Found', fg='green')}")
            else:
                click.echo(f"✘ {p}: {click.style('Missing', fg='red')}")
    else:
        click.echo("No mcp.json template found for this profile.")

def load_required_secrets(content):
    all_secrets = load_secrets()
    required_secrets = {}
    for key, value in all_secrets.items():
        placeholder = f"${{{key}}}"
        if placeholder in content:
            required_secrets[key] = value
    return required_secrets