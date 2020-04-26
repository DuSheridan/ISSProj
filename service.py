#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from modules.app import create_app

application = create_app(os.environ.get("APP_NAME", os.path.basename(os.path.dirname(__file__))),
                         os.environ.get("ENV", "DEV"))

if __name__ == "__main__":
    application.run("0.0.0.0", port=8431)
