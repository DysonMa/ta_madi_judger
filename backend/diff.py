import os, sys
import filecmp

inputFile = 'input.txt'
outputFile = 'output.txt'
answerFile = 'answer.txt'

if sys.platform == "win32":
    os.system('type input.txt | test.py > output.txt')
    # result = filecmp.cmp(outputFile, answerFile, shallow=False)
    # print('核對結果: ', result)