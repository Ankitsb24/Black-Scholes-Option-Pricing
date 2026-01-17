from src.black_scholes import BlackScholesModel

# Initialize a Call Option
# Spot=100, Strike=105, Time=1yr, Rate=5%, Vol=20%
model = BlackScholesModel(S=100, K=105, T=1, r=0.05, sigma=0.2, option_type='call')

print(f"Option Price: {model.price():.4f}")
print(f"Delta: {model.greeks()['Delta']:.4f}")
