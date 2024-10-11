#%%
import grynn_pylib.finance.options as options
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact

spot = 100
strike = 100.0
hist_vol = 0.5 #50%

# Initialize the plot lines
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Payoff Short Put')
line2, = ax.plot([], [], label='Position Delta')

def update_plot(hist_vol, dte):
	spot_ladder = np.linspace(50, 150, 100)
	strike = 100
	payoff_short_put = options.payoff_short_put(spot_ladder, strike, 0)
	position_delta = -options.bs_delta(np.asarray(spot_ladder), strike, dte/365, 0.05, 0.2, option_type='put')
	line1.set_ydata(payoff_short_put)
	line2.set_ydata(position_delta)
	ax.relim()
	ax.autoscale_view()
	plt.draw()

def update_plot(hist_vol, dte):
    spot_ladder = np.arange(spot*(1-hist_vol), spot*(1+hist_vol), num=50)
    payoff_short_put = options.payoff_short_put(spot_ladder, strike, 0)
    position_delta = -options.bs_delta(np.asarray(spot_ladder), strike, dte/365, 0.05, 0.2, option_type='put')
    line1.set_ydata(payoff_short_put)
    line2.set_ydata(position_delta)
    

# prepare_plot(spot, strike, hist_vol)
interact(update_plot, hist_vol=(0.1, 1.0, 0.1), dte=(1, 365, 1))


#%%

# def prepare_plot(spot, strike, hist_vol):
#     spot_ladder = range(int(spot*(1-hist_vol)), int(spot*(1+hist_vol)), 1)
#     payoff_short_put = options.payoff_short_put(spot_ladder, strike, 0)
#     position_delta = -options.bs_delta(np.asarray(spot_ladder), strike, 0, 0.05, 0.2, option_type='put')
    
#     plt.figure()
#     line1, = plt.plot(spot_ladder, payoff_short_put)
#     plt.xlabel('Spot Price')
#     plt.ylabel('Payoff')
#     plt.title('Short Put Payoff')
#     plt.axvline(x=strike, color='red', linestyle='--')
    
#     ax1 = plt.gca()
#     ax2 = ax1.twinx()
    
#     line2, = ax2.plot(spot_ladder, position_delta, label='Position Delta', color='blue')
#     ax2.set_ylabel('Delta')
