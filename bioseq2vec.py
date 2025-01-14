from numpy import shape
import numpy as np
from bioseq2vec import Seq2VecR2R
from bioseq2vec.util import DataGenterator
import argparse


def read_fasta_file(fasta_file):
    seq_dict = {}
    fp = open(fasta_file, 'r')
    name = ''
    for line in fp:
        # let's discard the newline at the end (if any)
        line = line.rstrip()
        # distinguish header from sequence
        if line[0] == '>':  # or line.startswith('>')
            # it is the header
            name = line[1:]  # discarding the initial >
            seq_dict[name] = ''
        else:
            # it is sequence
            seq_dict[name] = seq_dict[name] + line.upper()
    fp.close()

    return seq_dict


# def get_words(k, seq):
#     # seq_len = len(seq)
#     words = []
#
#     # tmp_fea = [0] * len(tris)
#     for x in range(len(seq) + 1 - k):
#         kmer = seq[x:x + k]
#         words.append(str(kmer))
#     # tri_feature = [float(val)/seq_len for val in tmp_fea]
#     # pdb.set_trace()
#     return words

def get_words(k, seq):
    seq_len = len(seq)
    words = []

    # tmp_fea = [0] * len(tris)
    # i = 0
    # while len(seq) - i > k:
    #     word = seq[i:i + k]
    #     words.append(str(word))
    #     i = i + k
    for x in range(len(seq) + 1 - k):
        kmer = seq[x:x + k]
        words.append(str(kmer))
    # tri_feature = [float(val)/seq_len for val in tmp_fea]
    # pdb.set_trace()
    return words


def data_convert(filenames):
    results = []
    for filename in filenames:
        result = []
        fr = open(filename, "r")
        seq = []
        for line in fr:
            if line[0] != '>':
                for i in line:
                    if i != '\n':
                        seq.append(i)
            else:
                result.append(list(seq))
                seq = []
        results.append(result)

    return results[0], results[1]


def data_convert_1(filename):
    result = []
    fr = open(filename, "r")
    seq = []
    for line in fr:
        if line[0] != '>':
            for i in line:
                if i != '\n':
                    seq.append(i)
        else:
            result.append(list(seq))

    return result


def pretrain(data, transformer, type):
    print("pretrain starts!")
    # data = np.array(data).tolist()
    transformer.fit(data)
    print("pretrain ends!")
    transformer.save_model("pretrained models/seq2vec_" + str(type) + ".model")  # save model

    return


if __name__ == "__main__":
    # input_file = sys.argv[1]
    transformer = Seq2VecR2R(
        max_index=10,
        max_length=300,
        latent_size=20,
        embedding_size=100,
        encoding_size=200,
        learning_rate=0.05
    )

    file_path = "data\corpus\gencode.v33.pc_translations.fa"
    seq_dict = read_fasta_file(file_path)
    sequences = []
    for seq in seq_dict.values():
        words = get_words(3, seq)  # 3 for protein, 4 for RNA/DNA
        sequences.append(words)
    pretrain(sequences, transformer, "protein_word_200")
