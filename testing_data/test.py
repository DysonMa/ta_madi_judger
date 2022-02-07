import math
import operator


def dot_product2(v1, v2):
    return sum(map(operator.mul, v1, v2))


def cosineSimilarity(v1, v2):
    # v1請放入doc，v2請放入query
    prod = dot_product2(v1, v2)
    len1 = math.sqrt(dot_product2(v1, v1))
    len2 = math.sqrt(dot_product2(v2, v2))
    return prod / (len1 * len2)


# 主程式開始
wordSet = set()
docs = []
docs_words = []
docs_cosineSimilarity = []
maxCosineSimilarity = 0
bestDoc = ''

inputCount = int(input())
# 輸入Doc
for i in range(inputCount):
    inputDoc = input()
    docs.append(inputDoc)
    docs_words.append([])
    inputDocWords = (inputDoc.lower()).split(' ')
    for j in range(len(inputDocWords)):
        wordSet.add(inputDocWords[j])
        docs_words[i].append(inputDocWords[j])

# 輸入Query
inputQuery = input()
inputQueryWords = (inputQuery.lower()).split(' ')

# 轉換為dictionary
# wordDict = dict(wordSet)
wordList = list(wordSet)
wordDict = {}
for i in range(len(wordList)):
    wordDict[wordList[i]] = 0

# 整理query vector
queryVectorDict = wordDict.copy()
for i in range(len(inputQueryWords)):
    try:
        queryVectorDict[inputQueryWords[i]] += 1
    except:
        continue

queryVector = list(queryVectorDict.values())

# 整理doc vector
for i in range(len(docs)):
    docVectorDict = wordDict.copy()
    for j in range(len(docs_words[i])):
        try:
            docVectorDict[docs_words[i][j]] += 1
        except:
            continue
    docVector = list(docVectorDict.values())
    # 計算cosineSimilarity
    thisCosineSimilarity = round(cosineSimilarity(docVector, queryVector), 4)
    docs_cosineSimilarity.append(thisCosineSimilarity)
    if thisCosineSimilarity > maxCosineSimilarity:
        maxCosineSimilarity = thisCosineSimilarity
        bestDoc = 'doc{0}'.format(i+1)

# 印出doc
for i in range(len(docs)):
    print('doc{0} {1}'.format(i+1, docs_cosineSimilarity[i]))

# 印出best
if bestDoc != '':
    print('best:{0}'.format(bestDoc))
