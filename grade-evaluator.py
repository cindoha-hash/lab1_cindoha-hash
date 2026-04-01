#!/usr/bin/python3
import csv
import sys
import os

"""Ask for the CSV file name and load its rows."""
def load_csv_data():
    filename = input("Enter the name of the CSV file to process").strip()

    if not os.path.exists(filename):
        print(f"Error:'{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"Error:'The {filename}' was empty.")
                sys.exit(1)

            required_fields = ['assignment', 'group', 'score', 'weight']
            missing_fields = []

            for field in required_fields:
                if field not in reader.fieldnames:
                    missing_fields.append(field)

            if missing_fields:
                print("Error: Missing required column(s): " + ", ".join(missing_fields))
                sys.exit(1)

            for row in reader:
                if not any(row.values()):
                    continue

                try:
                    assignments.append({
                        'assignment': row['assignment'].strip(),
                        'group': row['group'].strip(),
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except ValueError:
                    print("Error: Score and weight must be numbers.")
                    sys.exit(1)

        if not assignments:
            print("Error: The CSV file has no grade records to process.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def validate_scores(data):
    """Make sure all scores are between 0 and 100."""
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(
                f"Error: Score for '{item['assignment']}' must be between 0 and 100."
            )
            return False
    return True


def validate_weights(data):
    """Check that the weights add up correctly."""
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
    invalid_groups = []

    for item in data:
        total_weight += item['weight']
        group_name = item['group'].strip().lower()

        if group_name == 'formative':
            formative_weight += item['weight']
        elif group_name == 'summative':
            summative_weight += item['weight']
        else:
            invalid_groups.append(item['group'])

    if invalid_groups:
        print("Error: Invalid group name(s): " + ", ".join(sorted(set(invalid_groups))))
        return False

    if round(total_weight, 2) != 100:
        print(f"Error: Total weight must be 100, but got {total_weight}.")
        return False

    if round(formative_weight, 2) != 60:
        print(f"Error: Formative weight must be 60, but got {formative_weight}.")
        return False

    if round(summative_weight, 2) != 40:
        print(f"Error: Summative weight must be 40, but got {summative_weight}.")
        return False

    return True


def calculate_results(data):
    """Work out the final grade, category averages, and GPA."""
    final_grade = 0
    formative_weighted_total = 0
    summative_weighted_total = 0
    formative_weight = 0
    summative_weight = 0

    for item in data:
        weighted_score = (item['score'] * item['weight']) / 100
        final_grade += weighted_score

        if item['group'].strip().lower() == 'formative':
            formative_weighted_total += weighted_score
            formative_weight += item['weight']
        else:
            summative_weighted_total += weighted_score
            summative_weight += item['weight']

    formative_percentage = 0
    summative_percentage = 0

    if formative_weight > 0:
        formative_percentage = (formative_weighted_total / formative_weight) * 100

    if summative_weight > 0:
        summative_percentage = (summative_weighted_total / summative_weight) * 100

    gpa = (final_grade / 100) * 5.0

    return {
        'final_grade': final_grade,
        'gpa': gpa,
        'formative_percentage': formative_percentage,
        'summative_percentage': summative_percentage
    }


def get_resubmissions(data):
    """Find failed formative assignments with the highest weight."""
    failed_formative = []

    for item in data:
        if item['group'].strip().lower() == 'formative' and item['score'] < 50:
            failed_formative.append(item)

    if not failed_formative:
        return []

    highest_weight = failed_formative[0]['weight']
    for item in failed_formative[1:]:
        if item['weight'] > highest_weight:
            highest_weight = item['weight']

    eligible = []
    for item in failed_formative:
        if item['weight'] == highest_weight:
            eligible.append(item)

    return eligible


def evaluate_grades(data):
    """Calculate the results, and print them."""
    print("\n--- Processing Grades ---")

    if not validate_scores(data):
        sys.exit(1)

    if not validate_weights(data):
        sys.exit(1)

    results = calculate_results(data)
    status = "PASSED"

    if results['formative_percentage'] < 50 or results['summative_percentage'] < 50:
        status = "FAILED"

    resubmissions = get_resubmissions(data)

    print(f"Final Grade: {results['final_grade']:.2f}%")
    print(f"GPA: {results['gpa']:.2f} / 5.00")
    print(f"Formative Average: {results['formative_percentage']:.2f}%")
    print(f"Summative Average: {results['summative_percentage']:.2f}%")
    print(f"Final Status: {status}")

    if status == "FAILED":
        if resubmissions:
            print("Eligible formative assignment(s) for re-submission:")
            for item in resubmissions:
                print(
                    f" - {item['assignment']} "
                    f"(Score: {item['score']:.2f}%, Weight: {item['weight']:.2f}%)"
                )
        else:
            print("No formative assignment is eligible for re-submission.")
    else:
        print("No re-submission needed.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
