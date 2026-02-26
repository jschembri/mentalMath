import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime, timedelta

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
        questions.append(f"{i}. {question}")
        answers.append(f"{i}. {answer:g}")

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
    week1 = ["multiplication", "trick1", "trick2", "additionCheck", "trick3", "trick4", "root5", "trick6", "trick5",
              "trick7", "trick6", "trick7", "trick8", "trick9"]
    tricks = week1
    trick = random.choice(tricks)

    match trick:
        case "multiplication":
            num1 = random.randint(12, 19)
            num2 = random.randint(12, 19)
            question = f"{num1} * {num2} = "
            answer = num1 * num2
        case "trick1":
            zeros1 = random.randint(-3, 3)
            zeros2 = random.randint(-3, 3)
            num1 = random.randint(2,20) * 10**zeros1
            num2 = random.randint(2,20) * 10**zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1*num2
        case "trick2":

            num2_noZero = random.randint(2, 20)
            answer_noZero = random.randint(2, 20)
            num1_noZero = num2_noZero * answer_noZero

            zeros1 = random.randint(-3, 3)
            zeros2 = random.randint(-3, 3)

            num1 = num1_noZero * 10**zeros1
            num2 = num2_noZero * 10**zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick3":
            whichOne = random.randint(0, 1)

            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 = random.randint(2,20) * 10**zeros1
                num2 = 4 * 10**zeros2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = random.randint(2,20) * 10**zeros1
                num1 = 4 * 10**zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1*num2
        case "trick4":
            num2_noZero = 4
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            zeros1 = random.randint(-3, 3)
            zeros2 = random.randint(-3, 3)

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
            question = f"{num1}^5  = "
        case "trick5":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 = random.randint(2, 99) * 10 ** zeros1
                num2 = 5 * 10 ** zeros2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = random.randint(2, 99) * 10 ** zeros1
                num1 = 5 * 10 ** zeros2
            question = f"{num1:,g} * {num2:,g} = "
            answer = num1 * num2
        case "trick6":
            num2_noZero = 5
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            zeros1 = random.randint(-3, 3)
            zeros2 = random.randint(-3, 3)

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} = "
        case "trick7":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                answer = 5 + random.randint(1, 9)*10
                question = f"{answer:,g}^2 = "
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                base5 = (5 + random.randint(1, 9) * 10)
                num1 =  base5*zeros1
                num2 =  base5*zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick8":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 =  11*zeros1
                num2 =  random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = 11 * zeros1
                num1 = random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick9":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 =  25*zeros1
                num2 =  random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = 25 * zeros1
                num1 = random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick10":
            num2_noZero = 25
            answer_noZero = random.randint(2, 99)
            num1_noZero = num2_noZero * answer_noZero

            zeros1 = random.randint(-3, 3)
            zeros2 = random.randint(-3, 3)

            num1 = num1_noZero * 10 ** zeros1
            num2 = num2_noZero * 10 ** zeros2
            answer = num1 / num2

            question = f"{num1:,g} / {num2:,g} ="
        case "trick11":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 =  99*zeros1
                num2 =  random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = 99 * zeros1
                num1 = random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick12":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num1 =  101*zeros1
                num2 =  random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                zeros1 = random.randint(-3, 3)
                zeros2 = random.randint(-3, 3)
                num2 = 101 * zeros1
                num1 = random.randint(1, 99) * zeros2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
        case "trick13":
            whichOne = random.randint(0, 1)
            if whichOne == 0:
                zeros1 = random.randint(-3, 3)
                num1 =  random.randint(11, 99) * zeros1
                num2 =  num1-2
                question = f"{num1:,g} * {num2:,g} = "
                answer = num1 * num2
            else:
                zeros2 = random.randint(-3, 3)
                num2 = random.randint(11, 99) * zeros2
                num1 = num2-2
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
            question = f"When was {random_date.strftime(%Y-%m-%d)}"
            answer = random_date.strftime("%Y-%m-%d")
        case "trick13":
            rightOrWrong = random.randint(0, 1)


            num1 = random.randint(11, 999)
            num2 = random.randint(11, 999)
            if rightOrWrong == 0:
                answer1 = num1 * num2
                answer = "Correct"
            else:
                answer1 = num1 * num2 + random.randint(9, 11)
                answer = "Wrong"
            question = f"Is this right: {num1:,g} * {num2:,g} = {answer1: ,g}"



    return question, answer


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
                print(f"Incorrect. The correct answer was {answer}\n")

        except ValueError:
            print("Please enter a valid number or 'quit'.\n")

    if total > 0:
        percentage = (correct / total) * 100
        print(f"\nYou answered {correct} out of {total} correctly.")
        print(f"Score: {percentage:.2f}%")
    else:
        print("\nNo questions answered.")


if __name__ == "__main__":
    main()