import numpy as np
"""
I will now define this class LMSR with the given properties, and then import
it to my implementation file. Note that in the given file, transaction costs
are not involved, and wll be handled manually.
"""
class LMSRMarket:
    
    def __init__(self, outcomes, liquidity=1000):
        """
        Initialize the LMSR market.
        :param outcomes: List of outcome names.
        :param liquidity: The b parameter, controlling market sensitivity. This
        b parameter can be changed based on total number of tokens and market
        scenario. Perhaps in the future, machine learning can be used here. 
        """
        self.outcomes = outcomes
        self.liquidity = liquidity
        self.bets = {outcome: 0 for outcome in outcomes}

    def cost_function(self, bets):
        
        """
        This is the cost function based on the LMSR model. 
        Compute the cost function.
        :param bets: Current bets on all outcomes.
        :return: Cost.
        """
        return self.liquidity * np.log(np.sum(np.exp(np.array(bets) / self.liquidity)))

    def prices(self):
        """
        Calculate the current prices for all outcomes.
        :return: A dictionary of outcome prices.
        """
        exp_values = {outcome: np.exp(q / self.liquidity) for outcome, q in self.bets.items()}
        total = sum(exp_values.values())
        return {outcome: exp / total for outcome, exp in exp_values.items()}

    def buy(self, outcome, amount):
        """
        Simulate buying an amount of an outcome.
        :param outcome: The outcome to buy.
        :param amount: The amount to spend.
        :return: The price paid and the new outcome prices.
        """
        prev_cost = self.cost_function(list(self.bets.values()))
        self.bets[outcome] += amount
        new_cost = self.cost_function(list(self.bets.values()))
        price_paid = new_cost - prev_cost
        return price_paid, self.prices()

# Example usage
market = LMSRMarket(outcomes=["Team A", "Team B"], liquidity=10)
print("Initial Prices:", market.prices())

price_paid, new_prices = market.buy("Team A", 5)
print("Price Paid for Team A:", price_paid)
print("New Prices:", new_prices)


import json
# I will create a register to record all the transactions. This register will
# stored after every game in a different location and cleared. 
class LMSRMarket:
    def __init__(self, outcomes, liquidity=10, register_file="bets_register.json"):
        """
        Initialize the LMSR market.
        :param outcomes: List of outcome names.
        :param liquidity: The b parameter, controlling market sensitivity.
        :param register_file: File to store bets register.
        """
        self.outcomes = outcomes
        self.liquidity = liquidity
        self.bets = {outcome: 0 for outcome in outcomes}
        self.register_file = register_file
        self.initialize_register()

    def initialize_register(self):
        """Ensure the register file exists and is properly initialized."""
        try:
            with open(self.register_file, 'r') as f:
                self.register = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.register = []
            self.save_register()

    def save_register(self):
        """Save the current register to file."""
        with open(self.register_file, 'w') as f:
            json.dump(self.register, f, indent=4)

    def cost_function(self, bets):
        """
        Compute the cost function.
        :param bets: Current bets on all outcomes.
        :return: Cost.
        """
        return self.liquidity * np.log(np.sum(np.exp(np.array(bets) / self.liquidity)))

    def prices(self):
        """
        Calculate the current prices for all outcomes.
        :return: A dictionary of outcome prices.
        """
        exp_values = {outcome: np.exp(q / self.liquidity) for outcome, q in self.bets.items()}
        total = sum(exp_values.values())
        return {outcome: exp / total for outcome, exp in exp_values.items()}

    def buy(self, bettor_name, outcome, amount):
        """
        Place a bet on an outcome.
        :param bettor_name: Name of the person placing the bet.
        :param outcome: The outcome being bet on.
        :param amount: The amount being bet.
        :return: The price paid and the new outcome prices.
        """
        if outcome not in self.outcomes or amount <= 0:
            raise ValueError("Invalid outcome or amount.")

        prev_cost = self.cost_function(list(self.bets.values()))
        self.bets[outcome] += amount
        new_cost = self.cost_function(list(self.bets.values()))
        price_paid = new_cost - prev_cost

        # Register the bet
        self.register.append({
            "bettor": bettor_name,
            "outcome": outcome,
            "amount": amount,
            "price_paid": price_paid
        })
        self.save_register()

        return price_paid, self.prices()


