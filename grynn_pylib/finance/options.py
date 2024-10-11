from scipy.stats import norm
import numpy as np

def bs_d1_d2(spot, strike, time, rate, volatility):
    """Helper function to calculate d1 and d2."""
    sqrt_time = np.sqrt(time)
    d1 = (np.log(spot / strike) + (rate + 0.5 * volatility ** 2) * time) / (volatility * sqrt_time)
    d2 = d1 - volatility * sqrt_time
    return d1, d2

def bs_delta(spot, strike, time, rate, volatility, option_type='call'):
    d1, _ = bs_d1_d2(spot, strike, time, rate, volatility)
    if option_type == 'call':
        return norm.cdf(d1)
    elif option_type == 'put':
        return norm.cdf(d1) - 1
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def bs_gamma(spot, strike, time, rate, volatility):
    """Calculate gamma of an option."""
    d1, _ = bs_d1_d2(spot, strike, time, rate, volatility)
    gamma = norm.pdf(d1) / (spot * volatility * np.sqrt(time))
    return gamma  # Units: 1 / price²

def bs_theta(spot, strike, time, rate, volatility, option_type='call'):
    """Calculate theta of an option.
    
    Returns: 
    float: The theta of the option. Units: price per day
    """
    d1, d2 = bs_d1_d2(spot, strike, time, rate, volatility)
    sqrt_time = np.sqrt(time)
    first_term = - (spot * norm.pdf(d1) * volatility) / (2 * sqrt_time)
    
    if option_type == 'call':
        second_term = - rate * strike * np.exp(-rate * time) * norm.cdf(d2)
    elif option_type == 'put':
        second_term = rate * strike * np.exp(-rate * time) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be either 'call' or 'put'")
    
    theta = first_term + second_term  # Units: price per year
    theta_per_day = theta / 365  # Convert to per-day theta
    return theta_per_day  # Units: price per day

def bs_omega(spot, strike, time, rate, volatility, option_price, option_type='call'):
    """Calculate the omega (elasticity) of an option."""
    delta = bs_delta(spot, strike, time, rate, volatility, option_type)
    omega = delta * (spot / option_price)
    return omega

def bs_omega_short_put(spot, strike, time, rate, volatility, option_price):
    """Calculate the omega (elasticity) for a short put option."""
    omega_put = bs_omega(spot, strike, time, rate, volatility, option_price, option_type='put')
    omega_short_put = -omega_put  # Omega for short put is negative of long put's omega
    return omega_short_put

def payoff_put(spot,strike,premium):
    """
    Calculate the profit as a percentage of the risk from writing a put option.

    Returns:
    float or np.ndarray: The maximum profit as a percentage of the risk.
    """
    # Convert inputs to numpy arrays
    spot = np.asarray(spot)
    strike = np.asarray(strike)
    premium = np.asarray(premium)
    
    # Calculate risk and profit
    risk = strike - premium
    profit = np.minimum(spot - strike, 0) + premium
    
    # Calculate profit as a percentage of the risk
    result = profit / risk
    
    # If the input was a scalar, return a scalar
    if result.size == 1:
        return result.item()
    return result

def payoff_short_put(spot, strike, premium):
    """
    Calculate the intrinsic value of a short put option.

    Returns:
    float or np.ndarray: Intrinsic value of the short put option.
    """
    # Convert inputs to numpy arrays
    spot = np.asarray(spot)
    strike = np.asarray(strike)
    premium = np.asarray(premium)
    
    result = np.minimum(spot - strike, 0) + premium
        
    if result.size == 1:
        return result.item()
    return result

