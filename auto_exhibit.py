import string
from fpdf import FPDF

class PDF(FPDF):
    def add_exhibit_id(self
                       , exhibit="_____"
                       , affidavit="________________"
                       , day="___"
                       , month="______________"
                       , year="____"
                       , province="__________"
                       , bookmark_prefix="Exhibit"
                       , font="Times"
                       , font_style="B"
                       , font_sz=12
                       , draw_border=True
                       , ln_height=8
                       , str_override=""):

        self.start_section(f"{bookmark_prefix} {exhibit}", level=0)
        self.set_xy(pdf.w/6, pdf.h/4)
        self.set_font(font, font_style, font_sz)

        if str_override:
            text = str_override
        else:
            text = f"This is Exhibit \"{exhibit}\" referred to in the Affidavit of {affidavit} sworn (or affirmed) before me this {day}{get_day_suffix(day)} day of {month} {year}.\n\n_________________________________________\nA Commisioner/Notary Public for the Province of {province}"

        self.multi_cell(w=(2*pdf.w)/3
                  , h=ln_height
                  , align='C'
                  , border=draw_border
                  , txt=text)

def exhibit_letter_to_num(letter):
    # Using iteration A ... AA, BB rather than permutation A ... AA, AB
    letter_to_num = {char: i + 1 for (i, char) in enumerate(string.ascii_uppercase)}
    return 26 * (len(letter) - 1) + letter_to_num[letter[-1]]

def exhibit_num_to_letter(num):
    # Using A ... AA, BB rather than true permutations A ... AA, AB
    num_to_letter = string.ascii_uppercase
    if num % 26 == 0:
        return "Z" * (num // 26)
    else:
        return num_to_letter[(num % 26) - 1] * ((num // 26) + 1)

def get_day_suffix(day):
    unit_digit = day % 10
    if unit_digit > 3 or unit_digit == 0 or day % 100 in [11, 12, 13]:
        return "th"
    elif unit_digit == 1:
        return "st"
    elif unit_digit == 2:
        return "nd"
    elif unit_digit == 3:
        return "rd"

if __name__ == "__main__":
    pdf = PDF(format='Letter')

    start_exhibit = "A"
    end_exhibit = "AAAAA"
    affidavit = "Test"
    day = 1
    month = "April"
    year = 2023
    province = "Ontario"

    start_exhibit_num = exhibit_letter_to_num(start_exhibit)
    end_exhibit_num = exhibit_letter_to_num(end_exhibit)

    for exhibit_num in range(start_exhibit_num, end_exhibit_num + 1):
        exhibit = exhibit_num_to_letter(exhibit_num)
        pdf.add_page()
        pdf.add_exhibit_id(exhibit_num_to_letter(exhibit_num), affidavit, day, month, year, province)

    pdf.output(name="exhibits.pdf")