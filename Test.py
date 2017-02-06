from analysis import assess_portfolio

from collections import OrderedDict
import random
import subprocess
import time
import unittest

class PortfolioTestCase:
    def __init__(self, inputs, outputs, description):
        self.inputs = inputs
        self.outputs = outputs
        self.description = description

portfolio_test_cases = [
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2010-12-31',
            symbol_allocs=OrderedDict([('GOOG', 0.2), ('AAPL', 0.3), ('GLD', 0.4), ('XOM', 0.1)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.255646784534,
            avg_daily_ret=0.000957366234238,
            stdev_daily_ret=0.0100104028,
            sharpe_ratio=1.51819243641,
            end_value=1255646.78),
        description="Wiki example 1"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2010-12-31',
            symbol_allocs=OrderedDict([('AXP', 0.0), ('HPQ', 0.0), ('IBM', 0.0), ('HNZ', 1.0)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.198105963655,
            avg_daily_ret=0.000763106152672,
            stdev_daily_ret=0.00926153128768,
            sharpe_ratio=1.30798398744,
            end_value=1198105.96),
        description="Wiki example 2"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-06-01',
            end_date='2010-12-31',
            symbol_allocs=OrderedDict([('GOOG', 0.2), ('AAPL', 0.3), ('GLD', 0.4), ('XOM', 0.1)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.205113938792,
            avg_daily_ret=0.00129586924366,
            stdev_daily_ret=0.00929734619707,
            sharpe_ratio=2.21259766672,
            end_value=1205113.93),
        description="Wiki example 3: Six month range"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2010-12-31',
            symbol_allocs=OrderedDict([('GOOG', 0.2), ('AAPL', 0.4), ('GLD', 0.2), ('XOM', 0.2)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.262285147745,
            avg_daily_ret=0.000993303139465,
            sharpe_ratio=1.3812384175,
            end_value=1262285.14),
        description="Wiki example 1 with different allocations"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2013-05-31',
            symbol_allocs=OrderedDict([('AXP', 0.3), ('HPQ', 0.5), ('IBM', 0.1), ('GOOG', 0.1)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=-0.110888530433,
            avg_daily_ret=-6.50814806831e-05,
            sharpe_ratio=-0.0704694718385,
            end_value=889111.46),
        description="Normalization check"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2010-01-31',
            symbol_allocs=OrderedDict([('AXP', 0.9), ('HPQ', 0.0), ('IBM', 0.1), ('GOOG', 0.0)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=-0.0758725033871,
            avg_daily_ret=-0.00411578300489,
            sharpe_ratio=-2.84503813366,
            end_value=924127.49),
        description="One month range"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2011-01-01',
            end_date='2011-12-31',
            symbol_allocs=OrderedDict([('WFR', 0.25), ('ANR', 0.25), ('MWW', 0.25), ('FSLR', 0.25)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=-0.686004563165,
            avg_daily_ret=-0.00405018240566,
            sharpe_ratio=-1.93664660013,
            end_value=313995.43),
        description="Low Sharpe ratio"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-01-01',
            end_date='2010-12-31',
            symbol_allocs=OrderedDict([('AXP', 0.0), ('HPQ', 1.0), ('IBM', 0.0), ('HNZ', 0.0)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=-0.191620333598,
            avg_daily_ret=-0.000718040989619,
            sharpe_ratio=-0.71237182415,
            end_value=808379.66),
        description="All your eggs in one basket"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2010-06-01',
            end_date='2011-06-01',
            symbol_allocs=OrderedDict([('AAPL', 0.1), ('GLD', 0.4), ('GOOG', 0.5), ('XOM', 0.0)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.177352039318,
            avg_daily_ret= 0.000694756409052,
            sharpe_ratio=1.10895144722,
            end_value=1177352.03),
        description="Mid-2010 to mid-2011"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2006-01-03',
            end_date='2008-01-02',
            symbol_allocs=OrderedDict([('MMM', 0.0), ('MO', 0.9), ('MSFT', 0.1), ('INTC', 0.0)]),
            start_val=1000000),
        outputs=dict(
            cum_ret=0.43732715979,
            avg_daily_ret=0.00076948918955,
            sharpe_ratio=1.26449481371,
            end_value=1437327.15),
        description="Two year range"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2006-01-03',
            end_date='2006-01-10',
            symbol_allocs=OrderedDict([('AAPL', 0.4), ('FCX', 0.3), ('CBSH', 0.2), ('QLGC', 0.1)]),
            start_val=135794),
        outputs=dict(
            cum_ret=0.06231698270,
            avg_daily_ret=0.01231179034,
            stdev_daily_ret=0.01934737763,
            sharpe_ratio=10.10181412292,
            end_value=144256.27),
        description="One week range"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2006-01-03',
            end_date='2008-01-02',
            symbol_allocs=OrderedDict([('BEAM', 0.3), ('NCC', 0.3), ('URBN', 0.2), ('VNO', 0.1), ('AMAT', 0.1)]),
            start_val=305498),
        outputs=dict(
            cum_ret=-0.15046709371,
            avg_daily_ret=-0.00025986228,
            stdev_daily_ret=0.01140417477,
            sharpe_ratio=-0.36172594156,
            end_value=259530.60),
        description="Five stocks over two year range"
    ),
    PortfolioTestCase(
        inputs=dict(
            start_date='2005-04-29',
            end_date='2016-04-01',
            symbol_allocs=OrderedDict([('SPY', 1.0)]),
            start_val=100000),
        outputs=dict(
            cum_ret=0.43843395099,
            avg_daily_ret=0.00029799727,
            stdev_daily_ret=0.01430916718,
            sharpe_ratio=0.33059645925,
            end_value=143843.39),
        description="Should I have puchased my houe or the S&P 500?"
    )
]

class TestAnalysisCode(unittest.TestCase):
    def assess_portfolio_helper(self, test):
        return assess_portfolio(sd=test.inputs['start_date'],
            ed=test.inputs['end_date'],
            syms=test.inputs['symbol_allocs'].keys(),
            allocs=test.inputs['symbol_allocs'].values(),
            sv=test.inputs['start_val'])

    def test_assess_portfolio_cumulative_return(self):
        for test in portfolio_test_cases:
            expected = test.outputs['cum_ret']
            cr, adr, sddr, sr, ev = self.assess_portfolio_helper(test)
            actual = cr
            self.assertAlmostEqual(expected, actual, delta=.00000000001)

    def test_assess_portfolio_average_daily_return(self):
        for test in portfolio_test_cases:
            expected = test.outputs['avg_daily_ret']
            cr, adr, sddr, sr, ev = self.assess_portfolio_helper(test)
            actual = adr
            self.assertAlmostEqual(expected, actual, delta=.00000000001)

    def test_assess_portfolio_stdev_daily_return(self):
        for test in portfolio_test_cases:
            if 'stdev_daily_ret' not in test.outputs:
                continue
            expected = test.outputs['stdev_daily_ret']
            cr, adr, sddr, sr, ev = self.assess_portfolio_helper(test)
            actual = sddr
            self.assertAlmostEqual(expected, actual, delta=.00000000001)

    def test_assess_portfolio_sharpe_ratio(self):
        for test in portfolio_test_cases:
            expected = test.outputs['sharpe_ratio']
            cr, adr, sddr, sr, ev = self.assess_portfolio_helper(test)
            actual = sr
            self.assertAlmostEqual(expected, actual, delta=.00000000001)

    def test_assess_portfolio_end_value(self):
        for test in portfolio_test_cases:
            expected = test.outputs['end_value']
            cr, adr, sddr, sr, ev = self.assess_portfolio_helper(test)
            actual = ev
            self.assertAlmostEqual(expected, actual, delta=.01)

    def test_performance(self):
        start = time.time()
        for test in portfolio_test_cases:
            self.assess_portfolio_helper(test)
        end = time.time()
        self.assertLess(end - start, 5.)

if __name__ == "__main__":
    unittest.main()