import string

from pytrie import SortedStringTrie as Trie

# Jaro Winkler Similarity
from pyjarowinkler import distance as jarowinklerSimilarity
import numpy as np

def solution():

    trie = Trie()
    reverseTrie = Trie()
    candidatesList = []
    blendList = []
    blendAnswerList = []

    def inputTrie():
        file = open("data/dict.txt", "r", encoding='utf-8')
        wordList = file.read().splitlines()

        # input prefixly
        for word in wordList:
            word = word.strip()
            word = word.lower()
            trie[word] = word
            reverseWord = word[::-1]
            reverseTrie[reverseWord] = reverseWord

    def inputCandidate():
        file = open("data/candidates.txt", "r", encoding='utf-8')
        wordList = file.read().splitlines()
        for word in wordList:
            word = word.strip()
            word = word.lower()
            candidatesList.append(word)

    def inputBlendAnswerList():
        file = open("data/blends.txt", "r", encoding='utf-8')
        wordList = file.read().splitlines()

        for word in wordList:
            word = word.split()[0]
            word = word.lower()
            blendAnswerList.append(word)

    def splitWord(word):
        length = len(word)
        prefix = word[:int(length/2)]
        reverseSuffix = word[int(length/2) :][::-1]
        splitedCandidate = [prefix, reverseSuffix]
        return splitedCandidate

    def equal(replace, match, char1, char2):
        if char1 == char2:
            return match
        else:
            return replace

    def localEditDistance(word1,word2):
        A = [[]]
        deletion = -1
        insertion = -1
        replace = -1
        match = 1


        word1Length = len(word1)
        word2Length = len(word2)
        A = np.zeros([word1Length, word1Length])
        # construct matrix
        for j in range(word1Length):
            for k in range(word1Length):
                A[j][k] = max(0, A[j][k-1] + deletion, A[j-1][k] + insertion, A[j-1][k-1] + equal(replace, match, word1[k-1],word2[j-1]))

        max_item = max(max(row) for row in A)
        return max_item

    def comparePrefixNDictUsingLED(pref, reverse = 0):
        if reverse:
            trieList = reverseTrie
        else:
            trieList = trie
        prefixDict = trieList.keys(prefix = pref)
        threshold = len(pref) * (0.8)

        prefixFlag = 0
        for word in prefixDict:
            LEDValue = localEditDistance(pref, word)
            if LEDValue >= threshold:
                JWValue = jarowinklerSimilarity.get_jaro_distance(pref, word[:int(len(pref))], winkler = True, scaling = 0.1)
                if JWValue > 0.95:
                    return True
        return False

    def calAccurancy():
        truePositiveAmount = 0

        print(" ***********  blendlist : ")
        print(blendList)
        print("\n\n ")
        print(" *********** count blendlist : ")
        print(len(blendList))
        print("\n\n ")

        for word in blendList:
            if word in blendAnswerList:
                truePositiveAmount += 1

        print(" ***********  truePositive : ")
        print(truePositiveAmount)
        print("\n\n ")

        # precision
        precision = float(truePositiveAmount) / len(blendList)
        recall = float(truePositiveAmount) / (len(blendAnswerList) - 32)

        print("***** Precision is : ")
        print(precision)
        print("\n\n")
        print("***** Recall is : ")
        print(recall)
        print("\n\n")


    # input
    inputTrie()
    inputCandidate()
    inputBlendAnswerList()

    # append filtered candidates to blendList
    for word in candidatesList:
        prefix, reverseSuffix = splitWord(word)
        if comparePrefixNDictUsingLED(prefix, 0) and comparePrefixNDictUsingLED(reverseSuffix, 1):
            blendList.append(word)

    calAccurancy()


    # # test
    # inputBlendAnswerList()
    # print(blendAnswerList)

# run
if __name__ == "__main__":
    solution()