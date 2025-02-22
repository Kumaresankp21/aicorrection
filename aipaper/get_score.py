import re


def extract_score_from_report(data):
    # Extract marks_awarded and max_marks using regex
    awarded_marks = re.findall(r'"marks_awarded":\s*(\d+)', data)
    max_marks = re.findall(r'"max_marks":\s*(\d+)', data)

    # Convert extracted marks to integers
    awarded_marks = list(map(int, awarded_marks))
    max_marks = list(map(int, max_marks))

    # Calculate scores
    user_score = sum(awarded_marks)
    total_possible_score = sum(max_marks)

    return user_score