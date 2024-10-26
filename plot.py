
#%%
# plot the basic options (put & call, long & short) payoffs
# the main goal is to ensure these are correctly calculated and consistent
# is a short put just a -1 * long put? => yes
# next: 
    #TODO: Make the plot interactive
    #Allow fiddling with dte, 
    #Add lines for delta
    #Add bs_price for the options (i.e. black-scholes price, assuming european options, no dividends)

import numpy as np
import grynn_pylib.finance.options as options
import matplotlib.pyplot as plt

strike = 100
spot = np.linspace(strike*0.5, strike*1.5, 100)
premium = 5
dte = 30

plt.figure()
plt.plot(spot, options.intrinsic_value(spot, strike, 'call') - premium, label='long call')
plt.plot(spot, -options.intrinsic_value(spot, strike, 'call') + premium, label='short call')
plt.plot(spot, options.intrinsic_value(spot, strike, 'put') - premium, label='long put')
plt.plot(spot, -options.intrinsic_value(spot, strike, 'put') + premium, label='short put')
plt.xlabel('Spot Price')
plt.ylabel('Payoff')
plt.axhline(0, color='black', linewidth=0.5)
plt.legend()
lines = plt.gca().get_lines()
for i, txt in enumerate(['long call', 'short call', 'long put', 'short put']):
    plt.annotate(txt, (spot[-1], [options.intrinsic_value(spot, strike, 'call')[-1] - premium,
                                  -options.intrinsic_value(spot, strike, 'call')[-1] + premium,
                                  options.intrinsic_value(spot, strike, 'put')[-1] - premium,
                                  -options.intrinsic_value(spot, strike, 'put')[-1] + premium][i]),
                 textcoords="offset points", xytext=(0,10), ha='center', color=lines[i].get_color())
plt.show()

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Long Call
axs[0, 0].plot(spot, options.intrinsic_value(spot, strike, 'call') - premium, label='long call')
axs[0, 0].set_title('Long Call')

# Short Call
axs[0, 1].plot(spot, -options.intrinsic_value(spot, strike, 'call') + premium, label='short call')
axs[0, 1].set_title('Short Call')

# Long Put
axs[1, 0].plot(spot, options.intrinsic_value(spot, strike, 'put') - premium, label='long put')
axs[1, 0].set_title('Long Put')

# Short Put
axs[1, 1].plot(spot, -options.intrinsic_value(spot, strike, 'put') + premium, label='short put')
axs[1, 1].set_title('Short Put')

for ax in axs.flat:
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(strike, color='red', linestyle='--')
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Payoff')


plt.tight_layout()
plt.show()

# Plot a long call and (forward + put) position
fig = plt.figure()
plt.plot(spot, options.intrinsic_value(spot, strike, 'call') - premium, label='long call')
plt.plot(spot, spot - strike + options.intrinsic_value(spot, strike, 'put'), label='forward + put')
plt.xlabel('Spot Price')
plt.ylabel('Payoff')
plt.axhline(0, color='black', linewidth=0.5)
plt.legend()
plt.show()


