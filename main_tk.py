import tkinter as tk
from tkinter import messagebox
from pillow import Image, ImageTk
import random


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("1280x720")

        # Label to display the question
        self.question_label = tk.Label(root, text="Question will appear here", wraplength=500, font=("Arial", 14))
        self.question_label.pack(pady=20)

        # Frame to hold the answer buttons
        self.answer_frame = tk.Frame(root)
        self.answer_frame.pack(pady=10)

        # Answer buttons (4 buttons)
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(self.answer_frame, text=f"Answer {i+1}", width=50, height=2,
                            command=lambda idx=i: self.check_answer(idx))
            btn.grid(row=i, column=0, pady=5)
            self.answer_buttons.append(btn)

        # Lifeline Buttons
        self.lifeline_frame = tk.Frame(root)
        self.lifeline_frame.pack(pady=10)

        self.fifty_fifty_button = tk.Button(self.lifeline_frame, text="50/50", command=self.use_fifty_fifty, state=tk.NORMAL)
        self.fifty_fifty_button.grid(row=0, column=0, padx=10)

        self.skip_button = tk.Button(self.lifeline_frame, text="Skip", command=self.use_skip, state=tk.NORMAL)
        self.skip_button.grid(row=0, column=1, padx=10)

        self.hint_button = tk.Button(self.lifeline_frame, text="Hint", command=self.use_hint, state=tk.NORMAL)
        self.hint_button.grid(row=0, column=2, padx=10)

        # Score Label
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Initialize some variables for the game state
        self.current_question = 0
        self.questions = []  # This will be populated with question data
        self.score = 0
        self.lifelines_used = {"fifty_fifty": False, "skip": False, "hint": False}

    def load_questions(self, questions):
        """Load the questions into the app and start the game."""
        self.questions = questions
        self.show_next_question()

    def show_next_question(self):
        """Display the next question and answers."""
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data['question'])

            # Set the answers to the buttons
            options = [question_data['right_answer']] + question_data['wrong_answers']
            random.shuffle(options)  # Shuffle answers to randomize their order
            for i, option in enumerate(options):
                self.answer_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            # No more questions, show the final score
            self.show_final_score()

    def check_answer(self, selected_index):
        """Check if the selected answer is correct."""
        question_data = self.questions[self.current_question]
        correct_answer = question_data['right_answer']
        selected_answer = self.answer_buttons[selected_index].cget("text")
        if selected_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror("Wrong!", f"Oops! The correct answer was: {correct_answer}")
        
        self.current_question += 1
        self.update_score()
        self.show_next_question()

    def use_fifty_fifty(self):
        """Use 50/50 lifeline."""
        if not self.lifelines_used["fifty_fifty"]:
            self.lifelines_used["fifty_fifty"] = True
            question_data = self.questions[self.current_question]
            correct_answer = question_data['right_answer']
            wrong_answers = question_data['wrong_answers']

            # Randomly hide two wrong answers (just as an example)
            wrong_to_hide = random.sample(wrong_answers, 2)
            for i, btn in enumerate(self.answer_buttons):
                if btn.cget("text") in wrong_to_hide:
                    btn.config(state=tk.DISABLED)

            self.fifty_fifty_button.config(state=tk.DISABLED)

    def use_skip(self):
        """Use skip lifeline."""
        if not self.lifelines_used["skip"]:
            self.lifelines_used["skip"] = True
            self.current_question += 1
            self.show_next_question()
            self.skip_button.config(state=tk.DISABLED)

    def use_hint(self):
        """Use hint lifeline."""
        if not self.lifelines_used["hint"]:
            self.lifelines_used["hint"] = True
            question_data = self.questions[self.current_question]
            hint = question_data.get('hint', 'No hint available.')
            messagebox.showinfo("Hint", hint)
            self.hint_button.config(state=tk.DISABLED)

    def update_score(self):
        """Update the score label."""
        self.score_label.config(text=f"Score: {self.score}")

    def show_final_score(self):
        """Display the final score when all questions are done."""
        messagebox.showinfo("Quiz Over", f"Your final score is: {self.score}")
        self.root.quit()


