#!/usr/bin/env python3

import click

from MakeAnthems import makeAnthems


@click.group()
@click.option("--database", help="The path to the RLT database", required=True)
@click.option("--debug/--no-debug", default=False, help="Debug")
@click.pass_context
def cli(ctx, database, debug):
    ctx.ensure_object(dict)

    ctx.obj["DATABASE"] = database
    ctx.obj["DEBUG"] = debug


cli.add_command(makeAnthems)

if __name__ == "__main__":
    cli(obj={})
