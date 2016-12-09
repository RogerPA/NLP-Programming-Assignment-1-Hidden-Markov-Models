import sys
from collections import defaultdict
import math

def file_iterator(in_file):

    line = in_file.readline()
    while line:
        in_line = line.strip()
        if in_line:
            fields = in_line.split(" ")
            tag = fields[-1]
            word = " ".join(fields[:-1])
            yield (word, tag)
        else:
            yield (None, None)
        line = in_file.readline()


def word_counter(in_file, counter):
    iterator = file_iterator(in_file)
    for word, tag in iterator:
        if word:
            counter[word] += 1

def replace(in_file, out_file, counter):
    iterator = file_iterator(in_file)
    for word, tag in iterator:
        if word is None:
            out_file.write("\n")
        else:
            if counter[word] < 5:
                out_file.write("_RARE_ " + str(tag) + "\n")
            else:
                out_file.write(word + " " + str( tag) + "\n")

input_file_name = "gene.train"
output_file_name = "gene_rare.train"


counter = defaultdict(int)

in_file = open(input_file_name, "r")

word_counter(in_file, counter)

in_file.close()

in_file = open(input_file_name, "r")

out_file = open(output_file_name, "w")

replace(in_file, out_file, counter)

in_file.close()

out_file.close()