# Example questions data
def get_questions():
    """Simulate fetching questions, could be replaced with actual data fetching."""
    return [
        {
            "question": "Who directed the movie 'Inception'?",
            "right_answer": "Christopher Nolan",
            "wrong_answers": ["Steven Spielberg", "James Cameron", "Ridley Scott"],
            "hint": "He also directed 'The Dark Knight' trilogy."
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "right_answer": "Mars",
            "wrong_answers": ["Jupiter", "Saturn", "Venus"],
            "hint": "It is the fourth planet from the Sun."
        },
        {
            "question": "What is the capital of France?",
            "right_answer": "Paris",
            "wrong_answers": ["Rome", "Berlin", "Madrid"],
            "hint": "The city is famous for the Eiffel Tower."
        },
        {
            "question": "What is the powerhouse of the cell?",
            "right_answer": "Mitochondria",
            "wrong_answers": ["Nucleus", "Ribosome", "Chloroplast"],
            "hint": "It generates energy in the cell."
        }
    ]

def show_frame(frame):
    frame.tkraise()

def handle_selection(category):
    global username  # Use the global variable to store the username
    username = entry.get()  # Get the username input
    if username:  # Ensure the user entered a username
        selected_category.set(f"Username: {username}, Category: {category}")
        show_frame(frame2)  # Go to the next screen
    else:
        error_label.config(text="Please enter a username!")

# Create the main window
root = tk.Tk()
root.title("Username and Category Example")
root.geometry("800x600")

# Create a container to hold the frames
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Configure the grid layout to stack frames on top of each other
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create two frames (screens)
frame1 = tk.Frame(container)
frame2 = tk.Frame(container)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nsew")

# Global variable to store username
username = ""


# Load and display an image (must be PNG or GIF)
img = Image.open("static/heisenberg.png")
resized_image = img.resize((150, 150), Image.ANTIALIAS)

photo = ImageTk.PhotoImage(resized_image)

label = tk.Label(root, image=photo)
label.image = photo

# Create a label to display the image
label = tk.Label(root, image=img)
label.pack(pady=20)

# ----- Frame 1 Content (User Input and Category Selection) -----
label1 = tk.Label(frame1, text="Hello stranger.", font=('Helvetica', 12))
label1.pack(pady=5)
label1 = tk.Label(frame1, text="I welcome you to a game of Who Wants to Be a Trivia Master?", font=('Helvetica', 12))
label1.pack(pady=5)
label1 = tk.Label(frame1, text="I invite you to test your knowledge.", font=('Helvetica', 12))
label1.pack(pady=5)
label1 = tk.Label(frame1, text="If you dare.", font=('Helvetica', 12))
label1.pack(pady=5)



# Entry widget for username input
entry = tk.Entry(frame1, width=30)
entry.pack(pady=5)

# Error label for missing username
error_label = tk.Label(frame1, text="", fg="red", font=('Helvetica', 10))
error_label.pack()

# Category selection buttons
categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6']

for category in categories:
    button = tk.Button(frame1, text=category, width=20,
                       command=lambda c=category: handle_selection(c))
    button.pack(pady=5)

# ----- Frame 2 Content (Display Username and Category) -----
selected_category = tk.StringVar()
selected_category.set("")

label2 = tk.Label(frame2, textvariable=selected_category, font=('Helvetica', 14))
label2.pack(pady=20)

button_back = tk.Button(frame2, text="Go Back", command=lambda: show_frame(frame1))
button_back.pack(pady=10)

# Show the first frame initially
show_frame(frame1)

# Start the GUI loop
root.mainloop()

#
# def main_tk():
#     roots = tk.Tk()
#     app = QuizApp(roots)
#     app.load_questions(get_questions())  # Load questions into the app
#     roots.mainloop()
#
#
#
#
# if __name__ == "__main__":
#     main_tk()
#
