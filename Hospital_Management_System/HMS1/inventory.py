class DrugUpdate():
    def __init__(self, balance):
        self.balance = balance
        
    def dispense(self, amount):
        self.balance -= amount
        return self.balance
    
    def stockup(self, amount):
        self.balance += amount
        return self.balance