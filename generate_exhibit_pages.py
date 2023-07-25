import string
from fpdf import FPDF  # fpdf2 not fpdf1


def main():  # only for if run as script
    # ====== #
    # Inputs #
    start_exhibit = "A"
    # start_exhibit = 1
    end_exhibit = "AAA"
    # end_exhibit = 100
    affidavit = "Test"
    day = 1
    month = "April"
    year = 2023
    province = "Ontario"
    #        #
    # ====== #

    if type(start_exhibit) is str:
        pdf = generate_letter_pdf(
            start_exhibit, end_exhibit, affidavit, day, month, year, province
        )
    elif type(start_exhibit) is int:
        pdf = generate_num_pdf(
            start_exhibit, end_exhibit, affidavit, day, month, year, province
        )
    else:
        raise ValueError('start_exhibit must be a string ("a") or integer (1)')
    
    pdf.output(name="exhibits.pdf")
    return


def generate_letter_pdf(
    start_exhibit, end_exhibit, affidavit, day, month, year, province
):
    start_exhibit_num = exhibit_letter_to_num(start_exhibit)
    end_exhibit_num = exhibit_letter_to_num(end_exhibit)

    pdf = PDF(format="Letter")
    for exhibit_num in range(start_exhibit_num, end_exhibit_num + 1):
        pdf.add_page()
        pdf.add_exhibit_page(
            exhibit_num_to_letter(exhibit_num),
            affidavit,
            day,
            month,
            year,
            province,
        )

    return pdf


def generate_num_pdf(
    start_exhibit, end_exhibit, affidavit, day, month, year, province
):
    pdf = PDF(format="Letter")
    for exhibit_num in range(start_exhibit, end_exhibit + 1):
        pdf.add_page()
        pdf.add_exhibit_page(
            exhibit_num,
            affidavit,
            day,
            month,
            year,
            province,
        )

    return pdf


class PDF(FPDF):
    def add_exhibit_page(
        self,
        exhibit="_____",  # Exhibit letter
        affidavit="________________",  # affidavit name
        day="___",  # day sworn
        month="______________",  # month sworn
        year="____",  # year sworn
        province="__________",  # province of commissioner
        bookmark_prefix="Exhibit",  # prefix for the bookmark to the exhibit pg
        font="Times",  # Courier, Helvetica, Times
        font_style="B",  # B for bold
        font_sz=12,  # Font size
        draw_border=True,  # Surround text with a border
        ln_height=8,  # Line height
        str_override="",
    ):  # Override default text with any string
        self.start_section(f"{bookmark_prefix} {exhibit}", level=0)
        self.set_xy(self.w / 6, self.h / 4)
        self.set_font(font, font_style, font_sz)

        if str_override:
            text = str_override
        else:
            text = (f'This is Exhibit "{exhibit}" '
                    f'referred to in the Affidavit of {affidavit} '
                    f'sworn (or affirmed) before me this '
                    f'{day}{get_day_suffix(day)} '
                    f'day of {month}, {year}.\n\n'
                    f'_________________________________________\n'
                    f'A Commisioner/Notary Public '
                    f'for the Province of {province}')

        self.multi_cell(
            w=(2 * self.w) / 3,
            h=ln_height,
            align="C",
            border=draw_border,
            txt=text,
        )


def exhibit_letter_to_num(letter):
    # Using iteration A ... AA, BB rather than permutation A ... AA, AB
    letter_to_num = {
        char: i + 1 for (i, char) in enumerate(string.ascii_uppercase)
    }
    return 26 * (len(letter) - 1) + letter_to_num[letter[-1].upper()]


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
    main()
