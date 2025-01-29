# I will now import the class and implement it. As already mentioned, 
# transaction costs are handled manually for now. 
from lmsr import LMSRMarket

# Initialize the market
market = LMSRMarket(outcomes=["Team A", "Team B"], liquidity=1000)

while True:
    print("\nCurrent Prices:")
    for outcome, price in market.prices().items():
        print(f"{outcome}: {price:.4f}")

    # Get bettor input
    bettor_name = input("\nEnter bettor's name: ")
    outcome = input("Enter outcome (Team A or Team B): ")
    amount = float(input("Enter amount to bet: "))

    try:
        price_paid, new_prices = market.buy(bettor_name, outcome, amount)
        print(f"\nBet placed successfully!")
        print(f"Price Paid: {price_paid:.2f}")
        print("New Prices:")
        for outcome, price in new_prices.items():
            print(f"{outcome}: {price:.4f}")
    except ValueError as e:
        print(f"Error: {e}")

    # Check if user wants to continue
    cont = input("\nDo you want to add another bet? (y/n): ")
    if cont.lower() != 'y':
        break


