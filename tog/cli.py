from dataclasses import dataclass
import os
import click
from tog.data_asker import AskVerb, DataAsker, Resource
from tog.toggl import Toggl
from tog.data_types import TimeEntry


@dataclass
class TogConfig:
    token: str
    verbose: bool


@click.group()
@click.option(
    "--token",
    default=lambda: os.getenv("TOGGL_TOKEN"),
    help="The API token for toggle. "
    + "If omitted, will be read from $TOGGLE_TOKEN.")
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    if token is None:
        print("Expected $TOGGL_TOKEN!")
        exit()
    ctx.obj = TogConfig(token, verbose=True)


@cli.command(help="Show your basic information")
@click.pass_obj
def me(cfg: TogConfig) -> None:
    toggl = Toggl(cfg.token)

    if cfg.verbose:
        me_json = toggl.me().model_dump_json(indent=2)
        print(me_json)
    else:
        me = toggl.me()
        print(f"Hello, {me.fullname}!")


@cli.command(help="List all workspaces")
@click.pass_obj
def workspaces(cfg: TogConfig) -> None:
    for w in Toggl(cfg.token).workspaces():
        print(f"[{w.id}] {w.name}")


@cli.command(help="List all projects")
@click.pass_obj
def projects(cfg: TogConfig) -> None:
    for p in Toggl(cfg.token).projects():
        print(f"[{p.id}] {p.name}")


@cli.command(help="Start a time entry")
@click.pass_obj
def start(cfg: TogConfig) -> None:
    Toggl(cfg.token).start()


@cli.command(help="Show current time entry")
@click.pass_obj
@click.argument("verb", required=False)
@click.argument("resource", required=False)
def current(cfg: TogConfig, verb, resource) -> None:
    toggl = Toggl(cfg.token)

    match toggl.current():
        case None:
            print("No entry currently running!")

        case TimeEntry() as te if verb is not None:
            da = DataAsker()
            da.register_source("project", Resource[int](
                source=lambda: [(p.name, p.id) for p in toggl.projects()]))
            da.ask(AskVerb(verb), te, resource)

        case TimeEntry() as te:
            print(te.model_dump_json(indent=2))


@cli.command(help="Stop a time entry")
@click.pass_obj
def stop(cfg: TogConfig) -> None:
    Toggl(cfg.token).stop()


if __name__ == "__main__":
    cli()
