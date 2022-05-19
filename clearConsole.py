import os

# Function to clear the console
clearConsole = lambda: os.system('cls'
                                 if os.name in ('nt', 'dos') else 'clear')
