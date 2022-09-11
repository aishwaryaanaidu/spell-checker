import re
import string
from collections import defaultdict

title_dict = {
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Misses",
    "Ms.": "Miss"
}


def process_regex(file_path):
    print("Processing file...")
    # Opening the file in read mode
    text_file = open(file_path, 'r')
    # Storing all the contents of the file into a variable
    text = text_file.read()
    # Substituting all the occurrences of titles with their appropriate expansions of words
    for key, value in title_dict.items():
        text = re.sub(key, value, text)

    output_file = open("regex.txt", "w")
    output_file.write(text)
    output_file.close()
    print("Output stored to “regex.txt”")


def get_unique_words(text):
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    stripped_words = [w.translate(table) for w in words]
    stripped_words = [word.lower() for word in stripped_words]
    # Removes strings containing numbers and alphanumeric characters
    stripped_words = [item for item in stripped_words if item.isalpha()]
    # Remove duplicate words
    unique_words = list(set(stripped_words))
    return unique_words


def normalize_text(regex_file_path):
    print("Normalizing text...")
    # Opening the file in read mode
    text_file = open(regex_file_path, 'r')
    # Storing all the contents of the file into a variable
    text = text_file.read()
    # words = text.split()
    # table = str.maketrans('', '', string.punctuation)
    # stripped_words = [w.translate(table) for w in words]
    # stripped_words = [word.lower() for word in stripped_words]
    # # Removes strings containing numbers and alphanumeric characters
    # stripped_words = [item for item in stripped_words if item.isalpha()]
    # # Remove duplicate words
    # unique_words = list(set(stripped_words))
    unique_words = get_unique_words(text)
    # Sort the list in alphabetical order
    unique_words.sort()
    print(unique_words)
    with open('dictionary.txt', 'w') as f:
        for word in unique_words:
            f.write(word)
            f.write('\n')
    print("Output stored to “dictionary.txt”")


def edit_distance(str1, str2, m, n):
    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m - 1] == str2[n - 1]:
        return edit_distance(str1, str2, m - 1, n - 1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(edit_distance(str1, str2, m, n - 1),  # Insert
                   edit_distance(str1, str2, m - 1, n),  # Remove
                   edit_distance(str1, str2, m - 1, n - 1)  # Replace
                   )

def spell_checker():
    # process_regex("pg41537.txt")
    # normalize_text("regex.txt")
    print("Welcome to the spell checker!")
    print("Please enter a text to check spelling or enter quit to exit the program.")
    print("-----------------------------------------")
    input_text = input("Enter text to be checked:")
    unique_words = get_unique_words(input_text)
    print(unique_words)
    dictionary_file = open("dictionary.txt", 'r')
    # misspelled_words = defaultdict([])
    misspelled_words = {}
    word_dictionary = dictionary_file.read()
    for word in unique_words:
        if word not in word_dictionary:
            misspelled_words[word] = ""
    word_dictionary_list = word_dictionary.split()
    if len(misspelled_words.keys()) > 0:
        print(misspelled_words)
        for word in misspelled_words.keys():
            min_distance = float("inf")
            suggested_word = ""
            for item in word_dictionary_list:
                distance = edit_distance(word, item, len(word), len(item))
                if distance <= min_distance:
                    min_distance = distance
                    suggested_word = item
                misspelled_words[word] = suggested_word

        print("Misspelling - Suggestion")
        print("------------------------")
        for item, value in misspelled_words.items():
            print("{} - {}".format(item, value))

    else:
        print("No misspellings detected!")


spell_checker()
