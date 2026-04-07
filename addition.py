import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def generate_problem():
    """Generate an addition problem with 4-6 numbers, each 1-3 digits."""
    count = random.randint(4, 6)
    numbers = [random.randint(1, 999) for _ in range(count)]
    return numbers


def draw_problem(c, x, y, numbers, problem_num):
    """Draw a single addition problem at position (x, y). Returns height used."""
    font_name = "Courier-Bold"
    num_font_size = 18
    line_font_size = 16

    # Decide layout: single-line or stacked (vertical)
    layout = random.choice(["stacked", "single"])

    c.setFont(font_name, 12)
    c.setFillColor(colors.grey)
    c.drawString(x, y, f"#{problem_num}")
    c.setFillColor(colors.black)
    y -= 18

    if layout == "single":
        # Single line: 12 + 34 + 567 = ___
        expr = " + ".join(str(n) for n in numbers)
        c.setFont(font_name, num_font_size)
        c.drawString(x, y, f"{expr} = _______")
        height_used = 18 + 30
    else:
        # Stacked vertical addition
        max_digits = max(len(str(n)) for n in numbers)
        col_width = 14  # pixels per digit character
        num_width = (max_digits + 1) * col_width  # a bit of padding

        c.setFont(font_name, num_font_size)
        row_height = 24

        for i, num in enumerate(numbers):
            num_str = str(num).rjust(max_digits)
            if i == len(numbers) - 1:
                # Last number: draw '+' sign before it
                c.drawString(x, y, f"+ {num_str}")
            else:
                c.drawString(x + col_width, y, num_str)
            y -= row_height

        # Draw line
        line_x_start = x
        line_x_end = x + num_width + col_width
        c.setLineWidth(1.5)
        c.line(line_x_start, y + 6, line_x_end, y + 6)
        y -= 20

        # Answer blank
        c.setFont(font_name, num_font_size)
        blank = "_" * (max_digits + 2)
        c.drawString(x + col_width, y, blank)

        height_used = (len(numbers) + 2) * row_height + 30

    return height_used + 20  # extra padding between problems


def generate_worksheet(filename="addition_worksheet.pdf", num_problems=20):
    c = canvas.Canvas(filename, pagesize=letter)
    page_width, page_height = letter

    margin = 50
    col_gap = 40
    col_width = (page_width - 2 * margin - col_gap) / 2

    # Title
    def draw_header(c):
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor("#2c3e50"))
        c.drawCentredString(page_width / 2, page_height - 40, "Addition Practice Worksheet")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.grey)
        c.drawCentredString(page_width / 2, page_height - 58, "Name: ________________________   Date: ________________")
        c.setFillColor(colors.black)
        c.setLineWidth(1)
        c.line(margin, page_height - 68, page_width - margin, page_height - 68)

    draw_header(c)

    top_y = page_height - 90
    col_positions = [margin, margin + col_width + col_gap]

    col_y = [top_y, top_y]
    min_y = margin + 20  # bottom margin
    col_idx = 0
    problem_num = 1

    while problem_num <= num_problems:
        numbers = generate_problem()

        # Estimate height for this problem (stacked needs more)
        estimated_height = (len(numbers) + 4) * 24 + 30

        x = col_positions[col_idx]
        y = col_y[col_idx]

        if y - estimated_height < min_y:
            # Move to other column or new page
            other_col = 1 - col_idx
            if col_y[other_col] - estimated_height >= min_y:
                col_idx = other_col
                x = col_positions[col_idx]
                y = col_y[col_idx]
            else:
                # New page
                c.showPage()
                draw_header(c)
                col_y = [top_y, top_y]
                col_idx = 0
                x = col_positions[col_idx]
                y = col_y[col_idx]

        used = draw_problem(c, x, y, numbers, problem_num)
        col_y[col_idx] -= used
        col_idx = 1 - col_idx  # alternate columns
        problem_num += 1

    c.save()
    print(f"Worksheet saved as '{filename}' with {num_problems} problems.")


if __name__ == "__main__":
    generate_worksheet("addition_worksheet.pdf", num_problems=20)