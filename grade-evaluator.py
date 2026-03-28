import csv
import os

# opens the grades file
def get_grades_csv(filepath):
    # stop if file is missing
    if not os.path.exists(filepath):
        print("Error: grades.csv not found.")
        return None

    assignments = []
    # read the file row by row
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            assignments.append(row)

    # stop if file has no data
    if not assignments:
        print("Error: grades.csv is empty. No data to process.")
        return None

    # check column names are correct
    required_columns = {"assignment", "group", "score", "weight"}
    if not required_columns.issubset(set(assignments[0].keys())):
        print("Error: CSV is missing required columns.")
        return None

    return assignments

# checks every score is between 0 and 100
def grades_validator(assignments):
    errors = []
    for a in assignments:
        score = float(a["score"])
        # flag bad scores
        if not (0 <= score <= 100):
            errors.append(f"  - '{a['assignment']}' has an invalid score: {score}")
    return errors

# checks all weights add up correctly
def weights_validator(assignments):
    errors = []
    total = 0
    formative_total = 0
    summative_total = 0

    for a in assignments:
        weight = float(a["weight"])
        atype = a["group"].strip().lower()
        total += weight
        # sort weight into the right group
        if atype == "formative":
            formative_total += weight
        elif atype == "summative":
            summative_total += weight

    # check the three weight rules
    if round(total, 2) != 100:
        errors.append(f"  - Total weight is {total:.2f} (must equal exactly 100)")
    if round(formative_total, 2) != 60:
        errors.append(f"  - Formative weights sum to {formative_total:.2f} (must equal 60)")
    if round(summative_total, 2) != 40:
        errors.append(f"  - Summative weights sum to {summative_total:.2f} (must equal 40)")

    return errors

# does all the grade calculations
def calculate_results(assignments):
    formative_assignments = []
    summative_assignments = []

    # split into two groups
    for a in assignments:
        atype = a["group"].strip().lower()
        score = float(a["score"])
        weight = float(a["weight"])
        if atype == "formative":
            formative_assignments.append({**a, "score": score, "weight": weight})
        elif atype == "summative":
            summative_assignments.append({**a, "score": score, "weight": weight})

    # formative score
    formative_earned = sum((a["score"] / 100) * a["weight"] for a in formative_assignments)
    formative_max = sum(a["weight"] for a in formative_assignments)
    formative_pct = (formative_earned / formative_max * 100) if formative_max else 0

    # summative score
    summative_earned = sum((a["score"] / 100) * a["weight"] for a in summative_assignments)
    summative_max = sum(a["weight"] for a in summative_assignments)
    summative_pct = (summative_earned / summative_max * 100) if summative_max else 0

    # total grade and gpa
    total_grade = formative_earned + summative_earned
    gpa = (total_grade / 100) * 5.0

    # must pass both categories to pass overall
    passed = formative_pct >= 50 and summative_pct >= 50

    # find failed formatives for resubmission
    failed_formatives = [a for a in formative_assignments if a["score"] < 50]
    resubmit = []
    if failed_formatives:
        # pick the one with the highest weight
        max_weight = max(a["weight"] for a in failed_formatives)
        resubmit = [a for a in failed_formatives if a["weight"] == max_weight]

    return {
        "formative_pct": formative_pct,
        "summative_pct": summative_pct,
        "total_grade": total_grade,
        "gpa": gpa,
        "passed": passed,
        "resubmit": resubmit,
    }

# prints the final report
def print_report(assignments, results):
    print("\n" + "=" * 50)
    print("       GRADE EVALUATOR — STUDENT REPORT")
    print("=" * 50)

    print("\nASSIGNMENT BREAKDOWN")
    print(f"  {'Assignment':<30} {'Type':<12} {'Weight':>7} {'Score':>7}")
    for a in assignments:
        print(f"  {a['assignment']:<30} {a['group']:<12} {float(a['weight']):>6.1f}% {float(a['score']):>6.1f}%")

    print("\nCATEGORY SCORES")
    print(f"  Formative  : {results['formative_pct']:.2f}%")
    print(f"  Summative  : {results['summative_pct']:.2f}%")

    print("\nOVERALL RESULTS")
    print(f"  Total Grade: {results['total_grade']:.2f} / 100")
    print(f"  GPA        : {results['gpa']:.2f} / 5.0")
    status = "PASSED" if results["passed"] else "FAILED"
    print(f"  Status     : {status}")

    print("\nRESUBMISSION")
    if results["resubmit"]:
        for a in results["resubmit"]:
            print(f"    - {a['assignment']} (Weight: {a['weight']:.1f}%, Score: {a['score']:.1f}%)")
    else:
        print("  No resubmission needed.")

# runs everything in order
def main():
    GRADES_FILE = "grades.csv"

    assignments = get_grades_csv(GRADES_FILE)
    if assignments is None:
        return

    grade_errors = grades_validator(assignments)
    weight_errors = weights_validator(assignments)
    all_errors = grade_errors + weight_errors

    if all_errors:
        print("Validation failed:")
        for e in all_errors:
            print(e)
        return

    results = calculate_results(assignments)
    print_report(assignments, results)

# start here
if __name__ == "__main__":
    main()
