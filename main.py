import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime, timedelta

def vertical_addition(numbers):
    # Find the width needed (widest number + space for + sign)
    max_width = max(len(str(n)) for n in numbers)
    total = sum(numbers)
    total_width = len(str(total))
    col_width = max(max_width, total_width)
    question = "\n"
    # Print each number, right-aligned, with + on the last one
    for i, n in enumerate(numbers):
        if i == len(numbers) - 1:
            question = question + f"+ {str(n).rjust(col_width)}\n"
        else:
            question = question + f"   {str(n).rjust(col_width)}\n"

    # Print the dividing line
    question = question + "  " + "-" * (col_width+2) + "\n"
    return question


def number_to_letter(n):
    return chr((n - 1) % 26 + 65)

def digital_root(n: int) -> int:
    """
    Reduce a number to its single-digit digital root by repeatedly
    summing its digits. This is the core of 'casting out nines'.
    A result of 9 is kept as 9 (not reduced to 0).
    """
    n = abs(int(n))
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def cast_out_nines(operation: str, a: int | float, b: int | float, result: int | float) -> dict:
    """
    Check whether an arithmetic result is POSSIBLY correct or DEFINITELY WRONG
    using the casting-out-nines technique.

    Supports: addition (+), subtraction (-), multiplication (*).
    Note: Division is unreliable with this method and is not supported.

    Returns a dict with:
        - 'verdict'  : 'POSSIBLY CORRECT' or 'DEFINITELY WRONG'
        - 'details'  : step-by-step explanation (human-readable)
    """
    operation = operation.strip()
    if operation not in ('+', '-', '*'):
        raise ValueError("Supported operations: '+', '-', '*'")

    dr_a      = digital_root(a)
    dr_b      = digital_root(b)
    dr_result = digital_root(result)

    # Apply the operation to the digital roots, then reduce again
    if operation == '+':
        expected = digital_root(dr_a + dr_b)
        op_name  = "addition"
        formula  = f"{dr_a} + {dr_b} = {dr_a + dr_b} → reduces to {expected}"
    elif operation == '-':
        diff     = dr_a - dr_b
        if diff < 0:
            diff += 9          # wrap around for subtraction
        expected = digital_root(diff)
        op_name  = "subtraction"
        formula  = f"{dr_a} - {dr_b} = {dr_a - dr_b} → adjusted to {diff} → reduces to {expected}"
    elif operation == '*':
        expected = digital_root(dr_a * dr_b)
        op_name  = "multiplication"
        formula  = f"{dr_a} × {dr_b} = {dr_a * dr_b} → reduces to {expected}"

    match = (expected == dr_result)
    verdict = "✅ POSSIBLY CORRECT" if match else "❌ DEFINITELY WRONG"

    details = (
        f"Operation : {a} {operation} {b} = {result}  ({op_name})\n"
        f"  Digital root of {a:>12} → {dr_a}\n"
        f"  Digital root of {b:>12} → {dr_b}\n"
        f"  Digital root of {result:>12} → {dr_result}\n"
        f"  Apply operation to roots : {formula}\n"
        f"  Expected digital root    : {expected}\n"
        f"  Actual  digital root     : {dr_result}\n"
        f"  Verdict : {verdict}\n"
        f"  Reminder: 'Possibly correct' does NOT guarantee the answer is right —\n"
        f"            it only means the check did not catch an error."
    )

    return {"verdict": verdict, "details": details, "match": match}


