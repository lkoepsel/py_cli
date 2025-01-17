import click
import importlib
from py_cli.utils import get_version


@click.command()
@click.version_option(get_version(), prog_name="hlp")
def hlp():
    """Lists all installed CLI utilities and their descriptions."""
    utilities = ["ch", "fhc", "hc", "hw", "mf", "mfs"]

    click.echo(
        click.style(
            "Installed Utilities and Their Descriptions:", fg="green", bold=True
        )
    )
    click.echo()

    for util in utilities:
        try:
            # Import the module
            module = importlib.import_module(f"py_cli.{util}")

            # Get the click command object
            command = getattr(module, util, None)

            if command and isinstance(command, click.Command):
                name = util
                doc = command.help or "No description available"

                click.echo(click.style(f"{name}:", fg="blue", bold=True))
                click.echo(f"{doc}\n")
            else:
                click.echo(click.style(f"{util}:", fg="yellow"))
                click.echo("Not a Click command\n")

        except ImportError:
            click.echo(click.style(f"{util}:", fg="red"))
            click.echo("Unable to import module\n")