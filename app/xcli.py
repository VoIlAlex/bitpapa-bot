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


@cli.group("start")
def start_group():
    ...


@start_group.command("offer_updater")
def start_offer_updater():
    from tasks.update_offer import TaskUpdateOffer
    TaskUpdateOffer.start_loop()


@start_group.command("price_updater")
def start_price_updater():
    from tasks.update_price_info import TaskUpdatePriceInfo
    TaskUpdatePriceInfo.start_loop()


@start_group.command("trade_handler")
def start_trade_handler():
    from tasks.handle_trade import TaskHandleTrade
    TaskHandleTrade.start_loop()


@start_group.command("course_updater")
def start_course_updater():
    from tasks.update_course import TaskUpdateCourse
    TaskUpdateCourse.start_loop()


@start_group.command("new_trades_fetcher")
def new_trades_fetcher():
    from tasks.fetch_new_trades import TaskFetchNewTrades
    TaskFetchNewTrades.start_loop()


if __name__ == '__main__':
    cli()
