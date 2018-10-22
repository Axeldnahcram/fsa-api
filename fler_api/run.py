#!/usr/bin/env python
# coding: utf-8
"""
.. module:: albator_api:run
Albator runnable
"""

__author__ = "Axel Marchand"

# standard
import os
import logging
import logzero
from logging.handlers import TimedRotatingFileHandler
import argparse
import json
import getpass
import asyncio
# custom
from fler_api.api import Api
import uvloop

###############################################################################


def main() -> None:
    """
    .. function:: main
    Entry point
    """
    username = getpass.getuser()
    default_logfile = "/tmp/albator-api-{0}.log".format(username,)
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-l", "--logfile", default=default_logfile)
    parser.add_argument("-c", "--conf", default="config.json")
    args = parser.parse_args()

    # logging
    logger = logging.getLogger()
    loglvl = logging.INFO
    if args.verbose:
        loglvl = logging.DEBUG
    logger.setLevel(loglvl)
    logzero.loglevel(level=loglvl)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(funcName)s - %(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    persisted = TimedRotatingFileHandler(args.logfile, when="d", backupCount=7)
    persisted.setFormatter(formatter)
    logger.addHandler(persisted)

    # configuration
    cfg = {}
    if os.path.isfile(args.conf):
        with open(args.conf) as f:
            cfg = json.load(f)
    else:
        msg = "Could not load configuration."
        logger.error(msg)
        raise IOError(msg)

    try:
        # process
        api = Api(cfg)
        api.run()
    except Exception as e:
        logger.exception("Main process exited in error.")
        raise e


if __name__ == "__main__":
    main()
