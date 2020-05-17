#!/home/bsuuv/Ohjelmistoprojektit/venv/bin python
import os

from model.Classes import XlsxManager, Dao, JsonManager, EventHandler


def lists_to_dict(categories, tags):
    dictionary = {}

    categories_tags = zip(categories, tags)

    for category, tags in categories_tags:
        dictionary[category] = tags

    return dictionary


def choose_dir():
    while True:
        print("Path to directory containing your bank accounts events:")
        path = input()

        if not os.path.exists(path):
            print("Path does not exist.")
            continue
        elif os.path.isfile(path):
            print("The path you gave was to a file, but a path to a directory is needed!")
            continue
        else:
            break

    return path


def setup_settings():
    global language
    global transactions_dir

    settings = database.read_settings()
    if settings is None:
        print("It seems we'll have to do some settings before we begin\n")
        choose_settings()
    else:
        print("Would you like to edit your settings? Type Y for yes or N for no.")
        edit_settings = input()

        if edit_settings == "Y":
            choose_settings()
            return
        else:
            language, transactions_dir = settings


def set_categories_and_tags():
    global jsonManager
    global eventhandler

    categories = []

    # Lista, joka sisältää listoja, joista jokaisessa on tiettyyn kategoriaan kuuluvat tunnisteet.
    tags = []

    while True:
        print("Input category name. Type OK to finish setting up categories and tags.")
        category_name = input()

        if category_name == "OK":
            break

        categories.append(category_name)

        tags_of_category = []
        while True:
            print("""Input tags, parts of the receiver/sender strings of the transaction that can be used to 
            identify, which category the transaction belongs to. To finish inputting tags, type OK.""")
            tag = input()

            if tag == "OK":
                break

            tags_of_category.append(tag)

        tags.append(tags_of_category)

    dictionary = lists_to_dict(categories, tags)

    eventhandler.categories_tags_dict = dictionary
    jsonManager.write_tags(dictionary)


def choose_settings():
    global transactions_dir

    transactions_dir = choose_dir()

    print("Would you like to reset your categories and tags? Y for yes or N for no")
    reset = input()

    if reset == "Y":
        set_categories_and_tags()

    database.write_settings(transactions_dir)


database = Dao("localhost", "root", "mariaonihana", "fa")
jsonManager = JsonManager()
eventhandler = EventHandler()

language = ""
transactions_dir = ""

setup_settings()

print("Calculating incomes and expenses of the month...")
# TODO: omaa syötettyä kategoriaa ei ilmesty tähän sanakirjaan
values_by_category = eventhandler.calculate_values_by_category()

print("Writing results to talousseuranta_autom.xlsx...")

try:
    xlsxmanager = XlsxManager()
    xlsxmanager.write_month(values_by_category)
except FileNotFoundError as e:
    print(e.strerror, "\n\nFatal error")
