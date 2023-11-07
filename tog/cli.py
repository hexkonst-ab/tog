import os
import click
from tog.toggl import Toggl

@click.group()
@click.option(
    "--token", 
    default=lambda: os.getenv("TOGGL_TOKEN"),
    help= "The API token for toggle. If omitted, will be read from $TOGGLE_TOKEN.")
@click.pass_context
def cli(ctx: click.Context, token: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["token"] = token 

@cli.command(help= "Show your basic information")
@click.pass_context
def me(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).me()

@cli.command(help="List all workspaces")
@click.pass_context
def workspaces(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).workspaces()

@cli.command(help= "Start a time entry")
@click.pass_context
def start(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).start()

@cli.command(help= "Stop a time entry")
@click.pass_context
def stop(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).stop()

if __name__ == "__main__":
    cli()