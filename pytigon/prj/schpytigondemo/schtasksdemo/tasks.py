#!/usr/bin/python

# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _

import os
import sys
import datetime
import time
from queue import Empty
from pytigon_lib.schtasks.publish import publish


import asyncio
from pytigon_lib.schtasks.remote_screen import RemoteScreen


def init_schedule(scheduler, cmd, http):
    async def hello():
        print("Hello world")

    async def hello_long():
        print("Long hello world - start")
        await asyncio.sleep(1000)
        print("Long hello world - stop")

    async def hello1(name="", scheduler=None):
        if scheduler:
            tasks = scheduler.get_tasks("hello1")
            if len(tasks) > 0:
                print(tasks[0][4])
                return
        print("Hello world 1")

    async def hello2(scheduler):
        print("Hello world 2")
        x = p / 10
        print("hello2-finished")
        # scheduler.remove_tasks('hello2')

    async def exit(scheduler):
        scheduler.clear()

    scheduler.add_task("in_minute_intervals(1)", hello)
    scheduler.add_task("in_minute_intervals(2)", hello_long)
    scheduler.add_task("in_second_intervals(3)", hello)
    scheduler.add_task("in_second_intervals(4)", hello2, scheduler)
    scheduler.add_task("hourly(at='2,3')", hello)
    scheduler.add_task("daily(at='22:07')", hello)
    scheduler.add_task("monthly(day=1, at='22:07')", hello)

    scheduler.add_task(
        "monthly(day=1, at='22:07')", hello1, name="monthly", scheduler=scheduler
    )
    scheduler.add_task(
        "daily(at='22:07', in_weekdays=(1, 2, 3, 4, 5))",
        hello1,
        name="monthly",
        scheduler=scheduler,
    )
    scheduler.add_task(
        "hourly(at=7,in_weekdays=range(1,6), in_hours=range(3,5))",
        hello1,
        name="monthly",
        scheduler=scheduler,
    )
    scheduler.add_task(
        "in_second_intervals(in_weekdays=range(1,2), in_hours=range(3,5))",
        hello1,
        name="in_second_intervals",
        scheduler=scheduler,
    )

    scheduler.add_task(
        "in_second_intervals(in_weekdays=range(1,2), in_hours=range(3,5))",
        hello2,
        scheduler,
    )

    # scheduler.add_task("in_minute_intervals(1)", exit, scheduler=scheduler)

    scheduler.add_task(
        "M(day=31, at='22:07')", hello1, name="monthly", scheduler=scheduler
    )
    scheduler.add_task("M", hello1, name="monthly", scheduler=scheduler)
