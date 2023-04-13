#!/usr/local/bin/python
import asyncio

import click

from service.auth.register import RegisterService


@click.group()
def cli():
    ...


@cli.command("create_user")
@click.argument("username")
@click.argument("password")
def create_user(username: str, password: str):
    response = click.prompt(
        f"Are you sure you want to create "
        f"user with username = \"{username}\" "
        f"and password = \"{password}\" [Y/n]",
        type=str
    )
    if response and response.lower() == 'y':
        asyncio.get_event_loop().run_until_complete(
            RegisterService.register_user(
                username=username,
                password=password
            )
        )
        print("User created successfully.")
    else:
        print("Aborting.")


@cli.command("change_password")
@click.argument("username")
@click.argument("password")
def change_password(username: str, password: str):
    response = click.prompt(
        f"Are you sure you want to change "
        f"\"{username}\"'s password to \"{password}\" [Y/n]",
        type=str
    )
    if response and response.lower() == 'y':
        asyncio.get_event_loop().run_until_complete(
            RegisterService.change_password(
                username=username,
                password=password
            )
        )
        print("User's password changed successfully.")
    else:
        print("Aborting.")


if __name__ == '__main__':
    cli()
