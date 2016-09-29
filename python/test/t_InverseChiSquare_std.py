#! /usr/bin/env python

from __future__ import print_function
from openturns import *

TESTPREAMBLE()
RandomGenerator.SetSeed(0)

try:
    allDistributions = [InverseChiSquare(10.5), InverseChiSquare(15.0)]
    for n in range(len(allDistributions)):
        distribution = allDistributions[n]
        print("Distribution ", distribution)

        # Is this distribution elliptical ?
        print("Elliptical = ", distribution.isElliptical())

        # Is this distribution continuous ?
        print("Continuous = ", distribution.isContinuous())

        # Test for realization of distribution
        oneRealization = distribution.getRealization()
        print("oneRealization=", oneRealization)

        # Test for sampling
        size = 10000
        oneSample = distribution.getSample(size)
        print("oneSample first=", oneSample[0], " last=", oneSample[size - 1])
        print("mean=", oneSample.computeMean())
        print("covariance=", oneSample.computeCovariance())
        size = 100
        for i in range(2):
            if FittingTest.Kolmogorov(distribution.getSample(size), distribution).getBinaryQualityMeasure():
                msg = "accepted"
            else:
                msg = "rejected"
            print(
                "Kolmogorov test for the generator, sample size=", size, " is ", msg)
            size *= 10

        # Define a point
        point = NumericalPoint(
            distribution.getDimension(), 2.0 / distribution.getNu())
        print("Point= ", point)

        # Show PDF and CDF of point
        eps = 1e-5
        DDF = distribution.computeDDF(point)
        print("ddf     =", DDF)
        print("ddf (FD)=%.6g" % ((distribution.computePDF(point + NumericalPoint(1, eps)) -
                                  distribution.computePDF(point + NumericalPoint(1, -eps))) / (2.0 * eps)))
        LPDF = distribution.computeLogPDF(point)
        print("log pdf= %.12g" % LPDF)
        PDF = distribution.computePDF(point)
        print("pdf     =%.6g" % PDF)
        print("pdf (FD)=%.6g" % ((distribution.computeCDF(point + NumericalPoint(1, eps)) -
                                  distribution.computeCDF(point + NumericalPoint(1, -eps))) / (2.0 * eps)))
        CDF = distribution.computeCDF(point)
        print("cdf= %.12g" % CDF)
        CCDF = distribution.computeComplementaryCDF(point)
        print("ccdf= %.12g" % CCDF)
        Survival = distribution.computeSurvivalFunction(point)
        print("survival= %.12g" % Survival)
        CF = distribution.computeCharacteristicFunction(point[0])
        print("characteristic function=(%.6g, %.6g)" % (CF.real, CF.imag))
        LCF = distribution.computeLogCharacteristicFunction(point[0])
        print("log characteristic function=(%.6g, %.6g)" %
              (LCF.real, LCF.imag))
        PDFgr = distribution.computePDFGradient(point)
        print("pdf gradient     =", PDFgr)
        PDFgrFD = NumericalPoint(1)
        PDFgrFD[0] = (InverseChiSquare(distribution.getNu() + eps).computePDF(point) -
                      InverseChiSquare(distribution.getNu() - eps).computePDF(point)) / (2.0 * eps)
        print("pdf gradient (FD)=", PDFgrFD)
        CDFgr = distribution.computeCDFGradient(point)
        print("cdf gradient     =", CDFgr)
        CDFgrFD = NumericalPoint(1)
        CDFgrFD[0] = (InverseChiSquare(distribution.getNu() + eps).computeCDF(point) -
                      InverseChiSquare(distribution.getNu() - eps).computeCDF(point)) / (2.0 * eps)
        print("cdf gradient (FD)=", CDFgrFD)
        quantile = distribution.computeQuantile(0.95)
        print("quantile=", quantile)
        print("cdf(quantile)= %.2f" % distribution.computeCDF(quantile))
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
        print("mean=", mean)
        covariance = distribution.getCovariance()
        print("covariance=", covariance)
        correlation = distribution.getCorrelation()
        print("correlation=", correlation)
        spearman = distribution.getSpearmanCorrelation()
        print("spearman=", spearman)
        kendall = distribution.getKendallTau()
        print("kendall=", kendall)
        parameters = distribution.getParametersCollection()
        print("parameters=", parameters)
        for i in range(6):
            print("standard moment n=", i, ", value=",
                  distribution.getStandardMoment(i))
        print("Standard representative=",
              distribution.getStandardRepresentative())

        standardDeviation = distribution.getStandardDeviation()
        print("standard deviation=", standardDeviation)
        skewness = distribution.getSkewness()
        print("skewness=", skewness)
        kurtosis = distribution.getKurtosis()
        print("kurtosis=", kurtosis)

except:
    import sys
    print("InverseChiSquare.py", sys.exc_info()[0], sys.exc_info()[1])
