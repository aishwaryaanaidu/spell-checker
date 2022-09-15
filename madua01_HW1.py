import re
import string
import os


# A dictionary containing the abbreviated titles and their associated expansions of words
title_dict = {
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Misses",
    "Ms.": "Miss"
}


# This method performs initial processing on the input file using regex
def process_regex(file_path):
    print("Processing file...")
    # Opening the file in read mode
    text_file = open(file_path, 'r')
    # Storing all the contents of the file into a variable
    text = text_file.read()
    # Substituting all the occurrences of titles with their appropriate expansions of words
    for key, value in title_dict.items():
        text = re.sub(key, value, text)

    """ 
        Substituting all British spellings with American spellings. This method basically looks for 
        words ending with our or ours and replaces it with or and ors respectively. But this functionality has flaws.
        Since we are looking for words ending with our or ours, it fails to substitute our in words like
        "neighbourhood", "neighbouring".
    """
    text = re.sub(r'([a-zA-Z]{2,})(our|ours)\b', r'\1or', text)
    # Write the processed output to regex.txt
    output_file = open("regex.txt", "w")
    output_file.write(text)
    output_file.close()
    print("Output stored to “regex.txt” \n")


# Method used to get unique words from a given string
def get_unique_words(text):
    # Splits the words using space as the delimiter
    words = text.split()
    # Removes punctuations from the list of words
    table = str.maketrans('', '', string.punctuation)
    stripped_words = [w.translate(table) for w in words]
    # Converts words to lower case for case insensitive comparison
    stripped_words = [word.lower() for word in stripped_words]
    # Removes strings containing numbers and alphanumeric characters
    stripped_words = [item for item in stripped_words if item.isalpha()]
    # Removes duplicate words
    unique_words = list(set(stripped_words))
    return unique_words


# Method used to normalize text
def normalize_text(regex_file_path):
    print("Normalizing text...")
    # Opening the file in read mode
    text_file = open(regex_file_path, 'r')
    # Storing all the contents of the file into a variable
    text = text_file.read()
    # Getting unique set of words
    unique_words = get_unique_words(text)
    # Sort the list in alphabetical order
    unique_words.sort()
    # Storing the alphabetically sorted words in a file
    with open('dictionary.txt', 'w') as f:
        for word in unique_words:
            f.write(word)
            f.write('\n')
    print("Output stored to “dictionary.txt” \n")


# Method used to calculate edit distance between two strings
def edit_distance(word1, word2, m, n):

    # If either length of either of the words is 0 return the other word
    if m == 0:
        return n

    if n == 0:
        return m

    # If the length is not 0 we use recursion to calculate the distance
    if word1[m - 1] == word2[n - 1]:
        return edit_distance(word1, word2, m-1, n-1)

    return 1 + min(edit_distance(word1, word2, m, n - 1),  # Insert
                   edit_distance(word1, word2, m - 1, n),  # Remove
                   edit_distance(word1, word2, m - 1, n - 1)  # Replace
                   )


def spell_checker(input_text):
    """
        Method containing the logic to check for misspellings and provide suggestions. We first find a list of
        misspelled words and then find the edit distance for just the misspelled words. The words from the dictionary
        which have minimum edit distance from the misspelled word will be returned as the result
    """
    # Finds unique words
    unique_words = get_unique_words(input_text)

    dictionary_file = open("dictionary.txt", 'r')
    # A dictionary used to store the misspelled words as the key and the correct spellings as the value
    misspelled_words = {}
    # Store the contents of the dictionary file to check if a particular word exists in the dictionary
    word_dictionary = dictionary_file.read()
    # Populate the dictionary with misspelled words as the key and set the correct value to an empty string
    # as we still don't know the correct spelling
    for word in unique_words:
        if word not in word_dictionary:
            misspelled_words[word] = ""
    # Form a list of the words in the dictionary
    word_dictionary_list = word_dictionary.split()
    # We first check to see if there are any misspelled words
    if len(misspelled_words.keys()) > 0:
        # If there are any misspelled words we find the minimum edit distance
        for word in misspelled_words.keys():
            # Initializing the minimum distance to infinity
            min_distance = float("inf")
            suggested_word = ""
            for item in word_dictionary_list:
                distance = edit_distance(word, item, len(word), len(item))
                # If the minimum distance is less than the newly calculated distance, we replace the minimum distance
                # and store the correct spelling of the word with minimum distance
                if distance <= min_distance:
                    min_distance = distance
                    suggested_word = item
                # Populate the dictionary with the misspelled word and the correct spelling
                misspelled_words[word] = suggested_word
        print("Misspelling - Suggestion")
        print("------------------------")
        # Print the misspelled word and the correct spelling
        for item, value in misspelled_words.items():
            print("{} - {}".format(item, value))

    else:
        print("No misspellings detected!")


if __name__ == '__main__':
    """
        Main function that drives the program. The program takes about 10 seconds to produce the output
    """
    # Take the path to the file which contains the text from which a dictionary needs to be created
    text_file_path = input("Enter the path to the file which needs to be used to create word dictionary: ")
    # Check if the file is present at the path entered by the user
    if not os.path.isfile(text_file_path):
        text_file_path = input("Incorrect file path. Please enter the correct path: ")

    # Complete initial processing of the file
    process_regex(text_file_path)
    # Normalize the text
    normalize_text("regex.txt")

    print("Welcome to the spell checker!")
    print("Please enter a text to check spelling or enter quit to exit the program.")
    print("-----------------------------------------")

    # Keep prompting the user to enter a text to be checked till the user enters "quit"
    while True:
        entered_text = input("Enter text to be checked:")
        if entered_text.lower() == "quit":
            print("Goodbye!")
            break
        else:
            spell_checker(entered_text)
