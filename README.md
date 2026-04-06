Lab 1 - Grade Evaluator & Archiver

This project includes a Python script that evaluate student grades from a CSV file and a Bash script to archive the current `grades.csv` file for future use.

 1.Files Included
 
- grade-evaluator.py
- organizer.sh
- README.md
- grades.csv (for testing)

 2.Requirements
 
- Python 3
- Bash (Linux/macOS or WSL)

 3.Running the Python Script

1. Make sure `grade-evaluator.py` and `grades.csv` are in the same folder.
2. Run the script:

   python3 grade-evaluator.py

3. When asked, enter:

   grades.csv

 4.What the Python Script Does

- Checks that all scores are between 0 and 100
- Verifies total weight = 100
- Verifies Formative = 60 and Summative = 40
- Calculates final grade and GPA using:

  GPA = (Total Grade / 100) * 5

- Determines pass or fail
- If failed, shows which formative assignment(s) can be resubmitted

 5.Pass Rule
 
A student passes only if both:
- Formative ≥ 50%
- Summative ≥ 50%

 6.Running the Shell Script

1. Give permission:

   chmod +x organizer.sh

2. Run:

   ./organizer.sh

 7.What the Shell Script Does

- Creates an archive folder if it doesn't exist
- Renames grades.csv using a timestamp
- Moves it into the archive folder
- Creates a new empty grades.csv
- Logs the operation in organizer.log

# Example Log Entry

20260401-101530 | grades.csv | grades_20260401-101530.csv

## Example Output

Final Grade: 60.00%
GPA: 3.00 / 5.00
Formative Average: 56.67%
Summative Average: 65.00%
Final Status: PASSED
No re-submission needed.
