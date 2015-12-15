import yahoo_finance
from yahoo_finance import Share
import numpy

def backtest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50):
    #Create time series as list of dictionaries for specified dates
    obj = Share(ticker)
    tseries = obj.get_historical(start,end)
    tseries = list(reversed(tseries))
    # foo = pandas.read_csv('test_strat.csv')
    # tseries = foo.to_dict('records')
    # # For each day in this series update with calculated parameters
    # # and keep track of the metrics we want (total return)
    isFirstPurchase = False;
    FirstPurchase = 0;
    for i in range(len(tseries)):
    	# Change Adj_Close to a float
    	tseries[i]['Adj_Close'] = float(tseries[i]['Adj_Close'])
    	# Do nothing until we have entered the period where we know a moving average
    	if i >= duration - 1:
    		# Logic to update moving averages
    		duration_tseries = [tseries[i-j]['Adj_Close'] for j in range(duration)]
    		moving_ave = numpy.mean(duration_tseries)
    		tseries[i].update({'MA':moving_ave})
    		# Logic to OWN?
    		if tseries[i]['MA'] < tseries[i]['Adj_Close']:
    			tseries[i]['OWN'] = True
    		else:
    			tseries[i]['OWN'] = False
    		# Logic to update BUY_SELL
    		if tseries[i-1]['OWN'] and not tseries[i]['OWN']:
    			tseries[i].update({'BUY_SELL':'SELL'})
    		elif not tseries[i-1]['OWN'] and tseries[i]['OWN']:
    			tseries[i].update({'BUY_SELL':'BUY'})
    			if not isFirstPurchase:
    				FirstPurchase = tseries[i]['Adj_Close']
    				isFirstPurchase = True
    		else:
    			tseries[i].update({'BUY_SELL':''})
    		# Logic to update COST_BASIS
    		if tseries[i]['BUY_SELL'] == 'BUY':
    			tseries[i].update({'COST_BASIS':tseries[i]['Adj_Close']})
    		elif tseries[i]['OWN']:
    			tseries[i].update({'COST_BASIS':tseries[i-1]['COST_BASIS']})
    		else:
    			tseries[i].update({'COST_BASIS':0.0})
    		# Logic to update GAIN
    		if tseries[i]['BUY_SELL'] == 'SELL':
    			tseries[i].update({'GAIN':tseries[i]['Adj_Close']-tseries[i-1]['COST_BASIS']})
    		else:
    			tseries[i].update({'GAIN':0.0})
    	# If nothing then just fill with blanks
    	else: 
    		tseries[i].update({'MA':''})
    		tseries[i].update({'OWN':''})
    		tseries[i].update({'BUY_SELL':''})
    		tseries[i].update({'COST_BASIS':0.0})
    		tseries[i].update({'GAIN':0.0})
    		#tseries[i].update({'COMMISSION':''})
    # df = (pandas.DataFrame(tseries))	
    # print df[['Date','Adj_Close','MA','OWN','BUY_SELL','COST_BASIS','GAIN']]
    gains = [tseries[i]['GAIN'] for i in range(len(tseries))]
    gain = numpy.sum(gains)
    if FirstPurchase == 0:
    	returns = 0.0
    else:
    	returns = gain/FirstPurchase
    return returns
    
def sectortest (startdates = ["2003-01-01"], enddates =["2009-01-01"], durations =[100], file ="test2"):
    etfs = ['XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLK','XLU']
    permutations = list()
    # Get a list of dictionaries with all permutations
    for etf in etfs:
    	for i in range(len(startdates)):
    		for dur in durations:
    			gain = backtest(ticker=etf,start=startdates[i],end=enddates[i],duration=dur)
    			permutations.append({'ETF':etf,'GAIN':gain,'START':startdates[i],'END':enddates[i],'DUR':dur})
    # Determine best and worst performing permutations
    bestP = max(permutations, key=lambda x:x['GAIN'])
    worstP = min(permutations, key=lambda x:x['GAIN'])
    # Determine best average duration
    bestGainD = min(d['GAIN'] for d in permutations)
    for dur in durations:
    	permSubSet = filter(lambda x: x['DUR'] == dur, permutations)
    	averageGain = float(sum(d['GAIN'] for d in permSubSet)) / len(permSubSet)
    	if averageGain > bestGainD:
    		bestDur = dur
    		bestGainD = averageGain
    # Determine best time period
    bestGainT = min(d['GAIN'] for d in permutations)
    for j in range(len(startdates)):
    	permSubSet = filter(lambda x: x['START'] == startdates[j], permutations)
    	averageGain = float(sum(d['GAIN'] for d in permSubSet)) / len(permSubSet)
    	if averageGain > bestGainT:
    		startDate = startdates[j]
    		endDate = enddates[j]
    		bestGainT = averageGain	

    with open (file, "w") as f:
        best = 'best {0} {1} {2} {3} {4}\n'.format(bestP['ETF'],bestP['START'],bestP['END'],bestP['DUR'],bestP['GAIN']) 
        worst = 'worst {0} {1} {2} {3} {4}\n'.format(worstP['ETF'],worstP['START'],worstP['END'],worstP['DUR'],worstP['GAIN']) 
        dateStr = 'avg-period {0} {1} {2}\n'.format(startDate,endDate,bestGainT)
        durationStr = 'avg-duration {0} {1}\n'.format(bestDur,bestGainD)
        f.write (best)
        f.write (worst)
        f.write (dateStr)
        f.write (durationStr)

