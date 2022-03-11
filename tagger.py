import sys
import re

# Tag counter
word_tag_freq_matrix = {}

# Collect the command line args
train_file_path = sys.argv[1]
test_file_path = sys.argv[2]

train_file = open(train_file_path, "r", encoding="utf-8")  # Open file for reading
train_file_text = train_file.read()  # Reading...
train_file.close()  # We close our files in this house!!

lines = train_file_text.split("\n")  # Parse line by line
for l in lines:
    clean_l = re.sub(r"(^\[\s)|(\s\])", "", l)  # Removing those annoying brackets
    toks = clean_l.split(" ")  # Tokens are delimited by whitespace
    for t in toks:
        word = t.split("/")[0]  # Word comes before /
        tag = t.split("/")[1]  # Tag comes after /

        # Add information discovered to the matrix
        if word not in word_tag_freq_matrix:  # If word is not there we need to define it
            word_tag_freq_matrix[word] = {tag: 1}
        elif tag not in word_tag_freq_matrix[word]:  # If we haven't found this tag for this word, we need to init it
            word_tag_freq_matrix[word][tag] = 1
        else:  # Otherwise, just add 1 to the entry
            word_tag_freq_matrix[word][tag] += 1

