import sys
import re

# Tag counter
word_tag_freq_matrix = {}

# Output string
out = ""

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
        if len(t.split("/")) >= 2:  # Handling for edge cases, AKA empty string
            word = t.split("/")[0]  # Word comes before /
            tag = t.split("/")[1]  # Tag comes after /
            if "|" in tag:
                tag = tag.split("|")[0]

        # Add information discovered to the matrix
        if word not in word_tag_freq_matrix:  # If word is not there we need to define it
            word_tag_freq_matrix[word] = {tag: 1}
        elif tag not in word_tag_freq_matrix[word]:  # If we haven't found this tag for this word, we need to init it
            word_tag_freq_matrix[word][tag] = 1
        else:  # Otherwise, just add 1 to the entry
            word_tag_freq_matrix[word][tag] += 1

# Time to run algo on test file
test_file = open(test_file_path, "r", encoding='utf-8')
test_file_text = test_file.read()
test_file.close()  # Closed files are good files.

test_lines = test_file_text.split("\n")
for l in test_lines:
    brackets = re.search(r"(^\[\s)|(\s\])", l)
    if brackets:  # I want to be sure to print out the brackets when required to.
        clean_l = re.sub(r"(^\[\s)|(\s\])", "", l)  # Buuuuut for parsing they're annoying, so bye!
        toks = clean_l.split(" ")
        out += "["  # Since this line had brackets, it will have brackets on output
        for t in toks:  # Go through each word
            if t in word_tag_freq_matrix:  # If it's in the matrix, find the max
                max_inst = 0
                max_tag = ""
                for tag in word_tag_freq_matrix[t]:
                    if word_tag_freq_matrix[t][tag] > max_inst:
                        max_inst = word_tag_freq_matrix[t][tag]
                        max_tag = tag
                if max_tag == "":
                    max_tag = "NN"  # If for whatever reason out matrix doesn't have the answer NN
                out+=" "+t+"/"+max_tag  # Adding the result to the string
            else:
                out+=" "+t+"/NN"  # If it's not in it altogether, NN
        out+=" ]\n"  # Closing bracket!
    else:  # No brackets? same sort of idea...
        l = l.rstrip()
        if l != "":  # New line at the end of the file caused some problems
            toks = l.split(" ")
            for t in toks:  # same as before, each token, get the max tag if applicable
                if t in word_tag_freq_matrix:
                    max_inst = 0
                    max_tag = ""
                    for tag in word_tag_freq_matrix[t]:
                        if word_tag_freq_matrix[t][tag] > max_inst:
                            max_inst = word_tag_freq_matrix[t][tag]
                            max_tag = tag
                    if max_tag == "":
                        max_tag = "NN"  # all else fails, NN
                    out+=" "+t+"/"+max_tag
                else:
                    out+=" "+t+"/NN"  # NN here too
            out+=" \n"  # next line please!

print(out)  # we're done, and we print

# TEMPORARY FOR EVALUATION COMMENT OUT OTHERWISE
test_out = open("output.txt", "w")
test_out.write(out)
test_out.close()