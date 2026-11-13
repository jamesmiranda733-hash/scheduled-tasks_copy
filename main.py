import datetime, random, smtplib
import csv

with open('birthdays.csv') as birthday:
    reader = csv.DictReader(birthday)
    bd_data = list(reader)

MY_EMAIL = "jamesmiranda733@gmail.com"
MY_PASSWORD = "wzkttvzptzeyjvvb"
ALL_LETTERS = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
dt = datetime.datetime.now()
CURRENT_DAY = dt.day
CURRENT_MONTH = dt.month
for data in bd_data:
    birthday_date = int(data["day"])
    birthday_month = int(data["month"])
    if CURRENT_DAY == birthday_date and CURRENT_MONTH == birthday_month:
        name_of_person = data["name"]
        persons_email =data["email"]
        chosen_letter = random.choice(ALL_LETTERS)
        with open(chosen_letter, 'r') as letter:
            line_1 = letter.readline()
            replaced_line = line_1.replace("[NAME]", name_of_person)
            rest_of_letter = letter.read()
        with open(chosen_letter, 'w') as letter:
            letter.write(replaced_line)
            letter.write(rest_of_letter)

        with open(chosen_letter, 'r') as letter:
            finished_letter = letter.read()

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr =MY_EMAIL,
                                to_addrs = persons_email,
                                msg = "Subject: Good Morning and Happy Birthday! <3  \n\n"
                                f"{finished_letter}")
