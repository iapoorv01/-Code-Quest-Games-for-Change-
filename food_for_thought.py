import tkinter as tk
from tkinter import messagebox


class FoodForThoughtGame:
    def __init__(self, screen):
        self.screen = screen
        self.root = tk.Tk()
        self.root.title("Food for Thought")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa")

        # Game constants
        self.INITIAL_RESOURCES = 800
        self.INITIAL_POPULATION = 50
        self.INITIAL_ENVIRONMENT = 50
        self.CROP_YIELD = 10
        self.LIVESTOCK_YIELD = 5
        self.SUSTAINABLE_PRACTICES_COST = 50
        self.SUSTAINABLE_PRACTICES_BONUS = 10
        self.MAX_POPULATION = 500

        # Game state
        self.resources = self.INITIAL_RESOURCES
        self.population = self.INITIAL_POPULATION
        self.environment = self.INITIAL_ENVIRONMENT
        self.crops_planted = 0
        self.livestock_raised = 0
        self.sustainable_practices_invested = 0

        # GUI components
        self.create_widgets()
        self.display_instructions()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Food for Thought", font=("Arial", 28), bg="#4db6e1", fg="white")
        title_label.pack(pady=20)

        resource_frame = tk.Frame(self.root, bg="#b2ebf2")
        resource_frame.pack(pady=10, padx=20, fill='x')

        self.resource_label = tk.Label(resource_frame, text=f"Resources: {self.resources}", font=("Arial", 16),
                                       bg="#b2ebf2")
        self.resource_label.pack(side='left', padx=10)

        self.population_label = tk.Label(resource_frame, text=f"Population: {self.population}", font=("Arial", 16),
                                         bg="#b2ebf2")
        self.population_label.pack(side='left', padx=10)

        self.environment_label = tk.Label(resource_frame, text=f"Environment: {self.environment}", font=("Arial", 16),
                                          bg="#b2ebf2")
        self.environment_label.pack(side='left', padx=10)

        action_frame = tk.Frame(self.root, bg="#b2ebf2")
        action_frame.pack(pady=10, padx=20, fill='x')

        self.crops_label = tk.Label(action_frame, text=f"Crops planted: {self.crops_planted}", font=("Arial", 16),
                                    bg="#b2ebf2")
        self.crops_label.pack(side='left', padx=10)

        self.livestock_label = tk.Label(action_frame, text=f"Livestock raised: {self.livestock_raised}",
                                        font=("Arial", 16), bg="#b2ebf2")
        self.livestock_label.pack(side='left', padx=10)

        self.sustainable_practices_label = tk.Label(action_frame,
                                                    text=f"Sustainable practices: {self.sustainable_practices_invested}",
                                                    font=("Arial", 16), bg="#b2ebf2")
        self.sustainable_practices_label.pack(side='left', padx=10)

        self.action_label = tk.Label(self.root, text="What would you like to do?", font=("Arial", 16), bg="#e0f7fa")
        self.action_label.pack(pady=15)

        self.action_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.action_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.process_action, font=("Arial", 16),
                                       bg="#4db6e1", fg="white")
        self.submit_button.pack(pady=10)

        self.event_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#e0f7fa", wraplength=600)
        self.event_label.pack(pady=15)

        self.instructions_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left", bg="#e0f7fa")
        self.instructions_label.pack(pady=10)

    def display_instructions(self):
        instructions = (
            "Instructions:\n"
            "1. Plant crops: Use 'plant crops' (cost: 100 resources)\n"
            "2. Raise livestock: Use 'raise livestock' (cost: 150 resources)\n"
            "3. Invest in sustainable practices: Use 'invest in sustainable practices' (cost: 50 resources)\n"
            "4. Each action has an impact on resources, population, and environment.\n"
            "5. Aim for a sustainable balance to win!"
        )
        self.instructions_label.config(text=instructions)

    def process_action(self):
        action = self.action_entry.get().strip().lower()
        event_message = ""

        if "plant crops" in action:
            if self.resources >= 100:
                self.resources -= 100
                self.crops_planted += 1

                # Dynamic impact based on environment
                if self.environment > 70:
                    self.population += 10
                    self.environment -= 1
                    event_message = "You planted crops! Resources -100. Population +10. Environment -1."
                elif self.environment > 50:
                    self.population += 10
                    self.environment -= 1
                    event_message = "You planted crops! Resources -100. Population +5. Environment -2."
                else:
                    self.population += 3
                    self.environment -= 3
                    event_message = "You planted crops! Resources -100. Population +3. Environment -3."

            else:
                event_message = "Not enough resources!"

        elif "raise livestock" in action:
            if self.resources >= 150:
                self.resources -= 150
                self.livestock_raised += 1

                # Dynamic impact based on environment
                if self.environment > 70:
                    self.population += 5
                    self.environment -= 2
                    event_message = "You raised livestock! Resources -150. Population +5. Environment -2."
                elif self.environment > 50:
                    self.population += 5
                    self.environment -= 2
                    event_message = "You raised livestock! Resources -150. Population +3. Environment -4."
                else:
                    self.population += 1
                    self.environment -= 6
                    event_message = "You raised livestock! Resources -150. Population +1. Environment -6."

            else:
                event_message = "Not enough resources!"

        elif "invest in sustainable practices" in action:
            if self.resources >= self.SUSTAINABLE_PRACTICES_COST:
                self.resources -= self.SUSTAINABLE_PRACTICES_COST
                self.sustainable_practices_invested += 1
                self.environment += self.SUSTAINABLE_PRACTICES_BONUS
                event_message = "You invested in sustainable practices! Resources -50, Environment +10."
            else:
                event_message = "Not enough resources!"

        self.update_labels()
        self.event_label.config(text=event_message)
        self.check_game_over()

    def update_labels(self):
        self.resource_label.config(text=f"Resources: {self.resources}")
        self.population_label.config(text=f"Population: {self.population}")
        self.environment_label.config(text=f"Environment: {self.environment}")
        self.crops_label.config(text=f"Crops planted: {self.crops_planted}")
        self.livestock_label.config(text=f"Livestock raised: {self.livestock_raised}")
        self.sustainable_practices_label.config(text=f"Sustainable practices: {self.sustainable_practices_invested}")

    def check_game_over(self):
        if self.population >= self.MAX_POPULATION and self.environment > 50:
            messagebox.showinfo("Congratulations", "You won! You managed the farm sustainably.")
            self.root.quit()
        elif self.resources <= 0:
            messagebox.showinfo("Game Over", "Game over! You have run out of resources.")
            self.root.quit()
        elif self.population >= self.MAX_POPULATION:
            messagebox.showinfo("Game Over", f"Game over! Population exceeded sustainable limits: {self.population}.")
            self.root.quit()
        elif self.environment <= 0:
            messagebox.showinfo("Game Over", f"Game over! Environment depleted. Environment: {self.environment}.")
            self.root.quit()

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = FoodForThoughtGame(screen=tk.Tk())
    game.run()
