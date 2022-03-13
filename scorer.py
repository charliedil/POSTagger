import sys
import re

import numpy
from sklearn.metrics import confusion_matrix
# Collect the command line args
test_file_path = sys.argv[1]
test_key_path = sys.argv[2]

test_file = open(test_file_path, "r")
test_key = open(test_key_path, "r")

test_file_text = test_file.read()
test_key_text = test_key.read()
test_file.close()
test_key.close()


pred = []
true = []
labels = []

test_lines = test_file_text.split("\n")
test_key_lines = test_key_text.split("\n")

for l in range(len(test_lines)):
    clean_x = re.sub(r"(^\[\s)|(\s\])", "", test_lines[l])
    clean_y = re.sub(r"(^\[\s)|(\s\])", "", test_key_lines[l])
    x_toks = clean_x.split(" ")
    y_toks = clean_y.split(" ")
    for i in range(len(x_toks)):
        if len(x_toks[i].split("/"))>=2:
            x_tag = x_toks[i].split("/")[1]
            y_tag = y_toks[i].split("/")[1]
            if x_tag not in labels:
                labels.append(x_tag)
            if y_tag not in labels:
                labels.append(y_tag)
        pred.append(x_tag)
        true.append(y_tag)
cf_mat = confusion_matrix(true, pred, labels=labels)

sum_correct = 0
for i in range(len(labels)):
    sum_correct+=cf_mat[i][i]
print(cf_mat)
print("OVERALL ACCURACY:")
print(sum_correct/len(pred))


# numpy.savetxt("conf_mat.txt", cf_mat)
# conf_file = open("conf_mat.txt", "w+")
# conf_file.write(str(cf_mat))
# conf_file.close()