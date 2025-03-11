## LearnIt!
A simple flashcard application built with Tkinter that allows users to study terms and definitions from a CSV file.
The app tracks which terms have been memorized and saves the remaining terms to learn in a new CSV file when the app is closed.

## Features
Load terms and definitions from a CSV file.
Randomly presents terms for study.
Flip cards to see the definition.
Mark terms as memorized or not memorized.
Saves unmemorized terms to a new CSV file upon closing.
Option to load a different CSV file during a study session.
## Usage
Upload CSV File:
- Click the "Upload CSV" button to select a CSV file.
The CSV must have at least two columns:
First column: Terms (prompts)
Second column: Definitions (answers)
## Study Flashcards:
The app displays a term from the CSV file.
Click "See Answer" to flip the card and view the definition.
If you knew the answer, click the "Correct" button (marks the term as memorized and removes it from the to-learn list).
If you didn't know the answer, click the "Wrong" button (keeps the term in the to-learn list).
The app will randomly present another term from the remaining to-learn list.
## Completion:
When all terms are memorized, a congratulatory message is displayed, and the flashcard buttons are disabled.
If you close the app before memorizing all terms, the remaining terms are saved to a new CSV file (e.g., original_file_to_learn.csv).
## Load a Different File:
During a study session, you can click "Load Different File" to reset the app and upload a new CSV file.
## Running the Application
Ensure you have Python 3.x installed on your system.
Install the required libraries:
pip install tkinter pandas
Save the script as main.py, (or anything you want make sure to add the .py at the end though)
Run the script:
python main.py

## License
This project is licensed under the MIT License.
