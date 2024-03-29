from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime  # For datetime objects

import backtrader as bt

import backtest.dataloader as dt_loader
from backtest.strategy.test_strategy import TestStrategy
from backtest.strategy.turtle_strategy import (TurtleStrategy,TurtleSizer)
from backtest.strategy.grid_trading_strategy import GridTradingStrategy





def back_test_service(code,indicator):
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # # Add a backtest-TurtleStrategy
    # cerebro.addstrategy(TurtleStrategy)
    # cerebro.addsizer(TurtleSizer)
    # Add a backtest-GRID
    if code=='沪深300':
        dt =dt_loader.load_data('sh510310')
    elif code=='创业板指':
        dt = dt_loader.load_data('sz159915')
    elif code=='国防军工(申万)':
        dt = dt_loader.load_data('sh512710')
    elif code == '证券公司':
        dt = dt_loader.load_data('sh512880')
    elif code == '有色金属(申万)':
        dt = dt_loader.load_data('sh512400')
    elif code == '食品饮料(申万)':
        dt = dt_loader.load_data('sz159928')
    elif code == '中证银行':
        dt = dt_loader.load_data('sh512820')


    cerebro.addstrategy(GridTradingStrategy,code=code,indicator=indicator)
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    # start_date = datetime(2015, 1, 28)
    start_date = datetime(2022, 10, 28)

    end_date = datetime.now()
    # end_date = datetime(2022, 11, 19)

    # Create a Data Feed
    data = bt.feeds.PandasData(dataname=dt, fromdate=start_date, todate=end_date)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    # Set our desired cash start
    cerebro.broker.setcash(50000)
    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0003)
    # Print out the starting conditions
    start_money = cerebro.broker.getvalue()
    cerebro.addobserver(bt.observers.TimeReturn,timeframe=bt.TimeFrame.NoTimeFrame)
    benchdata = data
    cerebro.addobserver(bt.observers.Benchmark,
                            data=benchdata,
                            timeframe=bt.TimeFrame.NoTimeFrame)
    cerebro.addobserver(bt.observers.Benchmark,
                        data=benchdata,
                        timeframe=bt.TimeFrame.Years)
    # Run over everything
    cerebro.run()
    # Print out the final result
    end_money = cerebro.broker.getvalue()
    print('最后收益: %.2f' % (end_money - start_money))
    # Plot the result
    cerebro.plot()
