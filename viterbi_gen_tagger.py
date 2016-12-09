import sys
from collections import defaultdict
import math
import re

def file_iterator(in_file):

    line = in_file.readline()
    while line:
        in_line = line.strip()
        if in_line:
            yield in_line
        else:
            yield None
        line = in_file.readline()


def sentence_iterator(in_lines):

    sentence = []
    for line in in_lines:
        if line == None:
            yield sentence
            sentence = []
        else:
            sentence.append(line)

    if sentence:
        yield sentence

def counts(in_file, counter, ngram_counter, tag_counter, word_counter, states):
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
            word_counter[word] += count
        else:
            n = int(in_line[1].replace("-GRAM",""))
            ngram = tuple(in_line[2:])
            ngram_counter[n - 1][ngram] = count


def rare_word(word, word_counter):

    words_filter = [['_NUMERIC_' , "[0-9]+"], ['_ALL_CAPITALS_' , "^[A-Z]+$"], ['_LAST_CAPITAL_' , "[A-Z]+$"]]

    #words_filter = []


    if 4 < word_counter[word]:
        return word

    for [mark, regex] in words_filter:
        if re.search(regex, word):
            return mark
    return "_RARE_"

def get_q(args, ngram_counter):
    [w, u, v] = list(args)
    return ngram_counter[2][(w, u, v)] / ngram_counter[1][(w, u)]


def get_e(args, counter, tag_counter):
    [word, v] = list(args)
    return counter[(word, v)] / tag_counter[v]

def get_factor(q_args, e_args, counter, ngram_counter, tag_counter):
    q = get_q(q_args, ngram_counter)
    e = get_e(e_args, counter, tag_counter)
    return q * e


def step_coeff(step, sentence, counter, ngram_counter, tag_counter, word_counter, states, table_pi, table_bp):

    word = rare_word(sentence[step - 1], word_counter)

    if 1 == step:
        for v in states:
            table_pi[(step, '*', v)] = get_factor(('*', '*', v), (word, v), counter, ngram_counter, tag_counter)

    elif 2 == step:
        for v in states:
            for u in states:
                table_pi[(step, u, v)] = table_pi[(step - 1, '*', u)] * get_factor(('*', u, v), (word, v), counter, ngram_counter, tag_counter)
    
    else:
        for v in states:
            for u in states:
                arg_max = u
                for w in states:
                    my_pi = table_pi[(step - 1, w, u)] * get_factor((w, u, v), (word, v), counter, ngram_counter, tag_counter)
                    if table_pi[(step, u, v)] < my_pi:
                        table_pi[(step, u, v)] = my_pi
                        table_bp[(step, u, v)] = w




def viterbi(sentence, counter, ngram_counter, tag_counter, word_counter, states):

    table_pi = defaultdict(int)
    table_bp = defaultdict(int)

    n = len(sentence)
    for i in range(n):
        step_coeff(i + 1, sentence, counter, ngram_counter, tag_counter, word_counter, states, table_pi, table_bp)

    if n == 1:
        max_val = 0
        for v in states:
            p = table_pi[(n, '*', v)] * get_q(('*', v, 'STOP'), ngram_counter)

            if max_val < p:
                max_val = p
                arg_max = v

        if max_val == 0:
            arg_max = v
        retun [arg_max]

    else:
        max_val = 0
        for u in states:
            for v in states:
                p = table_pi[(n, u, v)] * get_q((u, v, 'STOP'), ngram_counter)

                if max_val < p:
                    max_val = p
                    tag_sequence = [u, v]

        if max_val == 0:
            tag_sequence = [u, v]

        if n == 2:
            return tag_sequence 

        for k in range(n - 2, 0, -1):
            prev = table_bp[(k + 2, tag_sequence[0], tag_sequence[1])]
            tag_sequence.insert(0, prev)

        return tag_sequence

def write(in_file, out_file, counter, ngram_counter, tag_counter, word_counter, states):

    iterator = sentence_iterator(file_iterator(in_file))

    for sentence in iterator:

        tag_sequence = viterbi(sentence, counter, ngram_counter, tag_counter, word_counter, states)

        for i in range(len(sentence)):
            out_file.write(sentence[i] + " " + str(tag_sequence[i]) + "\n")

        out_file.write("\n")


file_name_counts = "gene.counts"
file_name_test = "gene.test"
file_name_output = "gene_test.p3.out"

counter = defaultdict(int)
ngram_counter = [defaultdict(int) for i in range(3)]
tag_counter = defaultdict(int)
word_counter = defaultdict(int)
states = set()

in_file = open(file_name_counts, 'r')

counts(in_file, counter, ngram_counter, tag_counter, word_counter, states)


in_file.close()

in_file = open(file_name_test, 'r')

out_file = open(file_name_output, 'w')

write(in_file, out_file, counter, ngram_counter, tag_counter, word_counter, states)

in_file.close()

out_file.close()