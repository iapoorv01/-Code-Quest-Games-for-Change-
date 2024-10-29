import customtkinter as ctk
import random
from PIL import Image, ImageTk

class EcoAdventureGame:
    def __init__(self, parent):
        self.app = ctk.CTkToplevel(parent)
        self.app.title("Eco Adventure Game")
        self.app.attributes('-fullscreen', True)
        self.app.configure(bg="0000FF")

        self.score = 0
        self.current_scenario_index = 0
        self.scenarios = []
        self.selected_scenarios = []
        self.image_label = None  # To hold the image label

        # Define your custom font using CTkFont
        # Example: Check if changing to a common font works
        self.custom_font = ctk.CTkFont(family="Bahnschrift SemiBold Condensed", size=40)
        # Update with your font name

        self.display_intro()

        # Bind the Escape key to the exit_game method
        self.app.bind("<Escape>", self.exit_game)

    def exit_game(self, event=None):
        self.app.destroy()

    def display_intro(self):
        intro_frame = ctk.CTkFrame(self.app)
        intro_frame.pack(pady=20)

        intro_label = ctk.CTkLabel(intro_frame, text="Welcome to Eco Adventure!\n"
                                                     "Make wise decisions to help the environment.\n"
                                                     "Click 'Start' to begin.",
                                     font=self.custom_font, justify="center", text_color="#A9A9A9")
        intro_label.pack(pady=20)

        start_button = ctk.CTkButton(intro_frame, text="Start", command=self.start_game, font=self.custom_font)
        start_button.pack(pady=10)

    def start_game(self):
        self.score = 0
        self.current_scenario_index = 0

        for widget in self.app.winfo_children():
            widget.pack_forget()

        self.scenarios = self.load_scenarios()
        random.shuffle(self.scenarios)
        self.selected_scenarios = self.scenarios[:7]

        self.display_scenario()

    def load_scenarios(self):

        return [
            self.scenario_one, self.scenario_two, self.scenario_three,
            self.scenario_four, self.scenario_five, self.scenario_six,
            self.scenario_seven, self.scenario_eight, self.scenario_nine,
            self.scenario_ten, self.scenario_eleven, self.scenario_twelve,
            self.scenario_thirteen, self.scenario_fourteen, self.scenario_fifteen,
            self.scenario_sixteen, self.scenario_seventeen, self.scenario_eighteen,
            self.scenario_nineteen, self.scenario_twenty, self.scenario_twenty_one,
            self.scenario_twenty_two, self.scenario_twenty_three, self.scenario_twenty_four,
            self.scenario_twenty_five, self.scenario_twenty_six, self.scenario_twenty_seven,
            self.scenario_twenty_eight, self.scenario_twenty_nine, self.scenario_thirty,
            self.scenario_thirty_one, self.scenario_thirty_two, self.scenario_thirty_three,
            self.scenario_thirty_four, self.scenario_thirty_five, self.scenario_thirty_six,
            self.scenario_thirty_seven, self.scenario_thirty_eight, self.scenario_thirty_nine,
            self.scenario_forty, self.scenario_forty_one, self.scenario_forty_two,
            self.scenario_forty_three, self.scenario_forty_four, self.scenario_forty_five,
            self.scenario_forty_six, self.scenario_forty_seven, self.scenario_forty_eight,
            self.scenario_forty_nine, self.scenario_fifty, self.scenario_fifty_one,
            self.scenario_fifty_two, self.scenario_fifty_three, self.scenario_fifty_four,
            self.scenario_fifty_five, self.scenario_fifty_six, self.scenario_fifty_seven,
            self.scenario_fifty_eight, self.scenario_fifty_nine, self.scenario_sixty,
            self.scenario_sixty_one, self.scenario_sixty_two, self.scenario_sixty_three,
            self.scenario_sixty_four, self.scenario_sixty_five, self.scenario_sixty_six,
            self.scenario_sixty_seven, self.scenario_sixty_eight, self.scenario_sixty_nine,
            self.scenario_seventy, self.scenario_seventy_one, self.scenario_seventy_two,
            self.scenario_seventy_three, self.scenario_seventy_four, self.scenario_seventy_five,
            self.scenario_seventy_six, self.scenario_seventy_seven, self.scenario_seventy_eight,
            self.scenario_seventy_nine, self.scenario_eighty, self.scenario_eighty_one,
            self.scenario_eighty_two, self.scenario_eighty_three, self.scenario_eighty_four,
            self.scenario_eighty_five, self.scenario_eighty_six, self.scenario_eighty_seven,
            self.scenario_eighty_eight, self.scenario_eighty_nine, self.scenario_ninety,
            self.scenario_ninety_one, self.scenario_ninety_two, self.scenario_ninety_three,
            self.scenario_ninety_four, self.scenario_ninety_five, self.scenario_ninety_six,
            self.scenario_ninety_seven, self.scenario_ninety_eight, self.scenario_ninety_nine,
            self.scenario_one_hundred
        ]


    def display_scenario(self):
        for widget in self.app.winfo_children():
            widget.pack_forget()

        if self.image_label:
            self.image_label.destroy()  # Remove previous image if exists

        if self.current_scenario_index < len(self.selected_scenarios):
            scenario = self.selected_scenarios[self.current_scenario_index]
            scenario_text, choices, image_path = scenario()
            scenario_label1 = ctk.CTkLabel(
                self.app,
                text=f"Scenario: {self.current_scenario_index + 1}",
                font=self.custom_font,
                justify="left",
                text_color="#C0C0C0"
            )

            scenario_label1.pack(pady=20,padx=20)
            scenario_label = ctk.CTkLabel(self.app, text=scenario_text, font=self.custom_font, justify="left",
                                           text_color="#C0C0C0")
            scenario_label.pack(pady=20)

            # Load and display the image
            try:
                image = Image.open(image_path)
                image = image.resize((400, 300), Image.LANCZOS)
                self.image_label = ctk.CTkLabel(self.app, text="", image=ImageTk.PhotoImage(image))
                self.image_label.image = ImageTk.PhotoImage(image)  # Keep a reference
                self.image_label.pack(pady=10)
            except FileNotFoundError:
                error_label = ctk.CTkLabel(self.app, text="Image not found!", font=self.custom_font, text_color="red")
                error_label.pack(pady=10)

            choice_frame = ctk.CTkFrame(self.app)
            choice_frame.pack(pady=10)

            for i, choice in enumerate(choices):
                button = ctk.CTkButton(
                    choice_frame,
                    text=choice[0],
                    command=lambda i=i: self.process_choice(i),
                    font=self.custom_font
                )
                button.pack(pady=10, padx=10, fill='both')
        else:
            self.display_result()

    def process_choice(self, choice_index):
        points = self.selected_scenarios[self.current_scenario_index]()[1][choice_index][1]
        self.score += points
        self.current_scenario_index += 1
        self.display_scenario()

    def display_result(self):
        for widget in self.app.winfo_children():
            widget.pack_forget()

        result_text = f"Your total environmental impact score is: {self.score}\n\n"
        if self.score > 20:
            result_text += "Congratulations! You made great choices to help the environment!"
        elif self.score > 10:
            result_text += "Good job! Your choices were mostly positive, but there is still room for improvement."
        else:
            result_text += "You could have made better choices. Keep learning about how you can help the environment!"

        result_label = ctk.CTkLabel(self.app, text=result_text, font=self.custom_font, justify="center", text_color="#3c763d")
        result_label.pack(pady=20)

        restart_button = ctk.CTkButton(self.app, text="Play Again", command=self.start_game, font=self.custom_font)
        restart_button.pack(pady=10)

    # Define scenarios with image paths
    def scenario_one(self):
        scenario_text = "You come across a river full of plastic waste.\nWhat do you choose to do?"
        choices = [("Clean up the waste with your friends.", 10),
                   ("Ignore the waste and continue on your way.", -5),
                   ("Report it to the local authorities.", 5)]
        return scenario_text, choices, "scenariosimages/sc1.png"  # Path to image

    def scenario_two(self):
        scenario_text = "You are at a grocery store and have to choose between a plastic bag, a paper bag, or a reusable cloth bag.\nWhat do you choose?"
        choices = [("Plastic bag.", -5),
                   ("Paper bag.", 5),
                   ("Reusable cloth bag.", 10)]
        return scenario_text, choices, "scenariosimages/sc2.png"  # Path to image

    def scenario_three(self):
        scenario_text = "Your city is facing a severe drought. You have to choose how to conserve water.\nWhat do you choose?"
        choices = [("Take shorter showers and turn off the tap while brushing your teeth.", 10),
                   ("Use a garden hose to wash your car every week.", -5),
                   ("Collect rainwater for gardening and reduce water usage at home.", 15)]
        return scenario_text, choices, "scenariosimages/sc3.png"  # Path to image

    def scenario_four(self):
        scenario_text = "Your school is planning a paperless campaign.\nWhat do you suggest to help reduce paper waste?"
        choices = [("Encourage everyone to use digital notebooks.", 10),
                   ("Use both sides of the paper before recycling.", 5),
                   ("Ignore the campaign and keep using paper.", -5)]
        return scenario_text, choices, "scenariosimages/sc4.jpg"

    def scenario_five(self):
        scenario_text = "Your neighbor burns leaves in his backyard, causing smoke.\nWhat do you do?"
        choices = [("Ask him to compost the leaves instead.", 10),
                   ("Call the local authorities to report it.", 5),
                   ("Ignore it, it's not your problem.", -5)]
        return scenario_text, choices, "scenariosimages/sc5.jpeg"

    def scenario_six(self):
        scenario_text = "A factory near your town is releasing pollutants into the river.\nWhat is your course of action?"
        choices = [("Organize a protest and create awareness.", 15),
                   ("Ignore the issue, it's not affecting you directly.", -10),
                   ("Report the factory to the environmental authorities.", 10)]
        return scenario_text, choices, "scenariosimages/sc6.jpg"

    def scenario_seven(self):
        scenario_text = "You have a choice between buying local produce or imported fruits.\nWhich do you choose?"
        choices = [("Buy local produce.", 10),
                   ("Buy imported fruits.", -5),
                   ("Buy both and mix them up.", 0)]
        return scenario_text, choices, "scenariosimages/sc7.jpeg"

    def scenario_eight(self):
        scenario_text = "Your community is considering building a new park.\nWhat do you propose?"
        choices = [("Include a community garden and recycling bins.", 15),
                   ("Leave it as an empty field for people to use freely.", 5),
                   ("Pave most of it for parking space.", -5)]
        return scenario_text, choices, "scenariosimages/sc8.png"

    def scenario_nine(self):
        scenario_text = "You find a stray animal in need of help.\nWhat do you do?"
        choices = [("Adopt the animal or find it a home.", 10),
                   ("Take it to a shelter.", 5),
                   ("Ignore it.", -5)]
        return scenario_text, choices, "scenariosimages/sc9.jpg"

    def scenario_ten(self):
        scenario_text = "Your city plans to cut down trees for a new road.\nWhat is your response?"
        choices = [("Protest the tree-cutting and suggest alternative routes.", 15),
                   ("Support the development for better traffic flow.", -5),
                   ("Plant new trees to replace the cut ones.", 10)]
        return scenario_text, choices, "scenariosimages/sc10.jpg"

    def scenario_eleven(self):
        scenario_text = "You notice excessive energy use in your office building.\nWhat action will you take?"
        choices = [("Propose an energy-saving plan.", 10),
                   ("Ignore it, it’s not your responsibility.", -5),
                   ("Only switch off lights in your area.", 5)]
        return scenario_text, choices, "scenariosimages/sc11.jpeg"

    def scenario_twelve(self):
        scenario_text = "There’s an option to carpool to work instead of driving alone.\nWhat do you do?"
        choices = [("Carpool with colleagues.", 10),
                   ("Keep driving alone.", -5),
                   ("Use public transport instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc12.jpg"

    def scenario_thirteen(self):
        scenario_text = "You find a leaking faucet in a public restroom.\nHow do you handle it?"
        choices = [("Report it immediately.", 5),
                   ("Ignore it, someone else will report it.", -5),
                   ("Fix it yourself if possible.", 10)]
        return scenario_text, choices, "scenariosimages/sc13.jpeg"

    def scenario_fourteen(self):
        scenario_text = "You are responsible for organizing a community event.\nHow will you make it eco-friendly?"
        choices = [("Use reusable decorations and materials.", 10),
                   ("Use disposable items for convenience.", -5),
                   ("Limit waste and promote recycling.", 7)]
        return scenario_text, choices, "scenariosimages/sc14.jpeg"

    def scenario_fifteen(self):
        scenario_text = "You see a friend throwing trash on the ground.\nWhat do you do?"
        choices = [("Ask them to pick it up and throw it in the bin.", 10),
                   ("Ignore it, it's not your problem.", -5),
                   ("Pick it up yourself and show by example.", 7)]
        return scenario_text, choices, "scenariosimages/sc15.jpeg"

    def scenario_sixteen(self):
        scenario_text = "Your apartment complex doesn't have a recycling program.\nWhat do you do?"
        choices = [("Start a recycling initiative in your building.", 15),
                   ("Continue throwing all waste together.", -5),
                   ("Talk to the management about setting up a program.", 10)]
        return scenario_text, choices, "scenariosimages/sc16.jpeg"

    def scenario_seventeen(self):
        scenario_text = "Your friend frequently uses disposable plastic bottles.\nWhat do you suggest?"
        choices = [("Gift them a reusable bottle.", 10),
                   ("Do nothing, it's their choice.", -5),
                   ("Encourage them to recycle the bottles.", 5)]
        return scenario_text, choices, "scenariosimages/sc17.jpeg"

    def scenario_eighteen(self):
        scenario_text = "Your company uses excessive paper for printing.\nHow do you address this?"
        choices = [("Suggest moving to digital documents.", 10),
                   ("Keep using paper as usual.", -5),
                   ("Encourage reusing single-sided printed paper.", 7)]
        return scenario_text, choices, "scenariosimages/sc18.jpeg"

    def scenario_nineteen(self):
        scenario_text = "You notice an endangered species in your area.\nWhat do you do?"
        choices = [("Report it to the local wildlife authority.", 10),
                   ("Try to protect the habitat on your own.", 5),
                   ("Ignore it, it’s not your concern.", -5)]
        return scenario_text, choices, "scenariosimages/sc19.jpeg"

    def scenario_twenty(self):
        scenario_text = "Your city starts a recycling competition.\nHow do you participate?"
        choices = [("Encourage your community to join and recycle.", 15),
                   ("Recycle only your own waste.", 5),
                   ("Ignore the competition.", -5)]
        return scenario_text, choices, "scenariosimages/sc20.jpeg"

    def scenario_twenty_one(self):
        scenario_text = "You find out about an illegal dumping site near your home.\nWhat action do you take?"
        choices = [("Report it to the authorities.", 10),
                   ("Organize a community cleanup.", 15),
                   ("Ignore it.", -5)]
        return scenario_text, choices, "scenariosimages/sc21.png"

    def scenario_twenty_two(self):
        scenario_text = "Your neighborhood lacks green spaces.\nWhat do you suggest?"
        choices = [("Propose creating a community garden.", 10),
                   ("Encourage people to plant trees.", 7),
                   ("Do nothing about it.", -5)]
        return scenario_text, choices, "scenariosimages/sc22.jpg"

    def scenario_twenty_three(self):
        scenario_text = "You are aware of an endangered species in your area.\nWhat do you do?"
        choices = [("Report it to wildlife conservation groups.", 10),
                   ("Take pictures and leave them alone.", 5),
                   ("Ignore it.", -5)]
        return scenario_text, choices, "scenariosimages/sc23.jpg"

    def scenario_twenty_four(self):
        scenario_text = "Your local beach is polluted with plastic waste.\nWhat action do you take?"
        choices = [("Join a beach cleanup.", 10),
                   ("Ignore it, it's not your problem.", -5),
                   ("Organize a community awareness campaign.", 15)]
        return scenario_text, choices, "scenariosimages/sc24.jpeg"

    def scenario_twenty_five(self):
        scenario_text = "Your friend is planning a bonfire with treated wood.\nWhat do you suggest?"
        choices = [("Advise against it due to toxic fumes.", 10),
                   ("Join the bonfire regardless.", -5),
                   ("Suggest using natural wood instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc25.jpeg"

    def scenario_twenty_six(self):
        scenario_text = "The local school is planning to replace its playground with plastic turf.\nWhat is your opinion?"
        choices = [("Advocate for natural grass and plants.", 10),
                   ("Support the plastic turf for low maintenance.", -5),
                   ("Suggest a mix of both natural and synthetic elements.", 5)]
        return scenario_text, choices, "scenariosimages/sc26.jpeg"

    def scenario_twenty_seven(self):
        scenario_text = "Your local park is cutting down trees for a new parking lot.\nWhat do you do?"
        choices = [("Protest and suggest an alternative solution.", 10),
                   ("Accept it for better convenience.", -5),
                   ("Organize a tree planting campaign.", 7)]
        return scenario_text, choices, "scenariosimages/sc27.jpg"

    def scenario_twenty_eight(self):
        scenario_text = "Your school cafeteria uses disposable plastic cups.\nHow do you suggest reducing plastic waste?"
        choices = [("Introduce reusable cups for everyone.", 10),
                   ("Encourage bringing personal cups.", 5),
                   ("Do nothing, it's not a big deal.", -5)]
        return scenario_text, choices, "scenariosimages/sc28.jpg"

    def scenario_twenty_nine(self):
        scenario_text = "Your community is facing air pollution due to vehicle emissions.\nWhat do you propose?"
        choices = [("Encourage biking and walking.", 10),
                   ("Support installing more public transport options.", 7),
                   ("Ignore the issue.", -5)]
        return scenario_text, choices, "scenariosimages/sc29.jpg"

    def scenario_thirty(self):
        scenario_text = "Your local river is polluted and fish are dying.\nHow do you help?"
        choices = [("Organize a cleanup and raise awareness.", 10),
                   ("Ignore the issue.", -5),
                   ("Report it to environmental agencies.", 7)]
        return scenario_text, choices, "scenariosimages/sc30.jpeg"

    def scenario_thirty_one(self):
        scenario_text = "Your office wastes a lot of paper cups.\nHow can you reduce this?"
        choices = [("Introduce a reusable cup policy.", 10),
                   ("Ignore it, it's not your problem.", -5),
                   ("Encourage recycling bins for paper cups.", 5)]
        return scenario_text, choices, "scenariosimages/sc31.png"

    def scenario_thirty_two(self):
        scenario_text = "A nearby forest is at risk due to illegal logging.\nWhat do you do?"
        choices = [("Report it to the authorities and create awareness.", 10),
                   ("Join a local conservation group.", 7),
                   ("Ignore it.", -5)]
        return scenario_text, choices, "scenariosimages/sc32.jpeg"

    def scenario_thirty_three(self):
        scenario_text = "Your city is planning a new landfill.\nHow do you respond?"
        choices = [("Advocate for recycling and waste reduction.", 10),
                   ("Support the landfill for better waste management.", -5),
                   ("Promote composting and green waste initiatives.", 7)]
        return scenario_text, choices, "scenariosimages/sc33.jpeg"

    def scenario_thirty_four(self):
        scenario_text = "Your town lacks proper recycling facilities.\nWhat do you propose?"
        choices = [("Push for a new recycling center.", 10),
                   ("Organize a recycling awareness drive.", 7),
                   ("Ignore the lack of facilities.", -5)]
        return scenario_text, choices, "scenariosimages/sc34.jpeg"

    def scenario_thirty_five(self):
        scenario_text = "Your friend always leaves lights on in empty rooms.\nWhat do you suggest?"
        choices = [("Encourage them to turn off lights when not needed.", 10),
                   ("Ignore it, it's their choice.", -5),
                   ("Install automatic light sensors.", 7)]
        return scenario_text, choices, "scenariosimages/sc35.jpg"

    def scenario_thirty_six(self):
        scenario_text = "Your local beach is suffering from an oil spill.\nWhat is your response?"
        choices = [("Join or organize a cleanup effort.", 10),
                   ("Ignore it, it's not your problem.", -5),
                   ("Raise funds for wildlife affected by the spill.", 7)]
        return scenario_text, choices, "scenariosimages/sc36.jpg"

    def scenario_thirty_seven(self):
        scenario_text = "Your community lacks bicycle lanes.\nWhat do you suggest?"
        choices = [("Propose building bicycle lanes to promote biking.", 10),
                   ("Continue driving your car.", -5),
                   ("Encourage carpooling as an alternative.", 5)]
        return scenario_text, choices, "scenariosimages/sc37.jpeg"

    def scenario_thirty_eight(self):
        scenario_text = "You see someone dumping waste illegally.\nWhat do you do?"
        choices = [("Report it to local authorities.", 10),
                   ("Confront them directly.", 5),
                   ("Ignore it, it's not your issue.", -5)]
        return scenario_text, choices, "scenariosimages/sc38.jpeg"

    def scenario_thirty_nine(self):
        scenario_text = "Your city is planning a high-rise near a natural reserve.\nWhat is your opinion?"
        choices = [("Advocate against the construction near the reserve.", 10),
                   ("Support the development for economic growth.", -5),
                   ("Propose alternative locations for the high-rise.", 7)]
        return scenario_text, choices, "scenariosimages/sc39.jpeg"

    def scenario_forty(self):
        scenario_text = "Your neighbor plans to cut down a tree for a view.\nWhat do you suggest?"
        choices = [("Suggest trimming it instead of cutting it down.", 10),
                   ("Support the cutting for a better view.", -5),
                   ("Propose planting more trees to compensate.", 7)]
        return scenario_text, choices, "scenariosimages/sc40.jpeg"

    def scenario_forty_one(self):
        scenario_text = "You learn about a plan to drain a local wetland.\nWhat is your response?"
        choices = [("Petition against draining the wetland.", 10),
                   ("Support the plan for land development.", -5),
                   ("Promote alternative land use strategies.", 7)]
        return scenario_text, choices, "scenariosimages/sc41.jpeg"

    def scenario_forty_two(self):
        scenario_text = "Your office cafeteria uses a lot of single-use plastics.\nWhat is your suggestion?"
        choices = [("Propose using biodegradable materials.", 10),
                   ("Continue using single-use plastics for convenience.", -5),
                   ("Encourage bringing personal containers.", 7)]
        return scenario_text, choices, "scenariosimages/sc42.jpeg"

    def scenario_forty_three(self):
        scenario_text = "Your local community lacks a composting program.\nWhat do you suggest?"
        choices = [("Start a community composting program.", 10),
                   ("Ignore it, composting is not necessary.", -5),
                   ("Encourage backyard composting.", 7)]
        return scenario_text, choices, "scenariosimages/sc43.jpeg"

    def scenario_forty_four(self):
        scenario_text = "You see a business dumping chemicals into a river.\nWhat action do you take?"
        choices = [("Report them to environmental authorities.", 10),
                   ("Confront them directly.", 5),
                   ("Ignore it, it doesn't affect you.", -5)]
        return scenario_text, choices, "scenariosimages/sc44.jpeg"

    def scenario_forty_five(self):
        scenario_text = "Your city has a surplus of abandoned lots.\nWhat do you propose?"
        choices = [("Turn them into community gardens.", 10),
                   ("Use them for more parking space.", -5),
                   ("Leave them as they are.", -5)]
        return scenario_text, choices, "scenariosimages/sc45.jpeg"

    def scenario_forty_six(self):
        scenario_text = "A friend wants to release a pet turtle into a nearby lake.\nWhat do you suggest?"
        choices = [("Explain the ecological impact and discourage it.", 10),
                   ("Support their decision for the turtle’s freedom.", -5),
                   ("Suggest finding a suitable home for the turtle.", 7)]
        return scenario_text, choices, "scenariosimages/sc46.jpeg"

    def scenario_forty_seven(self):
        scenario_text = "Your school is considering installing solar panels.\nWhat do you do?"
        choices = [("Support the initiative and suggest additional green measures.", 10),
                   ("Oppose it due to costs.", -5),
                   ("Encourage partial installation as a trial.", 7)]
        return scenario_text, choices, "scenariosimages/sc47.jpeg"

    def scenario_forty_eight(self):
        scenario_text = "A nearby river is drying up due to overuse.\nWhat action do you take?"
        choices = [("Organize a water conservation campaign.", 10),
                   ("Ignore it, water will come back eventually.", -5),
                   ("Encourage water-saving measures among residents.", 7)]
        return scenario_text, choices, "scenariosimages/sc48.jpeg"

    def scenario_forty_nine(self):
        scenario_text = "Your city plans to build a road through a forest.\nWhat is your stance?"
        choices = [("Protest the construction and suggest alternatives.", 10),
                   ("Support it for faster transportation.", -5),
                   ("Propose a route that minimizes damage.", 7)]
        return scenario_text, choices, "scenariosimages/sc49.jpeg"

    def scenario_fifty(self):
        scenario_text = "Your friend wants to start a garden using pesticides.\nWhat do you suggest?"
        choices = [("Encourage organic gardening methods.", 10),
                   ("Support pesticide use for better yields.", -5),
                   ("Suggest natural pest control methods.", 7)]
        return scenario_text, choices, "scenariosimages/sc50.jpeg"

    def scenario_fifty_one(self):
        scenario_text = "A local factory is releasing waste into a river.\nWhat do you do?"
        choices = [("Report the factory to environmental authorities.", 10),
                   ("Ignore it; factories need to operate.", -5),
                   ("Organize a community meeting to raise awareness.", 7)]
        return scenario_text, choices, "scenariosimages/sc51.jpeg"

    def scenario_fifty_two(self):
        scenario_text = "Your neighbor wants to cut down a large tree in their yard.\nWhat do you suggest?"
        choices = [("Advise them to keep it for its ecological benefits.", 10),
                   ("Support their decision; it's their property.", -5),
                   ("Suggest trimming it instead of cutting it down.", 7)]
        return scenario_text, choices, "scenariosimages/sc52.jpeg"

    def scenario_fifty_three(self):
        scenario_text = "Your school has a recycling program, but many students don’t participate.\nWhat action do you take?"
        choices = [("Start a campaign to promote recycling.", 10),
                   ("Let it be; it’s not a big deal.", -5),
                   ("Suggest rewards for classes that recycle the most.", 7)]
        return scenario_text, choices, "scenariosimages/sc53.jpeg"

    def scenario_fifty_four(self):
        scenario_text = "A new study shows that plastic bags are harmful to wildlife.\nHow do you respond?"
        choices = [("Advocate for a ban on plastic bags in your community.", 10),
                   ("Dismiss the study; plastic bags are convenient.", -5),
                   ("Promote reusable bags as a compromise.", 7)]
        return scenario_text, choices, "scenariosimages/sc54.png"

    def scenario_fifty_five(self):
        scenario_text = "Your community is facing an increase in air pollution.\nWhat do you propose?"
        choices = [("Organize a clean air initiative.", 10),
                   ("Ignore it; it’s not your problem.", -5),
                   ("Encourage carpooling and public transport.", 7)]
        return scenario_text, choices, "scenariosimages/sc55.jpeg"

    def scenario_fifty_six(self):
        scenario_text = "You find litter in your local park during a walk.\nWhat do you do?"
        choices = [("Pick it up and organize a cleanup day.", 10),
                   ("Leave it; someone else will handle it.", -5),
                   ("Take a photo and post about it on social media.", 7)]
        return scenario_text, choices, "scenariosimages/sc56.jpeg"

    def scenario_fifty_seven(self):
        scenario_text = "Your school is planning a field trip to an aquarium.\nHow do you feel about it?"
        choices = [("Support it as an educational experience.", 10),
                   ("Oppose it due to ethical concerns about captivity.", -5),
                   ("Suggest visiting a local wildlife reserve instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc57.jpeg"

    def scenario_fifty_eight(self):
        scenario_text = "You discover that a nearby beach is covered in oil spills.\nWhat do you do?"
        choices = [("Report it to environmental agencies immediately.", 10),
                   ("Stay away; it’s not your problem.", -5),
                   ("Join a volunteer group to clean it up.", 7)]
        return scenario_text, choices, "scenariosimages/sc58.jpg"

    def scenario_fifty_nine(self):
        scenario_text = "Your friend wants to buy a new car that gets poor gas mileage.\nWhat do you suggest?"
        choices = [("Encourage them to consider a more fuel-efficient vehicle.", 10),
                   ("Support their choice; it’s their decision.", -5),
                   ("Suggest using public transportation more often.", 7)]
        return scenario_text, choices, "scenariosimages/sc59.jpeg"

    def scenario_sixty(self):
        scenario_text = "Your family is planning to renovate your home.\nWhat do you recommend?"
        choices = [("Use sustainable materials and energy-efficient appliances.", 10),
                   ("Stick to traditional methods to save money.", -5),
                   ("Suggest a mix of both for balance.", 7)]
        return scenario_text, choices, "scenariosimages/sc60.jpeg"

    def scenario_sixty_one(self):
        scenario_text = "A community member wants to plant non-native species in the local garden.\nWhat do you say?"
        choices = [("Educate them on the risks of non-native species.", 10),
                   ("Let them plant whatever they want.", -5),
                   ("Suggest a mix of native and non-native plants.", 7)]
        return scenario_text, choices, "scenariosimages/sc61.jpeg"

    def scenario_sixty_two(self):
        scenario_text = "Your city is experiencing frequent flooding.\nWhat action do you recommend?"
        choices = [("Advocate for better drainage systems and green spaces.", 10),
                   ("Ignore it; it’s just a natural occurrence.", -5),
                   ("Suggest community meetings to discuss solutions.", 7)]
        return scenario_text, choices, "scenariosimages/sc62.jpg"

    def scenario_sixty_three(self):
        scenario_text = "A new study reveals that plastic waste is in your drinking water.\nWhat do you suggest?"
        choices = [("Advocate for water filtration systems in homes.", 10),
                   ("Dismiss it; it's not a big concern.", -5),
                   ("Help spread awareness about reducing plastic use.", 7)]
        return scenario_text, choices, "scenariosimages/sc63.jpeg"

    def scenario_sixty_four(self):
        scenario_text = "Your school is planning to ban sugary drinks but faces opposition.\nWhat do you suggest?"
        choices = [("Support the ban for health and environmental reasons.", 10),
                   ("Oppose it; students should have a choice.", -5),
                   ("Suggest offering healthier alternatives instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc64.jpg"

    def scenario_sixty_five(self):
        scenario_text = "A local park needs more wildlife habitats.\nWhat do you propose?"
        choices = [("Advocate for planting native trees and shrubs.", 10),
                   ("Think it’s not important; it’s just a park.", -5),
                   ("Organize a community project to create habitats.", 7)]
        return scenario_text, choices, "scenariosimages/sc65.jpeg"

    def scenario_sixty_six(self):
        scenario_text = "A friend wants to hunt for sport.\nWhat do you say?"
        choices = [("Express your concerns about wildlife conservation.", 10),
                   ("Support their choice; it’s their right.", -5),
                   ("Suggest learning about sustainable hunting practices.", 7)]
        return scenario_text, choices, "scenariosimages/sc66.jpeg"

    def scenario_sixty_seven(self):
        scenario_text = "You hear about a community facing water shortages.\nWhat do you do?"
        choices = [("Support initiatives for water conservation.", 10),
                   ("Think it’s just a temporary issue.", -5),
                   ("Help spread awareness about water-saving practices.", 7)]
        return scenario_text, choices, "scenariosimages/sc67.jpg"

    def scenario_sixty_eight(self):
        scenario_text = "Your school is planning a walk-to-school day.\nWhat do you do?"
        choices = [("Participate and encourage others to join.", 10),
                   ("Think it’s pointless; driving is easier.", -5),
                   ("Suggest organizing a group to walk together.", 7)]
        return scenario_text, choices, "scenariosimages/sc68.jpeg"

    def scenario_sixty_nine(self):
        scenario_text = "You discover a local wildlife shelter needs donations.\nWhat do you do?"
        choices = [("Organize a fundraising event to support it.", 10),
                   ("Assume someone else will help.", -5),
                   ("Donate your own time or resources.", 7)]
        return scenario_text, choices, "scenariosimages/sc69.jpeg"

    def scenario_seventy(self):
        scenario_text = "A local business wants to go green but doesn’t know how.\nWhat do you suggest?"
        choices = [("Offer to help them create a sustainability plan.", 10),
                   ("Think it’s too complicated for them.", -5),
                   ("Encourage them to start with small changes.", 7)]
        return scenario_text, choices, "scenariosimages/sc70.jpeg"

    def scenario_seventy_one(self):
        scenario_text = "A friend asks if you want to attend a seminar on climate change.\nWhat do you say?"
        choices = [("Definitely; it’s important to learn more.", 10),
                   ("No thanks; I’m not interested.", -5),
                   ("Let’s go together and discuss what we learn.", 7)]
        return scenario_text, choices, "scenariosimages/sc71.jpg"

    def scenario_seventy_two(self):
        scenario_text = "Your community is planning a festival to celebrate sustainability.\nWhat role do you take?"
        choices = [("Help organize activities that promote eco-friendly practices.", 10),
                   ("Think it’s just a gimmick.", -5),
                   ("Participate by sharing your own sustainable projects.", 7)]
        return scenario_text, choices, "scenariosimages/sc72.jpeg"

    def scenario_seventy_three(self):
        scenario_text = "You find out about a project to restore a local wetland.\nHow do you respond?"
        choices = [("Volunteer to help with the restoration efforts.", 10),
                   ("Think it’s not important; wetlands are overrated.", -5),
                   ("Educate others about the benefits of wetlands.", 7)]
        return scenario_text, choices, "scenariosimages/sc73.jpeg"

    def scenario_seventy_four(self):
        scenario_text = "Your community is facing extreme weather events more frequently.\nWhat do you do?"
        choices = [("Advocate for climate resilience measures.", 10),
                   ("Think it’s just a natural cycle.", -5),
                   ("Participate in local discussions about climate adaptation.", 7)]
        return scenario_text, choices, "scenariosimages/sc74.jpeg"

    def scenario_seventy_five(self):
        scenario_text = "A friend asks to throw a party with single-use decorations.\nWhat do you suggest?"
        choices = [("Advise using reusable or DIY decorations instead.", 10),
                   ("Support their choice; it's just for one night.", -5),
                   ("Offer to help create sustainable decorations.", 7)]
        return scenario_text, choices, "scenariosimages/sc75.jpeg"

    def scenario_seventy_six(self):
        scenario_text = "You notice an increase in plastic waste in your area.\nWhat action do you take?"
        choices = [("Start a plastic reduction campaign.", 10),
                   ("Assume it’s not a big deal.", -5),
                   ("Encourage friends to reduce their plastic use.", 7)]
        return scenario_text, choices, "scenariosimages/sc76.jpg"

    def scenario_seventy_seven(self):
        scenario_text = "Your school is considering installing solar panels.\nWhat do you do?"
        choices = [("Support the initiative and suggest additional green measures.", 10),
                   ("Oppose it due to costs.", -5),
                   ("Encourage partial installation as a trial.", 7)]
        return scenario_text, choices, "scenariosimages/sc77.jpeg"

    def scenario_seventy_eight(self):
        scenario_text = "You hear about a community facing food deserts.\nWhat do you do?"
        choices = [("Support local gardens and farmers' markets.", 10),
                   ("Think it’s not a problem; people can grow their own food.", -5),
                   ("Volunteer to help create community gardens.", 7)]
        return scenario_text, choices, "scenariosimages/sc78.jpg"

    def scenario_seventy_nine(self):
        scenario_text = "Your local government is debating a new recycling program.\nWhat do you suggest?"
        choices = [("Advocate for it and offer to help implement it.", 10),
                   ("Think it's a waste of resources.", -5),
                   ("Suggest a pilot program to test its effectiveness.", 7)]
        return scenario_text, choices, "scenariosimages/sc79.jpeg"

    def scenario_eighty(self):
        scenario_text = "You notice a decline in bee populations in your area.\nWhat do you do?"
        choices = [("Start a campaign to plant more flowers for bees.", 10),
                   ("Think it’s just nature’s way.", -5),
                   ("Educate others about the importance of bees.", 7)]
        return scenario_text, choices, "scenariosimages/sc80.jpeg"

    def scenario_eighty_one(self):
        scenario_text = "Your community is planning to build a new shopping center.\nWhat is your stance?"
        choices = [("Protest the development due to environmental concerns.", 10),
                   ("Support it for economic growth.", -5),
                   ("Suggest including green spaces in the plan.", 7)]
        return scenario_text, choices, "scenariosimages/sc81.jpeg"

    def scenario_eighty_two(self):
        scenario_text = "A friend wants to use chemical fertilizers in their garden.\nWhat do you suggest?"
        choices = [("Encourage organic gardening methods instead.", 10),
                   ("Support their choice for quicker results.", -5),
                   ("Suggest using natural fertilizers like compost.", 7)]
        return scenario_text, choices, "scenariosimages/sc82.jpeg"

    def scenario_eighty_three(self):
        scenario_text = "Your family is discussing how to reduce plastic use at home.\nWhat do you recommend?"
        choices = [("Implement a strict no-plastic policy.", 10),
                   ("Think it’s too difficult to change habits.", -5),
                   ("Suggest starting with small changes.", 7)]
        return scenario_text, choices, "scenariosimages/sc83.jpg"

    def scenario_eighty_four(self):
        scenario_text = "You find out about a local campaign to protect endangered species.\nWhat do you do?"
        choices = [("Join the campaign and spread the word.", 10),
                   ("Think it’s not important.", -5),
                   ("Support it by educating others about endangered species.", 7)]
        return scenario_text, choices, "scenariosimages/sc84.jpeg"

    def scenario_eighty_five(self):
        scenario_text = "You hear about a company that is greenwashing its products.\nWhat do you do?"
        choices = [("Expose the truth through social media.", 10),
                   ("Think it’s just marketing.", -5),
                   ("Encourage friends to research before buying.", 7)]
        return scenario_text, choices, "scenariosimages/sc85.jpeg"

    def scenario_eighty_six(self):
        scenario_text = "Your friend wants to travel by plane for a weekend trip.\nWhat do you suggest?"
        choices = [("Encourage them to consider more sustainable travel options.", 10),
                   ("Support their choice; it’s their vacation.", -5),
                   ("Suggest taking a train or bus instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc86.jpg"

    def scenario_eighty_seven(self):
        scenario_text = "You find out a factory is illegally dumping waste.\nWhat do you do?"
        choices = [("Report it to the authorities immediately.", 10),
                   ("Think it’s not your business.", -5),
                   ("Organize a community protest against it.", 7)]
        return scenario_text, choices, "scenariosimages/sc87.jpg"

    def scenario_eighty_eight(self):
        scenario_text = "Your local library is promoting environmental literature.\nHow do you participate?"
        choices = [("Help organize an event to discuss these topics.", 10),
                   ("Think it’s not interesting.", -5),
                   ("Borrow books to learn more and spread the word.", 7)]
        return scenario_text, choices, "scenariosimages/sc88.jpeg"

    def scenario_eighty_nine(self):
        scenario_text = "Your friend suggests using a car for every short trip.\nWhat do you say?"
        choices = [("Encourage walking or biking for short distances.", 10),
                   ("Agree; it's more convenient.", -5),
                   ("Suggest using public transport instead.", 7)]
        return scenario_text, choices, "scenariosimages/sc89.jpg"

    def scenario_ninety(self):
        scenario_text = "Your school is considering a composting program.\nWhat do you do?"
        choices = [("Support the initiative and help implement it.", 10),
                   ("Think it’s unnecessary.", -5),
                   ("Suggest starting with a pilot program.", 7)]
        return scenario_text, choices, "scenariosimages/sc90.jpeg"

    def scenario_ninety_one(self):
        scenario_text = "You hear about a local effort to ban plastic straws.\nHow do you respond?"
        choices = [("Support the ban for environmental reasons.", 10),
                   ("Think it’s just a trend.", -5),
                   ("Promote the use of reusable straws.", 7)]
        return scenario_text, choices, "scenariosimages/sc91.png"

    def scenario_ninety_two(self):
        scenario_text = "You learn about the benefits of urban green spaces.\nWhat do you do?"
        choices = [("Advocate for more green spaces in your community.", 10),
                   ("Think it’s not a priority.", -5),
                   ("Start a petition for local parks.", 7)]
        return scenario_text, choices, "scenariosimages/sc92.jpg"

    def scenario_ninety_three(self):
        scenario_text = "A friend wants to buy fast fashion items.\nWhat do you suggest?"
        choices = [("Encourage them to choose sustainable brands instead.", 10),
                   ("Support their choice; it’s trendy.", -5),
                   ("Suggest buying second-hand clothes.", 7)]
        return scenario_text, choices, "scenariosimages/sc93.jpeg"

    def scenario_ninety_four(self):
        scenario_text = "You notice more wildlife in your area due to a local conservation effort.\nHow do you feel?"
        choices = [("Celebrate the success and support further efforts.", 10),
                   ("Think it’s just a coincidence.", -5),
                   ("Get involved in conservation activities.", 7)]
        return scenario_text, choices, "scenariosimages/sc94.jpeg"

    def scenario_ninety_five(self):
        scenario_text = "You find out about a local company that is using sustainable practices.\nWhat do you do?"
        choices = [("Support and promote the business.", 10),
                   ("Think it’s just a marketing ploy.", -5),
                   ("Encourage friends to shop there.", 7)]
        return scenario_text, choices, "scenariosimages/sc95.jpeg"

    def scenario_ninety_six(self):
        scenario_text = "Your community is discussing how to improve air quality.\nWhat do you propose?"
        choices = [("Advocate for more trees and green spaces.", 10),
                   ("Think it’s not worth the effort.", -5),
                   ("Suggest community awareness programs.", 7)]
        return scenario_text, choices, "scenariosimages/sc96.jpeg"

    def scenario_ninety_seven(self):
        scenario_text = "You hear about a campaign to reduce food waste in your area.\nWhat do you do?"
        choices = [("Join the campaign and promote it.", 10),
                   ("Think it’s unnecessary; food waste happens.", -5),
                   ("Help organize local workshops on food preservation.", 7)]
        return scenario_text, choices, "scenariosimages/sc97.jpeg"

    def scenario_ninety_eight(self):
        scenario_text = "A new report highlights the importance of biodiversity.\nHow do you react?"
        choices = [("Share the report to raise awareness.", 10),
                   ("Dismiss it as another environmental study.", -5),
                   ("Encourage discussions about biodiversity in your community.", 7)]
        return scenario_text, choices, "scenariosimages/sc98.jpeg"

    def scenario_ninety_nine(self):
        scenario_text = "You hear about a local event focusing on renewable energy.\nWhat do you do?"
        choices = [("Attend and learn more about it.", 10),
                   ("Think it’s not relevant to you.", -5),
                   ("Invite friends to join and discuss afterward.", 7)]
        return scenario_text, choices, "scenariosimages/sc99.jpeg"

    def scenario_one_hundred(self):
        scenario_text = "Your school is hosting a climate change awareness week.\nHow do you participate?"
        choices = [("Help organize activities and discussions.", 10),
                   ("Think it’s not important.", -5),
                   ("Share information on social media.", 7)]
        return scenario_text, choices, "scenariosimages/sc100.jpeg"

    def run(self):
        self.app.mainloop()
if __name__=="__main__":
    root = ctk.CTk()
    game_instance = EcoAdventureGame(root)
    game_instance.run()
