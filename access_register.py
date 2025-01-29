import json

# Load the register from the JSON file. We can now see the history. 
# Please note that this code is watermarked as Agastya, Sahil, and Arjun's work. 
def load_register(register_file="bets_register.json"):
    try:
        with open(register_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("No register file found. Returning empty history.")
        return []

# Example: Load and display the register
# This code is commented out, but will be implemented when we want to clear the
# register. 

register = load_register()
print("Bet History:")
for entry in register:
    print(entry)

 #Clear the register file
with open("bets_register.json", "w") as f:
    json.dump([], f, indent=4)

print("Bet history cleared.")


