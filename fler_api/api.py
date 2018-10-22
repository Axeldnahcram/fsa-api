#!/usr/bin/env python
# coding: utf-8
"""
.. module:: fler_api.api
Api wrapper classes
"""

__author__ = "Axel Marchand"

# standard
import logging
from typing import Dict
import os
import asyncio
# installed
from aiohttp import web
from aiohttp_swagger import setup_swagger
import aiohttp_debugtoolbar
from dotenv import load_dotenv, find_dotenv
import fler_api.constants as cst
import fler_utils.commons as comm
import uvloop

# Globals
###############################################################################

LOGGER = logging.getLogger(__name__)


# Functions and Classes
###############################################################################


class Api(object):
    """
    .. class:: Api
    Boilerplate arround the run of the API
    """

    def __init__(self, cfg: Dict[str, str]) -> None:
        """
        .. constructor:: Api(cfg)
          :param cfg: Api configuration passed as parameter
        Initialize the Api boilerplate and runtime
        """
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm.store_configuration(cfg))

        self.config = cfg
        LOGGER.info(cfg)
        self.app = web.Application(loop=loop)
        # self.app.router.add_routes(routes_test.ROUTES)
        setup_swagger(self.app)

    def run(self) -> None:
        """
        .. method:: run()
        Runs the http server's loop
        """
        port = 8981
        if self.config is not None and cst.PORT in self.config:
            port = self.config[cst.PORT]

        load_dotenv(find_dotenv())
        if cst.ENV in os.environ:
            if os.environ[cst.ENV] == cst.PROD:
                web.run_app(self.app, port=port)
            elif os.environ[cst.ENV] == cst.DEV:
                aiohttp_debugtoolbar.setup(self.app)
                web.run_app(self.app, port=port)
            else:
                msg = "Runtime not supported. Must be either in prod or dev."
                LOGGER.error(msg)
                raise ValueError(msg)
        else:
            msg = "Missing ENV environment. You must define your runtime."
            LOGGER.error(msg)
            raise ValueError(msg)
