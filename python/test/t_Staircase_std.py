#! /usr/bin/env python

from __future__ import print_function
from openturns import *

TESTPREAMBLE()
RandomGenerator.SetSeed(0)

try:
    # Instanciate one distribution object
    dim = 1
    meanPoint = Point(dim, 1.0)
    meanPoint[0] = 0.5
    sigma = Point(dim, 1.0)
    sigma[0] = 2.0
    R = CorrelationMatrix(dim)
    distribution1 = Normal(meanPoint, sigma, R)

    # Instanciate another distribution object
    meanPoint[0] = -1.5
    sigma[0] = 4.0
    distribution2 = Normal(meanPoint, sigma, R)

    # Test for sampling
    size = 200
    nPoints = 20
    sample1 = distribution1.getSample(size)
    sample2 = distribution2.getSample(size)

    # Construct empirical CDF for each sample
    data1 = Sample(nPoints, 2)
    data2 = Sample(nPoints, 2)
    cursor1 = Point(2)
    cursor2 = Point(2)
    for i in range(nPoints):
        cursor1[0] = 13. * i / nPoints - 6.5
        count1 = 0.
        cursor2[0] = 24. * i / nPoints - 13.5
        count2 = 0.
        for j in range(size):
            if(sample1[j, 0] < cursor1[0]):
                count1 += 1.
            if(sample2[j, 0] < cursor2[0]):
                count2 += 1.
        cursor1[1] = count1 / size
        cursor2[1] = count2 / size
        data1[i] = cursor1
        data2[i] = cursor2

    # Create an empty graph
    myGraph = Graph("Some curves", "x1", "x2", True, "bottomright")

    # Create the first staircase
    myStaircase1 = Staircase(data1, "blue", "solid", "s", "")

    myStaircase1b = Staircase(myStaircase1)
    myStaircase1b.setPattern("S")
    myStaircase1b.setColor("green")
    myStaircase1b.setLineStyle("dashed")
    myStaircase1b.setLegend("eCDF1b, pat=S")

    # Then, draw it
    myGraph.add(myStaircase1)
    myGraph.add(myStaircase1b)
    myGraph.draw("Graph_Staircase_a_OT.png")

    # Check that the correct files have been generated by computing their
    # checksum

    # Create the second staircase
    myStaircase2 = Staircase(data2, "red", "dashed", "S", "eCDF2, pat=S")

    # Add it to the graph and draw everything
    myGraph.add(myStaircase2)
    myGraph.draw("Graph_Staircase_b_OT.png")

except:
    import sys
    print("t_Staircase_std.py", sys.exc_info()[0], sys.exc_info()[1])
