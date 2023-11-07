import os
import click
from tog.toggl import Toggl
from tog.data_types import TimeEntry

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
    me = Toggl(ctx.obj["token"]).me()
    print(f"Hello, {me.fullname}!")

@cli.command(help="List all workspaces")
@click.pass_context
def workspaces(ctx: click.Context) -> None:
    for w in Toggl(ctx.obj["token"]).workspaces():
        print(f"[{w.id}] {w.name}")

@cli.command(help="List all projects")
@click.pass_context
def projects(ctx: click.Context) -> None:
    for p in Toggl(ctx.obj["token"]).projects():
        print(f"[{p.id}] {p.name}")

@cli.command(help= "Start a time entry")
@click.pass_context
def start(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).start()

@cli.command(help= "Show current time entry")
@click.pass_context
def current(ctx: click.Context) -> None:
    match Toggl(ctx.obj["token"]).current():
        case None:
            print("No entry currently running!")
        case TimeEntry() as te:
            print(te.model_dump_json(indent=2))

@cli.command(help= "Stop a time entry")
@click.pass_context
def stop(ctx: click.Context) -> None:
    Toggl(ctx.obj["token"]).stop()

if __name__ == "__main__":
    cli()