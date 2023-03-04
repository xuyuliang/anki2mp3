import configparser
import os
import csv
from nltk.stem.lancaster import LancasterStemmer  

config = configparser.RawConfigParser()
config.read("config.ini",encoding='utf-8')
VOWELS = eval(config['characters']['vowels'])
CONSONANTS = eval(config['characters']['consonants'])
HALF_VOWEL = eval(config['characters']['half_vowel'])
DOUBLE_CONSONANTS =eval(config['characters']['double_consonants'])

def cutbyroot(aword):

    # 基于Lancaster 词干提取算法
    lancaster_stemmer = LancasterStemmer(strip_prefix_flag=True)  
    stem = lancaster_stemmer.stem(aword)
    affixes = aword.split(stem) 
    return stem, affixes 

def isEnglishChar(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
def extract_english_letters(realword,astring):
    contents = astring.split(' ')
    for content in contents:
        firstword = ''
        for c in content:
            if c.isalpha() and isEnglishChar(c) :
                firstword += c
            else:
                firstword +='.'
        # print('firstword:',firstword)
        bigword = firstword.replace('.','')
        if realword in bigword:
            #find tail
            listword = firstword.split('.')
            # 其实没写分隔符号，只是提及了这个单词
            if listword[0] == realword :
                return ''
            # print(listword)
            for i,item in enumerate(listword):
                # if realword.endswith(item) & listword[:i]
                # print('curr:',i,'item:',item,len(item),realword.endswith(item))
                curr_conbind_word = ''.join(listword[:i+1])
                if realword.endswith(item) and len(item)>0 and curr_conbind_word == realword: 
                    # print('got it',i,item,'combindword is:',curr_conbind_word)
                    resultword ,oldc = '',''
                    # print(listword[:i+1])
                    almostresult = '.'.join(listword[:i+1])
                    # print('almostresult:',almostresult)
                    for myc in almostresult: 
                        if oldc =='.' and myc == '.':
                            continue
                        if myc == '.':
                            oldc ='.' 
                        resultword += myc
                        oldc = myc
                    return resultword 
            return ''

def cutbypronuncation(myword):
    if len(myword) <= 5:
        return ' '.join(list(myword))
    list_myword = list(myword)
    list_newword = list_myword.copy()
    vowels_position =[] 
    for i in range(len(list_myword)):
        if list_myword[i] in VOWELS:
            vowels_position.append(i)
        if (list_myword[i] in HALF_VOWEL) and (i>0) and (i< (len(list_myword)-1)):
            vowels_position.append(i)

    # print(vowels_position)
    dict_consonants_group= {}
    for i in range(len(vowels_position)):
        if i+1 < len(vowels_position):
            consonants_group = list_myword[vowels_position[i]+1:vowels_position[i+1]]
            dict_consonants_group.update({vowels_position[i]+1:consonants_group})
        # 单词尾部的辅音就不处理了
        # else:
        #     consonants_group = list_myword[vowels_position[i]+1:]

        # print('cons',consonants_group)
    # print(dict_consonants_group)
    list_newword = list_myword.copy()
    offset = 0
    for k in dict_consonants_group:
        v = dict_consonants_group[k]
        # print (k,v)
        if len(v) == 1:
            list_newword.insert(offset+k,'.')
            offset += 1
        if len(v) == 2:
            if ''.join(v) in DOUBLE_CONSONANTS:
                list_newword.insert(offset+k,'.')
            else:
                list_newword.insert(offset+k+1,'.')
            offset += 1
        if len(v) == 3:
            if v[:2] in DOUBLE_CONSONANTS:
                list_newword.insert(offset+k+2,'.')
            if v[1:] in DOUBLE_CONSONANTS:
                list_newword.insert(offset+k+1,'.')
            else:
                # print('3个辅音，没有双辅音，是不是需要检查一下了')
                list_newword.insert(offset+k,'.')
            offset += 1
    # print(''.join(list_newword))
    # newword = list(newword)
    # newword = ' '.join(newword)
    return ' '.join(list_newword)
    
def main():
    # '''
    # word,text = 'tantrum',' tan晒黑+trum没有p，trump是川普、胜出 的意思。联想：小孩晒黑了发脾气'
    # word,text = 'apocalypse','apo.ca.lyp.se'
    # word,text = 'tantrum','tan.trum'
    # word,text = 'tantrum','tantrum 是什么[`tantrum]'
    # res = extract_english_letters(word,text)
    # print('result:',res)
    # '''

    # file = open('./testwords4cut.txt','r',encoding='utf-8')
    # i=0
    # for line in file:
    #     aword = str.strip(line)
    #     print(aword)
    #     print(cutbypronuncation(aword))
    #     # print(cutbyroot(aword))
    #     if i > 20:
    #         quit()
    #     i+=1
    aword = 'splincipho'
    aword = 'spate'
    print(cutbypronuncation(aword))

if __name__ == "__main__" :
    main()