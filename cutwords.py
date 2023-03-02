import os
import csv
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
        print('firstword:',firstword)
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
                    print(listword[:i+1])
                    almostresult = '.'.join(listword[:i+1])
                    print('almostresult:',almostresult)
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
        return myword
    
    
def main():
    '''
    word,text = 'tantrum',' tan晒黑+trum没有p，trump是川普、胜出 的意思。联想：小孩晒黑了发脾气'
    # word,text = 'apocalypse','apo.ca.lyp.se'
    # word,text = 'tantrum','tan.trum'
    res = extract_english_letters(word,text)
    print('result:',res)
    '''
    file = open('./testwords4cut.txt','r',encoding='utf-8')
    for line in file:
        aword = str.strip(line)
        print(aword)
        print(cutbypronuncation(aword))

if __name__ == "__main__" :
    main()