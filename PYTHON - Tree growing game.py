import time

class Tree:
    def __init__(self):
        self.height = 1  # Initial height of the tree
        self.branches = 0  # Initial number of branches
    
    def grow(self):
        self.height += 1
        self.branches += 1
    
    def display(self):
        # Display the trunk
        for i in range(self.height):
            print(" " * (10 - i) + "|" + " " * i + "|")
        
        # Display branches
        for _ in range(self.branches):
            print(" " * (10 - self.branches) + "/" + " " * self.branches + "\\")
        
        print(" " * 9 + "~~~")  # Represent the ground
    
    def needs_care(self):
        print("\nYour tree needs water and sunlight!")
        action = input("Type 'water' or 'sunlight' to care for your tree: ").strip().lower()
        if action in ['water', 'sunlight']:
            print("You provided the tree with " + action + "! 🌿")
            self.grow()
        else:
            print("Invalid input. The tree is still growing slowly...")

def play_game():
    print("Welcome to the Tree Growing Game! 🌳")
    tree = Tree()
    
    for day in range(1, 11):  # Let the game run for 10 cycles
        print(f"\nDay {day}:")
        tree.display()
        tree.needs_care()
        time.sleep(1)  # Simulate the passing of time

    print("\nYour tree has grown beautifully! 🌲")

# Run the game
play_game()
