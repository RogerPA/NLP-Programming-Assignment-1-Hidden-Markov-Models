import sys
from collections import defaultdict
import math

def file_iterator(in_file):

    line = in_file.readline()
    while line:
        in_line = line.strip()
        if in_line:
            yield in_line
        else:
            yield None
        line = in_file.readline()

def counts(in_file, counter, ngram_counter, tag_counter, states):
    iterator = file_iterator(in_file)


    for line in iterator:
        in_line = line.strip().split(" ")
        count = float(in_line[0])
        if in_line[1] == "WORDTAG":
            tag = in_line[2]
            word = in_line[3]
            counter[(word, tag)] = count
            states.add(tag)
            tag_counter[tag] += count
        else:
            n = int(in_line[1].replace("-GRAM",""))
            ngram = tuple(in_line[2:])
            ngram_counter[n - 1][ngram] = count


def max_tag(word, counter, ngram_counter, tag_counter, states):
    count = 0
    new_counter = 0
    rare = True

    for tag in states:
        if 0 < counter[(word, tag)]:
            rare = False
            new_counter = counter[(word, tag)] / tag_counter[tag]
        if count < new_counter:
            count = new_counter
            new_tag = tag

    if rare == True:
        return max_tag("_RARE_", counter, ngram_counter, tag_counter, states)

    return new_tag


def write(in_file, out_file, counter, ngram_counter, tag_counter, states):

    iterator = file_iterator(in_file)

    for word in iterator:
        if word:
            out_file.write(word + " " + max_tag(word, counter, ngram_counter, tag_counter, states) + "\n")
        else:
            out_file.write("\n");


file_name_counts = "gene.counts"
file_name_test = "gene.test"
file_name_output = "gene_test.p1.out"

counter = defaultdict(int)
ngram_counter = [defaultdict(int) for i in range(3)]
tag_counter = defaultdict(int)
states = set()

in_file = open(file_name_counts, 'r')

counts(in_file, counter, ngram_counter, tag_counter, states)

in_file.close()

in_file = open(file_name_test, 'r')

out_file = open(file_name_output, 'w')

write(in_file, out_file, counter, ngram_counter, tag_counter, states)

in_file.close()

out_file.close()