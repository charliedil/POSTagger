"""
Charlie Dil 03/12/2022

POSTagger code
1. Problem statement
The problem we are trying to solve is POS-tagging utilizing a baseline model of assigning the most common tag for
a word to that word (if it is a new word, we will label it NN). We want to see how much further we can boost the
model with the addition of 5 rules.

2. Usage
This code is written in Python 3.10, so please make sure that you run it with that interpreter.
You can run with:

python tagger.py training_data.txt testing_data.txt

Tags will be output to the command line. Here is an example:
Input from file:
No ,
[ it ]
[ was n't Black Monday ]
.

Output to terminal:
No/DT ,/,
[ it/PRP ]
[ was/VBD n't/RB Black/NNP Monday/NNP ]
./.

3. Algorithm
Baseline:
The baseline algorithm works by parsing the training data and creating a word_tag_freq_matrix which keeps track of the
number of times a specific word is tagged with a specific tag. For inference, it will parse the testing data in a simil-
ar fashion and for each word, check to see if it is in thhe word_tag_freq_matrix. If it is, it finds the most frequent
tag and tags that word with that. If the word is not in the matrix, it is tagged as NN. The results are in the form
word/tag and are appended to an "out" string that is printed at the very end.

With this baseline my accuracy was:
0.8581906752100085

First rule added:
Plural noun rule: If a word is about to be tagged NN but it ends with an "s", tag it instead as NNS.
Same with PNN and PNNS.

Accuracy:
0.8666602084169446 (prev: .8582)

Second rule added:
Capitalization rule. If something is labeled as NN or NNS, they are labeled NNP or NNPS if the first letter in
the word is capitalized.

Accuracy:
0.8911415878990853 (prev: 0.8667)

Third rule added:
Proper Noun Phrase Rule. If we are in a phrase and the previous token was tagged a proper noun and this token
starts with capital letter, it should be tagged the same way as its previous tag

Accuracy:
0.8911554270056325 (prev: 0.8911 - very small increase)

Fourth rule added:
Number rule. If it passes the isdigit() function call (checks to see if it is only numeric) it should be labeled
CD.

Accuracy:
0.8926777287258335 (prev: 0.8912)

Fifth rule added
The rule. That's it, that's what it's called. Assumes that the word following a DT word (such as "The", hence
the very good name) will be some kind of noun. Didn't expect it to be great since adjectives and adverbs exist,
but it makes for a very good name, so here it is.

Accuracy:
0.8834747228718914 (prev: 0.8927)


Final accuracy:
0.8834747228718914

Introducing The Rule was not super helpful, but it's the best joke I've made all year, so it's not leaving.
The best rule appears to have been the Capitalization Rule. That makes sense. People don't usually capitalize words
that aren't proper nouns unless they want to seem important.

"""


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
line_count = len(test_lines)  # There is the most annoying blank line at the end of the file. This is for that.

