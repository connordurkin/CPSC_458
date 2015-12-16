===========================================
     Markowitz Portfolio Optimization
===========================================
Final Project for CPSC 458 by Connor Durkin
-------------------------------------------
This project explores the use of a mean variance or Markowitz method of portfolio 
optimization. The goal is to employ this trading strategy for a portfolio of SPDR 
ETFs and track returns over historical data. More importantly, though, as this is a 
class in decision making, I have incporated the ability for the functions here to 
explain their motivations to a human being--hopefully in a palatable manner. Below 
are the function definitions and at the end of the notebook you will find an example 
of their use. These functions were written with default key values but the operations 
are general enough to apply this strategy to any selection of securities with return 
data available via yahoo finance. 

--------------------------------------------
getTimeSeries( ticker, start_date, end_date) 
--------------------------------------------
 What it does:

getTimeSeries() takes in a date range and a ticker and returns a timeseries of 
adjusted closing prices.

 Inputs:
* ticker: a string indiciating the security for which the time series will be 
generated.
* start_date: a string of the form 'YYYY-MM-DD' declaring the beginning of the 
historical window.
* end_date: a string of the form 'YYYY-MM-DD' declaring the end of the historical 
window

 Returns:
* time_series: a single column Pandas DataFrame containing the time series of 
adjusted close prices for the indicated ticker.

-------------------------------------------------
getMultTimeSeries( tickers, start_date, end_date) 
-------------------------------------------------
 What it does:
getMultTimeSeries() takes in a list of tickers and a specified date range and 
returns a Pandas DataFrame containing timeseries of adjusted closing prices. 
 Inputs:
* tickers: a list of strings indicating which tickers to include. Defaults to these 
9 SPDR ETFs: 'XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLK','XLU'.
* start_date: a string of the form 'YYYY-MM-DD' declaring the beginning of the 
historical window.
* end_date: a string of the form 'YYYY-MM-DD' declaring the end of the historical 
window

 Returns:
* time_series_dataframe: a dataframe of adjusted closing price timeseries over the 
specified date range for the specified group of tickers

-------------------------
markowitzReturns( returns)
-------------------------
 What it does:
markowitzReturns() takes in a Pandas DataFrame (or any container which can be 
converted to a numpy matrix) of returns and uses mean-variance portfolio theory to 
return an optimally weighted portfolio. It does so by minimizing 
$\omega^{T}\Sigma\omega -qR^{T}\omega$ (the Markowitz mean - variance framework) for 
portfolio weights $\omega$. Where $\Sigma$ is the covariance matrix of the 
securities, $R$ is the expected return matrix and $q$ is the mean return vector of 
all securities. The optimization is performed using the CVXOPT package employing the 
use of the solvers.qp() quadratic programming method. This method minimizes $(1/2)
x^{T}Px + q^{T}x$ subject to $Gx \preceq h$ and $Ax = b$. It also utilizes CVXOPT's 
BLAS methods for performing linear algebra computations. Inspiration for this 
process was found in Dr. Thomas Starke, David Edwards and Dr. Thomas Wiecki's 
quantopian blog post located at: http://blog.quantopian.com/markowitz-portfolio-
optimization-2/.

 Inputs:
* returns: a Pandas DataFrame(or other container which can be converted to a numpy 
matrix). NOTE: the dataframe produced by getMultTimeSeries must be transposed (
returns.T) for meaningful results. 
* justify: a True / False input determining whether to print a robust explanation of 
the choice for the portfolio shift. 


 Returns:
* optimal_weights: the weights of the optimal portfolio in array form.
* returns: the returns of all portfolios calculated across the effecient frontier.
* risks: list of risks of all portfolios calculated across the efficient frontier.

----------------------------------------------------------------------
backtest( tickers, start_date, end_date, start, max_lookback, explain)
----------------------------------------------------------------------
 What it does:
backtest() applies the mean-variance portfolio optimization trading strategy to a 
list of stocks. It applies the markowitzReturns() method over a range of dates and 
tracks the portfolio movement and returns, outputting a DataFrame describing the 
portfolio over time, a DataFrame describing the returns over time and a total return 
amount. **Backtest does not take into account commission costs.** Running backtest(
explain = True) produces the output below. The default dates were carefully selected 
so that just one explain instance would print. 

 Inputs:
* tickers: a list of strings indicating which tickers to include. Defaults to these 
9 SPDR ETFs: 'XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLK','XLU'.
* start_date: a string of the form 'YYYY-MM-DD' declaring the beginning of the 
historical window.
* end_date: a string of the form 'YYYY-MM-DD' declaring the end of the historical 
window
* start: the minimum number of days to wait before beginning to trade (i.e. how much 
information is needed). Default is 10.
* max_lookback: the maximum number of days to look back for data, i.e. the size of 
the input to markowitzReturns(). Default is 100.

 Returns:
* weights_df: a pandas DataFrame containing the portfolio weights over time 
beginning with the start date + start*days.
* total_returns: a pandas DataFrame containing the portfolio returns over time 
beginning with the start date + start*days.
* naive_return: the total naive return (numpy float).

--------------------------------------------------------------------
analyzeResults( weights_df, total_returns, naive_return, commission)
--------------------------------------------------------------------
 What it does:
analyzeResults() is the final function which analyzes and displays the results of 
the backtest() function. It takes the output of backtest() plus an argument for the 
commission wich defaults to 4 basis points. It plots the real and naive returns over 
time and displays the total real and naive returns over the date range from backtest().
Below is an example from 2012-2013.

 Inputs:
* weights_df: pandas DataFrame of portfolio weights over time, returned from backtest().
* total_returns: pandas DataFrame of naive returns over time, returned from backtest().
* naive_return: total naive_return as returned by backtest().
* commission: basis point cost on trades, defualts to 4 basis points. 

 Returns:
* nothing



