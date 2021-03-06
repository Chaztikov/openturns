#! /usr/bin/env python

from __future__ import print_function
from openturns import *

TESTPREAMBLE()

try:
    dim = 5
    meanPoint = Point(dim, 0.0)
    sigma = Point(dim, 5.0)
    R = CorrelationMatrix(dim)

    distribution = Normal(meanPoint, sigma, R)

    # Instanciate another distribution object
    for i in range(1, dim):
        R[i, i - 1] = -0.25

    distribution2 = Normal(meanPoint, sigma, R)

    # Test for sampling
    size = 1000
    sample = distribution.getSample(size)
    # Create an empty graph
    myGraph = Graph("Pairs", " ", " ", True, "topright")

    # Create the first cloud
    myPairs = Pairs(sample, "Pairs example",
                    sample.getDescription(), "green", "bullet")

    # Then, draw it
    myGraph.add(myPairs)
    myGraph.draw("Graph_Pairs_OT.png")

    # Check that the correct files have been generated by computing their
    # checksum

except:
    import sys
    print("t_Pairs_std.py", sys.exc_info()[0], sys.exc_info()[1])