def realbacktest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50, commission = 2, file = "test3"):
    #Create time series as list of dictionaries for specified dates
    obj = Share(ticker)
    tseries = obj.get_historical(start,end)
    tseries = list(reversed(tseries))
    # foo = pandas.read_csv('test_strat.csv')
    # tseries = foo.to_dict('records')
    # # For each day in this series update with calculated parameters
    # # and keep track of the metrics we want (total return)
    isFirstPurchase = False;
    FirstPurchase = 0;
    for i in range(len(tseries)):
    	# Change Adj_Close to a float
    	tseries[i]['Adj_Close'] = float(tseries[i]['Adj_Close'])
    	# Do nothing until we have entered the period where we know a moving average
    	if i >= duration - 1:
    		# Logic to update moving averages
    		duration_tseries = [tseries[i-j]['Adj_Close'] for j in range(duration)]
    		moving_ave = numpy.mean(duration_tseries)
    		tseries[i].update({'MA':moving_ave})
    		# Logic to OWN?
    		if tseries[i]['MA'] < tseries[i]['Adj_Close']:
    			tseries[i]['OWN'] = True
    		else:
    			tseries[i]['OWN'] = False
    		# Logic to update BUY_SELL
    		if tseries[i-1]['OWN'] and not tseries[i]['OWN']:
    			tseries[i].update({'BUY_SELL':'SELL'})
    		elif not tseries[i-1]['OWN'] and tseries[i]['OWN']:
    			tseries[i].update({'BUY_SELL':'BUY'})
    			if not isFirstPurchase:
    				FirstPurchase = tseries[i]['Adj_Close']
    				isFirstPurchase = True
    		else:
    			tseries[i].update({'BUY_SELL':''})
    		# Logic to update COST_BASIS
    		if tseries[i]['BUY_SELL'] == 'BUY':
    			tseries[i].update({'COST_BASIS':tseries[i]['Adj_Close']})
    		elif tseries[i]['OWN']:
    			tseries[i].update({'COST_BASIS':tseries[i-1]['COST_BASIS']})
    		else:
    			tseries[i].update({'COST_BASIS':0.0})
    		# Logic to update GAIN
    		if tseries[i]['BUY_SELL'] == 'SELL':
    			tseries[i].update({'GAIN':tseries[i]['Adj_Close']-tseries[i-1]['COST_BASIS']})
    		else:
    			tseries[i].update({'GAIN':0.0})
    		# Logic to update COMMISSION
    		if tseries[i]['BUY_SELL'] != '':
    			tseries[i].update({'COMMISSION':commission*tseries[i]['Adj_Close']*.0001})
    		else:
    			tseries[i].update({'COMMISSION':0.0})
    	# If nothing then just fill with blanks
    	else: 
    		tseries[i].update({'MA':''})
    		tseries[i].update({'OWN':''})
    		tseries[i].update({'BUY_SELL':''})
    		tseries[i].update({'COST_BASIS':0.0})
    		tseries[i].update({'GAIN':0.0})
    		tseries[i].update({'COMMISSION':0.0})
    # df = (pandas.DataFrame(tseries))	
    # print df[['Date','Adj_Close','MA','OWN','BUY_SELL','COST_BASIS','GAIN']]
    gains = [tseries[i]['GAIN'] for i in range(len(tseries))]
    gain = numpy.sum(gains)
    commissions = [tseries[i]['COMMISSION'] for i in range(len(tseries))]
    totalCommissions = numpy.sum(commissions)
    if FirstPurchase == 0:
    	returns = 0.0
    else:
    	returns = (gain-totalCommissions)/FirstPurchase
    buyHold = (tseries[len(tseries)-1]['Adj_Close'] - tseries[0]['Adj_Close'])/(tseries[0]['Adj_Close'])
    with open (file, "w") as f:
        f.write ('{0} net return, moving average.\n'.format(returns))
        f.write ('{0} buy and hold return.\n'.format(buyHold))