def create_math_pdf(filename, num_questions=30):
    """
    Creates a PDF with division questions on page 1
    and answers on page 2.
    """

    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    questions = []
    answers = []

    # Generate questions
    for i in range(1, num_questions*2 + 1):
        question, answer = generate_question()
        questions.append(f"{number_to_letter(i)}) {question}")
        answers.append(f"{number_to_letter(i)}) {answer}")

    # ----- QUESTIONS PAGE -----
    elements.append(Paragraph("<b>Math Division Quiz</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))


    elements.append(Paragraph("<b>Questions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Split into two columns (20 left, 20 right)
    left_column = questions[:num_questions]
    right_column = questions[num_questions:]

    left_answers = answers[:num_questions]
    right_answers = answers[num_questions:]


    # Combine into table rows
    table_data = []
    for left, right in zip(left_column, right_column):
        table_data.append([left, right])

    table = Table(table_data, colWidths=[3 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))

    elements.append(table)

    # Page break before answers
    elements.append(PageBreak())

    # ----- ANSWERS PAGE -----
    elements.append(Paragraph("<b>Answers</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    table_data = []
    for left, right in zip(left_answers, right_answers):
        table_data.append([left, right])

    table = Table(table_data, colWidths=[3 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)

def generate_question():
    tricks = []
    week1 = ["multiplication", "trick1", "trick2", "additionCheck", "trick3", "trick4","trick5", "trick6", "trick5",
              "trick7", "trick6", "trick7", "trick8", "trick9", "trick10", "trick11", "trick12", "trick13", "trick14"]
    week2 = ["trick15", "trick16", "trick17", "trick18", "trick19", "trick20", "trick21", "trick22", "trick23",
             "trick24", "trick25", "trick26", "trick27", "trick28"]
    week3 = ["trick30"]#3, "trick30"]
    parlorTricks = ["root5", "parlor2" ]
    if parlorMode:
        tricks = tricks + parlorTricks
    tricks = week3
    # tricks = ["trick28"]
    trick = random.choice(tricks)
    if zerosMode:
        zeros1 = random.randint(-3, 3)
        zeros2 = random.randint(-3, 3)
    else:
        zeros1 = 0
        zeros2 = 0
    whichOne = random.randint(0, 1)
    match trick:
        case "multiplication":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                num1 = random.randint(3, 19)
                num2 = random.randint(12, 19)
            else:
                num2 = random.randint(3, 19)
                num1 = random.randint(12, 19)
            question = f"{num1} * {num2} = "
            answer = num1 * num2
        case "trick1":
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0
            num1 = random.randint(2,20) * 10**zeros1
            num2 = random.randint(2,20) * 10**zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1*num2
        case "trick2":

            num2_noZero = random.randint(2, 20)
            answer_noZero = random.randint(2, 20)
            num1_noZero = num2_noZero * answer_noZero

            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            num1 = num1_noZero * 10**zeros1
            num2 = num2_noZero * 10**zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick3":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 = random.randint(2,20) * 10**zeros1
                num2 = 4 * 10**zeros2
            else:
                num2 = random.randint(2,20) * 10**zeros1
                num1 = 4 * 10**zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1*num2
        case "trick4":
            num2_noZero = 4
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "

        case "additionCheck":
            num1 = random.randint(2, 100)
            num2 = random.randint(2, 100)
            num3 = random.randint(2, 100)
            question = f"{num1} + {num2} + {num3}  = "
            answer = num1 + num2 + num3
        case "root5":
            answer = random.randint(2, 99)
            num1 = answer**5.
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                question = f"{answer}^5  = "
            else:
                question = f"{answer}*{answer}  = "
        case "trick5":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 = random.randint(2, 99) * 10 ** zeros1
                num2 = 5 * 10 ** zeros2
            else:
                num2 = random.randint(2, 99) * 10 ** zeros1
                num1 = 5 * 10 ** zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1 * num2
        case "trick6":
            num2_noZero = 5
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick7":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                num1 = 5 + random.randint(1, 9)*10
                question = f"{num1:,g}^2 = "
                answer = num1 * num1
            else:
                if zerosMode:
                    zeros1 = random.randint(-3, 3)
                    zeros2 = random.randint(-3, 3)
                else:
                    zeros1 = 0
                    zeros2 = 0
                base5 = (5 + random.randint(1, 9) * 10)
                num1 =  base5*10**zeros1
                num2 =  base5*10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick8":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 =  11*10**zeros1
                num2 =  random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 11 * 10**zeros1
                num1 = random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick9":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 =  25*10**zeros1
                num2 =  random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 25 * 10**zeros1
                num1 = random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick10":
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            num2_noZero = 25
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} ="
        case "trick11":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 =  99*10**zeros1
                num2 =  random.randint(1, 99) *10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 99 * 10**zeros1
                num1 = random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick12":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 =  101*10**zeros1
                num2 =  random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 101 * 10**zeros1
                num1 = random.randint(1, 99) * 10**zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick13":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1_nozeros = random.randint(11, 99)
                num1 =  num1_nozeros* 10**zeros1
                num2 =  num1_nozeros-2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2_nozeros = random.randint(11, 99)
                num2 =  num2_nozeros* 10**zeros2
                num1 = num2_nozeros-2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "parlor2":
            start_date = datetime(1990, 1, 1)
            end_date = datetime(2026, 12, 31)
        # Calculate difference in days
            delta = end_date - start_date

            # Pick a random number of days
            random_days = random.randint(0, delta.days)

            # Generate random date
            random_date = start_date + timedelta(days=random_days)

            # Print date and weekday
            question = f"What day was {random_date.strftime('%Y-%m-%d')}: "
            answer = random_date.strftime("%A")
        case "trick14":
            rightOrWrong = random.randint(0, 1)

            num1 = random.randint(11, 999)
            num2 = random.randint(11, 999)
            if rightOrWrong == 0:
                answer1 = num1 * num2
                answer = "Maybe Yes"
            else:
                answer1 = num1 * num2 + random.randint(1, 8)
                check = cast_out_nines("*", num1, num2, answer1)
                while check['match']:
                    answer1 = num1 * num2 + random.randint(1, 8)
                    check = cast_out_nines("*", num1, num2, answer1)

                answer = "No"
            question = f"{num1:,g} * {num2:,g} = {answer1: ,g} Maybe Yes or No. "
        case "trick15":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 = 125 * 10 ** zeros1
                num2 = random.randint(11, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 125 * 10 ** zeros1
                num1 = random.randint(1, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick16":
            num2_noZero = 125
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick17":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 = 9 * 10 ** zeros1
                num2 = random.randint(11, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 9 * 10 ** zeros1
                num1 = random.randint(1, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick18":
            whichOne = random.randint(0, 1)
            if zerosMode:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
            else:
                zeros1 = 0
                zeros2 = 0

            if whichOne == 0:
                num1 = 12 * 10 ** zeros1
                num2 = random.randint(11, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                num2 = 12 * 10 ** zeros1
                num1 = random.randint(1, 99) * 10 ** zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick19":
            num1 = 15 * 10 ** zeros1
            num2 = random.randint(11, 99) * 10 ** zeros2
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick20":
            tensDigit = random.randint(1,9)*10
            onesDigit_num1 = random.randint(1,9)
            onesDigit_num2 = 10 - onesDigit_num1
            num1 = (tensDigit + onesDigit_num1)* 10 ** zeros1
            num2 = (tensDigit + onesDigit_num2) * 10 ** zeros2
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick21":
            num1 = (random.randint(1, 9)+0.5) * 10 ** zeros1
            num2 = random.randint(1, 49)*2 * 10 ** zeros2
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick22":
            num2_noZero =  (random.randint(1, 9)+0.5)
            answer_noZero = random.randint(2, 40)
            num1_noZero = num2_noZero * answer_noZero

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick23":
            num1noZeroes = 5 * 10 + random.randint(1, 9)
            num1 = num1noZeroes* 10 ** zeros1
            answer = num1 * num1
            if whichOne == 0:
                question = f"{num1:,g} * {num1:,g} = "
            else:
                question = f"{num1:,g}^2 = "
        case "trick24":
            num1noZeroes = (random.randint(1, 9)) * 10 + 1
            num1 = num1noZeroes* 10 ** zeros1
            answer = num1 * num1
            if whichOne == 0:
                question = f"{num1:,g} * {num1:,g} = "
            else:
                question = f"{num1:,g}^2 = "
        case "trick25":
            num1 = random.randint(12, 99)
            num2 = random.randint(13, 99)
            # width = max(len(str(num1)), len(str(num2)), len(str(num1 * num2))) + 4
            # question = f"{num1:>{width}}\n" + f"    x {num2:>{width - 2}}\n" + f"-" * width + "\n"
            question = f"{num1} * {num2} = "
            answer = num1 * num2
        case "trick26":
            num1noZero = random.randint(8, 20)
            num2noZero = num1noZero + 4
            num1 = num1noZero * 10 ** zeros1
            num2 = num2noZero * 10 ** zeros2
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick27":
            num1 = random.randint(2, 9) * random.randint(2, 4) * 10 ** zeros1
            num2 = random.randint(11, 20)* 10 ** zeros2
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick28":
            num1_tens = random.randint(1, 33)
            num2_tens = random.randint(1, 33)
            while num1_tens * num2_tens > 99:
                num1_tens = random.randint(1, 33)
                num2_tens = random.randint(1, 33)
            num1 = 100 + num1_tens
            num2 = 100 + num2_tens
            answer = num1 * num2
            if whichOne == 0:
                question = f"{num1:,g} * {num2:,g} = "
            else:
                question = f"{num2:,g} * {num1:,g} = "
        case "trick29":
            numbers = []
            for i in range(0, random.randint(3, 6)):
                numbers.append(random.randint(6, 99))
            answer = sum(numbers)
            question = " + ".join(str(n) for n in numbers) + " = "
        case "trick30":
            numbers = []
            for i in range(0, random.randint(3, 7)):
                numbers.append(random.randint(100, 999))
            answer = sum(numbers)
            question =  vertical_addition(numbers)
    return question, answer

parlorMode = False
zerosMode = False
def main():
    total = 0
    correct = 0

    print("Math Quiz! Type 'quit' to stop.")
    print("Type 'pdf' for a pdf. \n")

    while True:
        question, answer = generate_question()
        user_input = input(question)

        if user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "q":
            break

        if user_input.lower() == "pdf":
            create_math_pdf("mathProblems.pdf", 32)
            break

        try:
            user_answer = float(user_input)
            total += 1

            if abs(user_answer - answer) < 0.0001:
                print("Correct!\n")
                correct += 1
            else:
                print(f"Incorrect. The correct answer was {answer:,g}\n")

        except ValueError:
            try:
                if user_input.lower() == answer.lower():
                    print("Correct!\n")
                    correct += 1
                else:
                    print(f"Incorrect. The correct answer was {answer}\n")
                total += 1
            except:
                print("Please enter a valid number or 'quit'.\n")

    if total > 0:
        percentage = (correct / total) * 100
        print(f"\nYou answered {correct} out of {total} correctly.")
        print(f"Score: {percentage:.2f}%")
    else:
        print("\nNo questions answered.")


if __name__ == "__main__":
    main()