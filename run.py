#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run JupyterLab Bot.
"""
# Local imports
from jupyterlab_bot.config import PORT  # pylint: disable=unused-import
from jupyterlab_bot.webapp import main


if __name__ == "__main__":
    print("\nRunning JupyterLab Bot on: http://localhost:5000\n")
    print("Press Ctrl+C to exit\n\n")
    main()
