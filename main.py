from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

class FlashcardApp:
    def __init__(self, root):
        self.window = root
        self.window.title("LearnIt!")
        self.window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
        
        # Initialize variables
        self.data = None
        self.prompt_title = "Term"
        self.answer_title = "Definition"
        self.prompt_list = None
        self.answer_list = None
        self.current_index = 0
        self.card_is_flipped = False
        self.to_learn = None  # List of indices for terms to learn
        self.file_path = None  # Store the original CSV file path
        
        # Set up UI elements
        self.setup_ui()
        
        # Start with upload prompt
        self.show_upload_prompt()
        
        # Bind the closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Card canvas
        self.cardfront = Canvas(width=800, height=526)
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        self.card_front = self.cardfront.create_image(400, 263, image=self.card_front_img)
        self.prompttitle = self.cardfront.create_text(400, 163, text="Welcome to LearnIt!", font=("Arial", 40, "italic"))
        self.prompt_text = self.cardfront.create_text(400, 263, text="Please upload a CSV file to begin", font=("Arial", 12, "bold"))
        self.cardfront.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.cardfront.grid(row=0, column=0, columnspan=4)
        
        # Buttons
        self.correct_img = PhotoImage(file="images/right.png")
        self.correct_button = Button(image=self.correct_img, command=self.mark_correct)
        self.correct_button.grid(row=1, column=2)
        self.correct_button.config(state=DISABLED)
        
        self.flip_button = Button(text="See Answer", height=5, width=40, command=self.flip)
        self.flip_button.grid(row=1, column=1)
        self.flip_button.config(state=DISABLED)
        
        self.wrong_img = PhotoImage(file="images/wrong.png")
        self.wrong_button = Button(image=self.wrong_img, command=self.mark_wrong)
        self.wrong_button.grid(row=1, column=0)
        self.wrong_button.config(state=DISABLED)
        
        # Upload button
        self.upload_button = Button(text="Upload CSV", height=2, width=20, command=self.upload_csv)
        self.upload_button.grid(row=1, column=3)
    
    def show_upload_prompt(self):
        self.cardfront.itemconfig(self.prompttitle, text="Welcome to LearnIt!")
        self.cardfront.itemconfig(self.prompt_text, text="Please upload a CSV file to begin")
        self.cardfront.itemconfig(self.card_front, image=self.card_front_img)
        
        # Disable flashcard buttons
        self.correct_button.config(state=DISABLED)
        self.flip_button.config(state=DISABLED)
        self.wrong_button.config(state=DISABLED)
        
        # Enable upload button
        self.upload_button.config(state=NORMAL)
    
    def upload_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                
                # Ensure the CSV has at least 2 columns
                if len(self.data.columns) < 2:
                    messagebox.showerror("Invalid CSV", "The CSV file must have at least 2 columns.")
                    return
                
                # Get column names for prompt and answer
                self.prompt_title = self.data.columns[0]
                self.answer_title = self.data.columns[1]
                
                # Get data lists
                self.prompt_list = self.data.iloc[:, 0]
                self.answer_list = self.data.iloc[:, 1]
                
                # Initialize to_learn with all indices
                self.to_learn = list(range(len(self.prompt_list)))
                self.file_path = file_path  # Store the file path
                
                # Enable flashcard buttons
                self.correct_button.config(state=NORMAL)
                self.flip_button.config(state=NORMAL)
                self.wrong_button.config(state=NORMAL)
                
                # Start first card
                self.next_card()
                
                # Update app title with the loaded file name
                file_name = os.path.basename(file_path)
                self.window.title(f"LearnIt! - {file_name}")
                
                # Hide upload button during study session
                self.upload_button.grid_remove()
                
                # Add a new button to load different file
                self.new_file_button = Button(text="Load Different File", height=2, width=20, command=self.reset_app)
                self.new_file_button.grid(row=1, column=3)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load CSV file: {str(e)}")
    
    def next_card(self):
        self.card_is_flipped = False
        if self.to_learn:  # Check if there are terms to learn
            self.current_index = random.choice(self.to_learn)
            prompt = self.prompt_list.iloc[self.current_index]
            self.cardfront.itemconfig(self.card_front, image=self.card_front_img)
            self.cardfront.itemconfig(self.prompttitle, text=self.prompt_title)
            self.cardfront.itemconfig(self.prompt_text, text=str(prompt))
            self.flip_button.config(state=NORMAL)
            self.correct_button.config(state=NORMAL)
            self.wrong_button.config(state=NORMAL)
        else:  # All terms are memorized
            self.cardfront.itemconfig(self.card_front, image=self.card_front_img)
            self.cardfront.itemconfig(self.prompttitle, text="Congratulations!")
            self.cardfront.itemconfig(self.prompt_text, text="All terms are memorized!")
            self.flip_button.config(state=DISABLED)
            self.correct_button.config(state=DISABLED)
            self.wrong_button.config(state=DISABLED)
    
    def flip(self):
        if not self.card_is_flipped and self.to_learn:
            self.card_is_flipped = True
            answer = self.answer_list.iloc[self.current_index]
            self.cardfront.itemconfig(self.card_front, image=self.card_back_img)
            self.cardfront.itemconfig(self.prompttitle, text=self.answer_title)
            self.cardfront.itemconfig(self.prompt_text, text=str(answer))
        elif self.card_is_flipped:
            self.card_is_flipped = False
            prompt = self.prompt_list.iloc[self.current_index]
            self.cardfront.itemconfig(self.card_front, image=self.card_front_img)
            self.cardfront.itemconfig(self.prompttitle, text=self.prompt_title)
            self.cardfront.itemconfig(self.prompt_text, text=str(prompt))
    
    def mark_correct(self):
        # Mark the current term as memorized by removing it from to_learn
        if self.current_index in self.to_learn:
            self.to_learn.remove(self.current_index)
        self.next_card()
    
    def mark_wrong(self):
        # Term is not memorized, keep it in to_learn and move to next card
        self.next_card()
    
    def reset_app(self):
        # Reset to initial state
        self.data = None
        self.prompt_list = None
        self.answer_list = None
        self.to_learn = None
        self.file_path = None
        
        # Hide the new file button
        self.new_file_button.grid_remove()
        
        # Show the upload button again
        self.upload_button.grid()
        
        # Show upload prompt
        self.show_upload_prompt()
    
    def on_closing(self):
        # Save terms to learn when closing the app
        if self.data is not None and self.to_learn is not None:
            if len(self.to_learn) > 0:
                # Create a DataFrame with only the terms still to learn
                to_learn_df = self.data.iloc[self.to_learn]
                base, ext = os.path.splitext(self.file_path)
                new_path = base + "_to_learn" + ext
                to_learn_df.to_csv(new_path, index=False)
                messagebox.showinfo("Saved", f"Saved to {new_path}")
            else:
                messagebox.showinfo("All Memorized", "All terms are memorized. No file saved.")
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    app = FlashcardApp(root)
    root.mainloop()