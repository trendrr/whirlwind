#!/usr/bin/env python

from whirlwind.core.bootstrap import Bootstrap    
import os

#main app entry point
if __name__ == "__main__":
    Bootstrap.run(os.path.dirname(__file__))