i = 0  # we will use this in tandem with line_count
for l in test_lines:
    i+=1  # matches the line number (counting from 1, I know, horrible)

    brackets = re.search(r"(^\[\s)|(\s\])", l)  # Brackets?
    if brackets:  # I want to be sure to print out the brackets when required to.
        clean_l = re.sub(r"(^\[\s)|(\s\])", "", l)  # Buuuuut for parsing they're annoying, so bye!
        toks = clean_l.split(" ")
        out += "[ "  # Since this line had brackets, it will have brackets on output
        first = True
        prev = ""  # store previous tag, some context helps
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
                if first:  # First tok in line has different printing rules, needs to be isolated
                    if max_tag not in ["NN", "NNS", "NNP", "NNPS"] and prev=="DT":  # My glorious rules in action
                        max_tag = "NN"
                    if max_tag == "NN" and t.endswith("s"):  # Plural?
                        max_tag = "NNS"
                    if (max_tag == "NN") and t[0].isupper():  # Proper noun?
                        max_tag = "NNP"
                    if (max_tag == "NNS") and t[0].isupper():  # Plural AND proper???
                        max_tag = "NNPS"
                    if max_tag != "CD" and t.isdigit():  # Number.
                        max_tag = "CD"
                    if max_tag not in ["NNP", "NNPS"] and prev in ["NNP", "NNPS"] and t[0].isupper():  # proper noun rule
                        max_tag = prev

                    out+=t+"/"+max_tag  # Adding the result to the string
                    prev = max_tag
                    first = False
                else:  # If it's not the first token, it gets printed a little differently
                    if max_tag not in ["NN", "NNS", "NNP", "NNPS"] and prev=="DT":  # The rules again, just in another branch
                        max_tag = "NN"
                    if max_tag == "NN" and t.endswith("s"):
                        max_tag = "NNS"
                    if (max_tag == "NN") and t[0].isupper():
                        max_tag = "NNP"
                    if (max_tag == "NNS") and t[0].isupper():
                        max_tag = "NNPS"
                    if max_tag != "CD" and t.isdigit():
                        max_tag = "CD"
                    if max_tag not in ["NNP", "NNPS"] and prev in ["NNP", "NNPS"] and t[0].isupper():
                        max_tag = prev
                    out += " " + t + "/" + max_tag  # Adding the result to the string
                    prev = max_tag
            elif t=='':
                out+=" "
            else:
                if first:  # first token in line?
                    if t.endswith("s") and t[0].isupper(): #  the rules again in yet another branch
                        out+=t+"/NNPS"                      # I'm sure there's a better way to do this but this is my
                        prev = "NNPS"                         # way I guess
                    elif t[0].isupper():
                        out += t + "/NNP"
                        prev = "NNP"
                    elif t.endswith("s"):
                        out += t + "/NNS"
                        prev = "NNS"
                    elif t.isdigit():
                        out += t + "/CD"
                        prev = "CD"
                    else:
                        out+=t+"/NN"  # If it's not in it altogether, NN
                        prev = "NN"
                    first = False
                else:
                    if t.endswith("s") and t[0].isupper():  # the rules... again
                        out += " " + t + "/NNPS"  # If it's not in it altogether, NN
                        prev = "NNPS"
                    elif t[0].isupper():
                        out += " " + t + "/NNP"
                        prev = "NNP"
                    elif t.endswith("s"):
                        out += " " + t + "/NNS"
                        prev = "NNS"
                    elif t.isdigit():
                        out += " " + t + "/CD"
                        prev = "CD"
                    else:
                        out += " " + t + "/NN"
                        prev = "NN"
        out+=" ]\n"  # Closing bracket!

    else:  # No brackets? same sort of idea...
        left_space = (l != l.lstrip())
        l = l.strip()
        if l != "":  # New line at the end of the file caused some problems
            toks = l.split(" ")
            first = True
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
                    if first:
                        if left_space:
                            out += " "
                            left_space = False
                        if max_tag == "NN" and t.endswith("s"):  # The rules... this is like 4 times now huh
                            max_tag = "NNS"
                        if (max_tag == "NN") and t[0].isupper():
                            max_tag = "NNP"
                        if (max_tag == "NNS") and t[0].isupper():
                            max_tag = "NNPS"
                        if max_tag!="CD" and t.isdigit():
                            max_tag = "CD"
                        out+=t+"/"+max_tag
                        first = False
                    else:  # not first
                        if max_tag == "NN" and t.endswith("s"):  #  the rules... part 5
                            max_tag = "NNS"
                        if (max_tag == "NN") and t[0].isupper():
                            max_tag = "NNP"
                        if (max_tag == "NNS") and t[0].isupper():
                            max_tag = "NNPS"
                        if max_tag == "CD" and t.isdigit():
                            max_tag = "CD"
                        out += " " + t + "/" + max_tag
                elif t=='':  # for the RANDOM EMPTY SPACES in the document
                    out+=" "
                else:  # not in matrix?
                    if first:
                        if left_space:
                            out += " "
                            left_space = False
                        if t.endswith("s") and t[0].isupper():  # Oh my god, not the rules again
                            out += t + "/NNPS"
                        elif t[0].isupper():
                            out+=t+"/NNP"
                        elif t.endswith("s"):
                            out += t + "/NNS"
                        elif t.isdigit():
                            out += t + "/CD"
                        else:
                            out+=t+"/NN"  # NN here too
                        first = False
                    else:
                        if t.endswith("s") and t[0].isupper():  # This is getting out of hand
                            out += " " + t + "/NNPS"
                        elif t[0].isupper():
                            out += " " + t + "/NNP"
                        elif t.endswith("s"):
                            out += " " + t + "/NNS"
                        elif t.isdigit():
                            out += " " + t + "/CD"
                        else:
                            out += " " + t + "/NN"  # NN here too

            out += " \n"  # next line please!


        else:
            if i != line_count:
                out += "\n"

print(out)  # PHEW, we're done, and we print

# TEMPORARY FOR EVALUATION COMMENT OUT OTHERWISE
# test_out = open("output.txt", "w")
# test_out.write(out)
# test_out.close()