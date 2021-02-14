from graphs_algorithms import Vertex
from graphs_algorithms import Graph

'''
Word Ladder Puzzle:
Transform word "FOOL" into word "SAGE". You can change one letter at a time transforming one word into another.
FOOL
POOL
POLL
POLE
PALE
SALE
SAGE

We can turn a large collection of words into a graph, with an edge from one word to another if they differ by a letter.
Any Path in the graph from one word to another is a solution.

Approach: Put words that differ on the same letter position in a bucket (dictionary).
The labels on the word buckets with an underscore, as letter position reference, are the keys in the dictionary.
The value stored for that key is a list of words.
'''


def buildGraph(wordFile):
    d = {}
    g = Graph()

    wfile = open(wordFile, 'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        print(line)
        word = line[:-1]
        print(word)
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i + 1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1, word2)
    return g
