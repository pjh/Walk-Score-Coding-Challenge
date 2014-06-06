# Walk Score coding challenge: reduce a directed graph by eliminating
# nodes with exactly one input and one output edge.
# Copyright (c) 2014 Peter Hornyack

import re
from collections import deque

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
# the key seems simple and efficient. In the reduce algorithm we will
# need to know the counts of both incoming and outgoing edges for each
# node. Does this mean that we should keep two lists, one for incoming
# edges and one for outgoing edges, or is it sufficient to keep just a
# list for outgoing edges and then just a count of incoming edges for
# each node? It seems like either could work, but keeping both lists
# should reduce the number of lookups needed during the reduce algorithm.
#
# Future enhancements:
#   Possibly use a sorted list or binary tree for the edge lists, if
#     edge tests or deletions are common.
#   Create a separate class for the edge lists as well?
#   Define better exceptions.

# Assumption: node IDs contain one or more alphanumeric characters or
# underscores.
EDGE_RE = re.compile(r"^(?P<start>\w+)\t(?P<end>\w+)$")

class Graph:
    """Class representing a directed graph. The representation kept
    internally is optimized for the particular goal of efficiently
    'reducing' the graph, and hence will occupy more space than is
    needed for a basic directed graph.
    """

    outedges = None
    inedges = None

    def __init__(self):
        return

    def add_directed_edge(self, start, end):
        """Adds an edge from start to end. Duplicate edges are
        ignored. Returns 1 if there was already an edge between
        start and end, otherwise returns 0.
        """
        # Does this handle self-edges? Yes.
        exists_out = self._add_edge(self.outedges, start, end)
        exists_in  = self._add_edge(self.inedges, end, start)
        assert(exists_out == exists_in)
        return exists_out

    def _add_edge(self, edgemap, start, end):
        """Adds an edge from 'start' to 'end' in the specified edge
        map. Duplicate edges are ignored. Returns 1 if there was
        already an edge between start and end, otherwise returns 0.
        """
        try:
            edgelist = edgemap[start]
        except KeyError:
            edgelist = list()
            edgemap[start] = edgelist

        # For now, just use a basic list for the edge lists. In the
        # future, if tests to check for edge presence or edge deletions
        # are frequent operations, then a sorted list or BST may be
        # more appropriate.
        if end in edgelist:
            return 1
        edgelist.append(end)
        return 0

    def del_directed_edge(self, start, end):
        """Removes an edge from start to end. If there is no edge from
        start to end, raises a KeyError.
        """
        # Does this handle self-edges? Yes.
        self._del_edge(self.outedges, start, end)
        self._del_edge(self.inedges, end, start)
        return

    def _del_edge(self, edgemap, start, end):
        """Removes an edge from 'start' to 'end' in the specified
        edge map. If there is no edge from start to end, raises a
        KeyError.
        """
        try:
            edgelist = edgemap[start]
        except KeyError:
            edgelist = []
        try:
            idx = edgelist.index(end)
        except ValueError:
            raise KeyError("no edge {}<->{}".format(start, end))

        edgelist.pop(idx)
        if len(edgelist) == 0:
            edgemap.pop(start)
        return

    def from_file(self, infile):
        """Reads edge lines from the open file and fills the edge
        maps. Raises ValueError if an invalid line is encountered.
        """
        # For now, just reset these every time this method is called.
        self.outedges = dict()
        self.inedges = dict()

        line = infile.readline()
        while line:
            edge_match = EDGE_RE.match(line)
            if not edge_match:
                raise ValueError("invalid input line {}".format(line))
            start = edge_match.group('start')
            end = edge_match.group('end')

            # Note: we don't add empty lists to the outedges and
            # inedges maps here, so nodes that have only input edges
            # or only output edges may not be found in one of the maps!
            self.add_directed_edge(start, end)

            line = infile.readline()

        return

    def to_file(self, outfile):
        """Writes edges from the outgoing edge map to the specified
        open writeable file. The order of edges is arbitrary.
        """
        for (start, edgelist) in self.outedges.items():
            for end in edgelist:
                outfile.write("{}\t{}\n".format(start, end))

        return

    def reduce_graph(self):
        """'Reduces' the graph by removing nodes that have exactly
        one input and one output edge and directly connecting their
        neighbors.
        """
        # Principles from example input+output files:
        #   1) When removing a node, if an edge already exists between
        #      its neighbors, don't add another one.
        #   2) If there is a two-node cycle that is "isolated" so that each
        #      node has exactly one input edge and one output edge, then
        #      remove both nodes.
        # Other "edge" cases to think about:
        #   Self edges
        #   Disconnected components
        #
        # Given the graph representation, we can immediately search for
        # nodes with exactly one incoming edge and one outgoing edge,
        # and we know that they will be removed. Most of the time, when
        # we directly connect the neighbors, the number of incoming +
        # outgoing edges for those neighbor nodes does not change. The
        # trickiness comes when the neighbors of the removed node are
        # *already* connected by an edge - in this case, the number of
        # incoming or outgoing edges for these two neighbors has
        # decremented, so each of these nodes must be checked again!
        #
        # Sketch of algorithm:
        #   Get list of "candidate" nodes in any order.
        #   While queue of candidate nodes is not empty:
        #     Check node at head of queue: does it have exactly one input
        #     edge and one output edge? If so:
        #       Remove the node and connect its neighbors directly. If
        #       the neighbors were already connected, then append both
        #       neighbors to the end of the candidate queue. Take care
        #       with cycles.
        #   Once the candidate queue is empty, we are done: we have checked
        #   all of the nodes at least once, and we double-checked nodes
        #   whose input/output edge count changed.

        # Use a deque rather than a list for candidates: supports faster
        # pops / appends at both ends. Note that this list will not
        # actually include nodes that only have input edges; this is
        # ok (and is in fact a bit of an optimization), because they will
        # definitely not be candidates for removal.
        candidates = deque(self.outedges.keys())

        while len(candidates) > 0:
            node = candidates.popleft()

            # We could possibly reduce the number of lookups here by
            # keeping just one map and storing a tuple of (outedges,
            # inedges) as the value for each node. I actually started
            # to refactor the code to do this, but the edge add /
            # delete methods got pretty messy, so leave this as two
            # separate map lookups for now. We also perform lookups
            # in the add/delete edge methods that duplicate lookups
            # we just performed here; these could potentially be
            # optimized away too.
            try:
                outedges = self.outedges[node]
            except KeyError:
                outedges = []
            try:
                inedges = self.inedges[node]
            except KeyError:
                inedges = []

            if len(outedges) == 1 and len(inedges) == 1:
                nbr_in  = inedges[0]
                nbr_out = outedges[0]
                self.del_directed_edge(nbr_in, node)
                if node == nbr_out:
                    # Isolated self-cycles: don't try to delete the edge
                    # a second time, and don't try to add back a new edge.
                    pass
                else:
                    self.del_directed_edge(node, nbr_out)
                    already_connected = self.add_directed_edge(nbr_in,
                                                               nbr_out)
                    if already_connected == 1:
                        candidates.append(nbr_in)
                        candidates.append(nbr_out)

        return

