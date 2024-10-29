import tkinter as tk
import random
import os
import google.generativeai as genai
import pygame
from PIL import Image, ImageTk  # Ensure Pillow is installed

# Set your API key (make sure to use your actual API key)
os.environ["API_KEY"] = "AIzaSyBX4QAOj_iBrEPF9y2QBUNEJK4nsnq7bW0"

# Configure the AI
genai.configure(api_key=os.environ["API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[]
)


class TriviaQuizGame:
    def __init__(self, root):
        pygame.init()
        self.root = root
        self.root.title("Climate Change Trivia Quiz")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.score = 0
        self.current_round = 1
        self.yellow = (255, 255, 102)
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        # Fetch questions from the AI
        self.questions = self.fetch_questions()

        # List of quotes
        self.quotes = [
            "What we are doing to the forests of the world is but a mirror reflection of what we are doing to ourselves. — Mahatma Gandhi",
            "In nature’s economy, the law of all sentient beings is a law of love. — Albert Schweitzer",
            "The greatest threat to our planet is the belief that someone else will save it. — Robert Swan",
            "We do not inherit the Earth from our ancestors; we borrow it from our children. — Native American Proverb",
            "It's not about saving the planet; it's about saving ourselves. — Anonymous"
        ]

        self.clock = pygame.time.Clock()
        self.start_game()

    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def loading_screen(self):
        self.root.configure(bg='black')
        self.loading_label = tk.Label(self.root, text="Loading, please wait...", font=("Arial", 24),
                                      fg=self.rgb_to_hex(self.yellow),bg="black")
        self.loading_label.pack(expand=True)

        self.root.update()

        loading_start_time = pygame.time.get_ticks()
        loading_duration = 3000

        self.check_loading_duration(loading_start_time, loading_duration)

    def check_loading_duration(self, loading_start_time, loading_duration):
        if pygame.time.get_ticks() - loading_start_time < loading_duration:
            self.root.after(100, lambda: self.check_loading_duration(loading_start_time, loading_duration))
        else:
            self.loading_label.pack_forget()

    def fetch_questions(self):
        self.loading_screen()
        prompt = (
            "Generate 10 new multiple-choice questions about climate change every time. "
            "Each question should have four answer choices and clearly indicate the correct answer "
            "in the format: 'Correct Answer: [the correct answer with choice]'."
        )
        response = chat_session.send_message(prompt)
        questions = self.parse_ai_response(response.text)
        return questions

    def parse_ai_response(self, response):
        questions = []
        for q in response.split('\n\n'):
            if not q.strip():
                continue

            lines = q.strip().split('\n')
            if len(lines) < 6:
                continue  # Skip if there aren't enough lines

            question = lines[0].strip()
            choices = [line.strip() for line in lines[1:5]]

            # Extract the correct answer
            answer = ""
            for line in lines[5:]:
                if "Correct Answer:" in line:
                    answer = line.split("Correct Answer:")[1].strip().lower().replace('[', '').replace(']', '').strip()
                    break

            if not answer:
                print(f"Warning: No correct answer found for question: '{question}'")
                answer = "N/A"

            questions.append({
                "question": question,
                "choices": choices,
                "answer": answer
            })

        return questions
    def start_game(self):
        self.current_question = 0
        self.timer = 15
        self.timer_running = False
        self.timer_id = None

        # Create main layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Load and set background image
        try:
            self.bg_image = Image.open("quizgamebackground.jpg")  # Change to your image file
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.main_frame, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)  # Cover entire frame
        except Exception as e:
            print(f"Error loading image: {e}")

        # Score label
        self.score_label = tk.Label(self.main_frame, text=f"Score: {self.score}", font=("Arial", 20), fg="blue",
                                    bg="#f0f0f0")
        self.score_label.place(x=20, y=20)

        # Current round label
        self.round_label = tk.Label(self.main_frame, text=f"Round: {self.current_round}", font=("Arial", 20), fg="blue",
                                    bg="#f0f0f0")
        self.round_label.place(x=200, y=20)

        self.question_label = tk.Label(self.main_frame, text="", wraplength=600, font=("Arial", 24, "bold"),
                                       bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.timer_label = tk.Label(self.main_frame, text="", font=("Arial", 18), bg="#f0f0f0")
        self.timer_label.pack(pady=10)

        # Load hourglass image
        self.hourglass_image = Image.open("sandwatch.png")
        self.hourglass_image = self.hourglass_image.resize((50, 100), Image.LANCZOS)
        self.hourglass_photo = ImageTk.PhotoImage(self.hourglass_image)
        self.hourglass_label = tk.Label(self.main_frame, image=self.hourglass_photo, bg="#f0f0f0")
        self.hourglass_label.pack(pady=10)

        # Display the quote
        self.quote_label = tk.Label(self.main_frame, text=random.choice(self.quotes), wraplength=600,
                                    font=("Arial", 16), bg="#f0f0f0", fg="green")
        self.quote_label.pack(side=tk.BOTTOM, pady=20)

        self.choice_vars = []
        self.choice_buttons = []

        self.create_choice_buttons()
        self.show_question()

        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 20), fg="blue", bg="#f0f0f0")
        self.result_label.pack(pady=20)

        # Play Again button
        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again, font=("Arial", 16),
                                           bg="green", fg="white")
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()

        # Bind resize event to update background
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        if hasattr(self, 'bg_image'):
            self.bg_image = self.bg_image.resize((event.width, event.height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label.config(image=self.bg_photo)

    def create_choice_buttons(self):
        for i in range(4):
            var = tk.StringVar()
            button = tk.Button(self.main_frame, textvariable=var, command=lambda i=i: self.check_answer(i),
                               font=("Arial", 14), width=50, bg="#e0e0e0")  # Increased width

            button.pack(pady=10)
            self.choice_vars.append(var)

    def show_question(self):
        if self.current_question >= len(self.questions):
            self.end_game()
            return

        question = self.questions[self.current_question]
        self.question_label.config(text=question["question"])

        choices = question["choices"]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            self.choice_vars[i].set(choice)

        # Update the current round label
        self.round_label.config(text=f"Round: {self.current_question + 1}")

        self.start_timer()

    def start_timer(self):
        self.timer = 15
        self.update_timer_label()
        self.timer_running = True
        self.countdown()

    def update_timer_label(self):
        self.timer_label.config(text=f"Time remaining: {self.timer} seconds")

    def countdown(self):
        if self.timer > 0 and self.timer_running:
            self.timer -= 1
            self.update_timer_label()
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            self.check_answer(-1)

    def check_answer(self, index):
        if self.current_question >= len(self.questions):
            self.end_game()
            return

        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        question = self.questions[self.current_question]

        selected_answer = self.choice_vars[index].get() if index != -1 else None

        feedback = ""

        if selected_answer is None:
            feedback = f"Time's up! The correct answer was '{question['answer']}'" if index == -1 else "No answer selected."
        else:
            correct_answer_cleaned = question["answer"].strip().lower().replace(')', '').replace('(', '').replace(' ',
                                                                                                                  '')
            selected_answer_cleaned = selected_answer.strip().lower().replace(')', '').replace('(', '').replace(' ', '')

            print(f"Selected Answer: '{selected_answer_cleaned}', Correct Answer: '{correct_answer_cleaned}'")

            if selected_answer_cleaned == correct_answer_cleaned:
                self.score += 1
                feedback = "Correct! Good job."
            else:
                feedback = f"Incorrect. The correct answer was '{correct_answer_cleaned}'"

        self.score_label.config(text=f"Score: {self.score}")
        self.display_feedback(feedback)

    def display_feedback(self, feedback):
        self.result_label.config(text=feedback)
        self.result_label.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_forget()

        self.root.after(3000, self.next_question)

    def next_question(self):
        self.result_label.pack_forget()
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.current_question += 1

        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.end_game()

    def end_game(self):
        final_score = f"Your final score: {self.score}/{len(self.questions)}"
        self.result_label.config(text=final_score)
        self.result_label.pack()
        self.play_again_button.pack()

    def play_again(self):
        self.current_question = 0
        self.score = 0
        self.result_label.config(text="")
        self.play_again_button.pack_forget()
        self.questions = self.fetch_questions()  # Fetch new questions
        self.show_question()


if __name__ == "__main__":
    root = tk.Tk()
    game = TriviaQuizGame(root)
    root.mainloop()
