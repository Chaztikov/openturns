#! /usr/bin/env python

from __future__ import print_function
from openturns import *

TESTPREAMBLE()
RandomGenerator.SetSeed(0)

try:
    # Instanciate one distribution object
    print("begin histo comp test")
    l = [1.0, 0.7, 1.2, 0.9]
    h = [0.5, 1.5, 3.5, 2.5]
    distribution = Histogram(-1.5, l, h)
    print("Distribution ", repr(distribution))
    print("Distribution ", distribution)

    # Is this distribution elliptical ?
    print("Elliptical = ", distribution.isElliptical())

    # Is this distribution continuous ?
    print("Continuous = ", distribution.isContinuous())

    # Test for realization of distribution
    oneRealization = distribution.getRealization()
    print("oneRealization=", repr(oneRealization))

    # Test for sampling
    size = 10000
    oneSample = distribution.getSample(size)
    print("oneSample first=", repr(oneSample[0]), " last=", repr(oneSample[1]))
    print("mean=", repr(oneSample.computeMean()))
    print("covariance=", repr(oneSample.computeCovariance()))

    size = 100
    for i in range(2):
        msg = ''
        if FittingTest.Kolmogorov(distribution.getSample(size), distribution).getBinaryQualityMeasure():
            msg = "accepted"
        else:
            msg = "rejected"
        print(
            "Kolmogorov test for the generator, sample size=", size, " is", msg)
        size *= 10

    # Define a point
    point = NumericalPoint(distribution.getDimension(), 1.0)
    print("Point= ", repr(point))

    # Show PDF and CDF at point
    eps = 1e-5
    # derivative of PDF with regards its arguments
    DDF = distribution.computeDDF(point)
    print("ddf     =", repr(DDF))
    # by the finite difference technique
    print("ddf (FD)=", repr(NumericalPoint(1, (distribution.computePDF(
        point + NumericalPoint(1, eps)) - distribution.computePDF(point + NumericalPoint(1, -eps))) / (2.0 * eps))))

    # PDF value
    LPDF = distribution.computeLogPDF(point)
    print("log pdf=%.6f" % LPDF)
    PDF = distribution.computePDF(point)
    print("pdf     =%.6f" % PDF)
    # by the finite difference technique from CDF
    print("pdf (FD)=%.6f" % ((distribution.computeCDF(point + NumericalPoint(1, eps)) -
                              distribution.computeCDF(point + NumericalPoint(1, -eps))) / (2.0 * eps)))

    # derivative of the PDF with regards the parameters of the distribution
    CDF = distribution.computeCDF(point)
    print("cdf=%.6f" % CDF)
    CCDF = distribution.computeComplementaryCDF(point)
    print("ccdf=%.6f" % CCDF)

    # quantile
    quantile = distribution.computeQuantile(0.95)
    print("quantile=", repr(quantile))
    print("cdf(quantile)=%.6f" % distribution.computeCDF(quantile))
    # Get 95% survival function
    inverseSurvival = NumericalPoint(distribution.computeInverseSurvivalFunction(0.95))
    print("InverseSurvival=", repr(inverseSurvival))
    print("Survival(inverseSurvival)=%.6f" % distribution.computeSurvivalFunction(inverseSurvival))
    # Confidence regions
    threshold = NumericalPoint()
    print("Minimum volume interval=", distribution.computeMinimumVolumeInterval(0.95, threshold))
    print("threshold=", threshold)
    beta = NumericalPoint()
    levelSet = distribution.computeMinimumVolumeLevelSet(0.95, beta)
    print("Minimum volume level set=", levelSet)
    print("beta=", beta)
    print("Bilateral confidence interval=", distribution.computeBilateralConfidenceInterval(0.95, beta))
    print("beta=", beta)
    print("Unilateral confidence interval (lower tail)=", distribution.computeUnilateralConfidenceInterval(0.95, False, beta))
    print("beta=", beta)
    print("Unilateral confidence interval (upper tail)=", distribution.computeUnilateralConfidenceInterval(0.95, True, beta))
    print("beta=", beta)
    
    mean = distribution.getMean()
    print("mean=", repr(mean))
    covariance = distribution.getCovariance()
    print("covariance=", repr(covariance))
    parameters = distribution.getParametersCollection()
    print("parameters=", repr(parameters))
    for i in range(6):
        print("standard moment n=", i, " value=",
              distribution.getStandardMoment(i))
    print("Standard representative=", distribution.getStandardRepresentative())

    testSize = 0
    for i in range(testSize):
        q = RandomGenerator().Generate()
        if (fabs(q - distribution.computeCDF(distribution.computeQuantile(q))) > eps):
            print("q=%.6f" % q,  " quantile=%.6f" % distribution.computeQuantile(q)[
                  0],  " CDF(quantile)=%.6f" % distribution.computeCDF(distribution.computeQuantile(q)))

except:
    import sys
    print("t_Histogram.py", sys.exc_info()[0], sys.exc_info()[1])
