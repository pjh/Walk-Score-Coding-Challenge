#! /usr/bin/env python3

# Walk Score coding challenge: reduce a directed graph by eliminating
# nodes with exactly one input and one output edge.
# Copyright (c) 2014 Peter Hornyack

import argparse
import sys

##############################################################################

def build_arg_parser():
    """Returns an ArgumentParser instance."""

    # No arguments at the moment, but prints a nice usage message when
    # -h arg is provided.
    parser = argparse.ArgumentParser(
        description=("Walk Score coding challenge: reads edge list "
            "(lines of tab-separated node IDs) from stdin, writes "
            "reduced edge list to stdout."),
        add_help=True)

    return parser

##############################################################################
# Main:
if __name__ == '__main__':
    parser = build_arg_parser()
    parser.parse_args(sys.argv[1:])

    sys.exit(0)
else:
    print('Must run stand-alone')
    sys.exit(1)
