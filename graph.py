# Walk Score coding challenge: reduce a directed graph by eliminating
# nodes with exactly one input and one output edge.
# Copyright (c) 2014 Peter Hornyack

# How should we represent the graph once we have read in the edge list?
# There are two basic structures for representing a graph: an adjacency
# matrix, which uses a two-dimensional array to mark which edges are
# present or not in the graph, or adjacency lists, where one list of
# outgoing edges is kept for every node. For this particular challenge,
# it seems like adjacency lists are appropriate, since they are easy
# to work with and the creation of an adjacency matrix is made a bit
# trickier due to not knowing the number of nodes and their names
# in advance. For very large + sparse graphs I think there are more
# sophisticated structures out there, but that's probably overkill for
# now.
#
# How should we hold the edge lists? A map/dict using the edge ID as
# the key seems simple and efficient. To make the "reduce" algorithm
# more efficient, we will need to know the counts of both incoming and
# outgoing edges for each node. Does this mean that we should keep two
# maps, one for incoming edges and one for outgoing edges, or is it
# sufficient to keep a map for outgoing edges and then keep track of
# just a count for incoming edges? Either could probably work, but it
# seems like the reduce algorithm may be faster if we keep both maps.

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

        edgemap = dict()

        return

    def to_file(self, outfile):
        """Writes edges from the edgemap to the open writeable file
        @outfile.
        """

        return

    def reduce_graph(self):

        return

