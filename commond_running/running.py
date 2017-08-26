#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-08-26

import time
import execute


def print_ts(message):
    print "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)


def run(interval):
    print_ts("-" * 100)
    print_ts("Starting every %s seconds." % interval)
    print_ts("-" * 100)
    while True:
        try:
            time_remaining = interval - time.time() % interval
            time.sleep(time_remaining)
            execute.execute()
        except Exception, e:
            print e


if __name__ == "__main__":
    interval = 5
    run(interval)
