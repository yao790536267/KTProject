import string

from pyjarowinkler import distance as jarowinklerSimilarity
import numpy as np
from pytrie import SortedStringTrie as Trie

def solution():

    candidatesTokens = []
    blendResults = []
    blendWords = []
    prefixTrie = Trie()
    reversalTrie = Trie()

    def equalLetter(replace, match, char1, char2):
        if char1 == char2:
            return match
        else:
            return replace

    def split(word):
        leng = len(word)
        prefix = word[:int(leng / 2) + 1]
        suffix = word[int(leng / 2 - 1):][::-1]
        splited = [prefix, suffix]
        return splited

    def calPreRe():
        truePositiveAmount = 0

        blendCorrectWords = []
        blendFalseWords = []

        for word in blendWords:
            if word in blendResults:
                truePositiveAmount += 1
                blendCorrectWords.append(word)

        print("  truePositive : ")
        print(truePositiveAmount)
        print("\n\n ")

        # precision
        recall = float(truePositiveAmount) / (len(blendResults) - 32)
        precision = float(truePositiveAmount) / len(blendWords)

        print(" Recall is : ")
        print(recall)
        print("\n\n")
        print(" Precision is : ")
        print(precision)
        print("\n\n")

        for word in blendResults:
            if word not in blendWords:
                blendFalseWords.append(word)

        print("count of  blendCorrectWords : " + len(blendCorrectWords))

        print("   blendCorrectWords : " + blendCorrectWords)

        print("  count of  blendFalseWords : " + len(blendFalseWords))

        print(" blendFalseWords : " + blendFalseWords)

    def input():
        file = open("data/dict.txt", "r", encoding='utf-8')
        wordList = file.read().splitlines()

        repeatLetters = ['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff', 'gggg', 'hhhh', 'iiii', 'jjjj', 'kkkk', 'llll',
                         'mmmm', 'nnnn', 'oooo', 'pppp', 'qqqq', 'rrrr', 'ssss', 'tttt', 'uuuu', 'vvvv', 'wwww', 'xxxx',
                         'yyy', 'zzzz']

        # input prefixly
        for word in wordList:
            word = word.strip()
            word = word.lower()
            prefixTrie[word] = word
            reverseWord = word[::-1]
            reversalTrie[reverseWord] = reverseWord

        file1 = open("data/candidates.txt", "r", encoding='utf-8')
        wordList1 = file1.read().splitlines()
        for word in wordList1:
            word = word.strip()
            word = word.lower()
            flag = 0
            for subString in repeatLetters:
                if subString in word:
                    flag = 1
                    break
            if flag == 0:
                candidatesTokens.append(word)

        file2 = open("data/blends.txt", "r", encoding='utf-8')
        wordList2 = file2.read().splitlines()

        for word in wordList2:
            word = word.split()[0]
            word = word.lower()
            blendResults.append(word)

    def editDistance(word1,word2):
        A = [[]]
        replace = -1
        match = 1
        deletion = -1
        insertion = -1


        word1Length = len(word1)
        word2Length = len(word2)
        A = np.zeros([word1Length, word1Length])
        # construct matrix
        for j in range(word1Length):
            for k in range(word1Length):
                A[j][k] = max(0, A[j][k-1] + deletion, A[j-1][k] + insertion, A[j-1][k-1] + equalLetter(replace, match, word1[k-1],word2[j-1]))

        max_item = max(max(row) for row in A)
        return max_item

    def compareUsingLED(pref, reverse = 0):
        if reverse:
            trieList = reversalTrie
        else:
            trieList = prefixTrie
        prefixDict = trieList.keys(prefix = pref)
        threshold = len(pref) * (0.85)

        prefixFlag = 0
        for word in prefixDict:
            LEDValue = editDistance(pref, word)
            if LEDValue >= threshold:
                JWValue = jarowinklerSimilarity.get_jaro_distance(pref, word[:int(len(pref))], winkler = True, scaling = 0.1)
                if JWValue > 0.8:
                    return True
        return False



    # input
    input()


    for word in candidatesTokens:
        prefix, reverseSuffix = split(word)
        if compareUsingLED(prefix, 0) and compareUsingLED(reverseSuffix, 1):
            blendWords.append(word)

    calPreRe()


# run
if __name__ == "__main__":
    solution()