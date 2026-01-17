import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesModel:    
    def __init__(self, S, K, T, r, sigma, option_type='call'):
        self.S = S          # Underlying Asset Price
        self.K = K          # Strike Price
        self.T = T          # Time to Maturity (Years)
        self.r = r          # Risk-free Rate (decimal)
        self.sigma = sigma  # Volatility (decimal)
        self.option_type = option_type.lower()
        
    def _calculate_d1_d2(self, S=None):
        S = self.S if S is None else S
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    def price(self, S=None):
        S = self.S if S is None else S
        d1, d2 = self._calculate_d1_d2(S)
        
        if self.option_type == 'call':
            return S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    def greeks(self, S=None):
        S = self.S if S is None else S
        d1, d2 = self._calculate_d1_d2(S)
        
        # Calculation of Common Components
        pdf_d1 = norm.pdf(d1)
        cdf_d1 = norm.cdf(d1)
        cdf_d2 = norm.cdf(d2)
        
        # Delta
        delta = cdf_d1 if self.option_type == 'call' else cdf_d1 - 1
        
        # Gamma (Same for Call/Put)
        gamma = pdf_d1 / (S * self.sigma * np.sqrt(self.T))
        
        # Vega (Same for Call/Put)
        vega = S * pdf_d1 * np.sqrt(self.T)
        
        # Theta
        theta_call = - (S * pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * cdf_d2
        theta_put = - (S * pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        theta = theta_call if self.option_type == 'call' else theta_put
        
        # Rho
        rho = self.K * self.T * np.exp(-self.r * self.T) * (cdf_d2 if self.option_type == 'call' else -norm.cdf(-d2))
        
        return {"Delta": delta, "Gamma": gamma, "Vega": vega, "Theta": theta, "Rho": rho}

def plot_analysis(model, price_range):
    prices = [model.price(S) for S in price_range]
    greeks_data = [model.greeks(S) for S in price_range]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(f"Black-Scholes Analysis: {model.option_type.capitalize()} Option", fontsize=16)
    
    # Price Plot
    axes[0, 0].plot(price_range, prices, color='blue')
    axes[0, 0].set_title("Option Price vs Underlying")
    axes[0, 0].grid(True)
    
    # Delta Plot
    axes[0, 1].plot(price_range, [g['Delta'] for g in greeks_data], color='green')
    axes[0, 1].set_title("Delta (Sensitivity to Price)")
    
    # Gamma Plot
    axes[0, 2].plot(price_range, [g['Gamma'] for g in greeks_data], color='red')
    axes[0, 2].set_title("Gamma (Stability of Delta)")
    
    # Vega Plot
    axes[1, 0].plot(price_range, [g['Vega'] for g in greeks_data], color='purple')
    axes[1, 0].set_title("Vega (Sensitivity to Volatility)")
    
    # Theta Plot
    axes[1, 1].plot(price_range, [g['Theta'] for g in greeks_data], color='orange')
    axes[1, 1].set_title("Theta (Time Decay)")
    
    # Rho Plot
    axes[1, 2].plot(price_range, [g['Rho'] for g in greeks_data], color='brown')
    axes[1, 2].set_title("Rho (Interest Rate Sensitivity)")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
