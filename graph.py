# Walk Score coding challenge: reduce a directed graph by eliminating
# nodes with exactly one input and one output edge.
# Copyright (c) 2014 Peter Hornyack

class Graph:
    """Class representing a directed graph. The representation kept
    internally is optimized for the particular goal of efficiently
    'reducing' the graph by eliminating nodes with exactly one input
    and one output edge, and hence will occupy more space than is
    needed for a basic directed graph.
    """

    edgemap = None

    def __init__(self):
        return

    def from_file(self, infile):
        """Reads edge lines from the open file @infile and fills the
        edgemap.
        """

        return

    def to_file(self, outfile):
        """Writes edges from the edgemap to the open writeable file
        @outfile.
        """

        return

    def reduce_graph(self):

        return

