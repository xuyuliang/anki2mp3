import configparser
import os
import csv
# from nltk.stem.lancaster import LancasterStemmer  

config = configparser.RawConfigParser()
config.read("config.ini",encoding='utf-8')
VOWELS = eval(config['characters']['vowels'])
CONSONANTS = eval(config['characters']['consonants'])
HALF_VOWEL = eval(config['characters']['half_vowel'])
DOUBLE_CONSONANTS =eval(config['characters']['double_consonants'])
PREFIXES = [] 
SUFFIXES = [] 

def get_affix_from_file():
    global PREFIXES
    PREFIXES = []
    global SUFFIXES
    SUFFIXES = []
    file = open('prefix.txt','r',encoding='utf-8')
    for line in file:
        word = str.strip(line)
        PREFIXES.append(word)
    file.close
    file = open('suffix.txt','r',encoding='utf-8')
    for line in file:
        word = str.strip(line)
        SUFFIXES.append(word)
    file.close

get_affix_from_file()


def cut_prefix_after(aword:str,n:int):
    return aword[0:n]+'.'+aword[n:]

def pre_process_prefix(aword):
    # deal with axx 
    if aword[0:1] == 'a' and aword[1] == aword[2] and aword[1] in CONSONANTS and aword[2] in CONSONANTS :
        return cut_prefix_after(aword,2)
    # deal with coxx  co
    if aword[0:2] == 'co' and aword[2] == aword[3] and aword[2] in CONSONANTS and aword[3] in CONSONANTS :
        return cut_prefix_after(aword,3) 
    if aword[0:2] == 'co' and ( aword[2] == 'h' or aword[2:4] =='gn' ):
        return cut_prefix_after(aword,2)
    # deal with bin
    if aword[0:3] == 'bin' and aword[3] in VOWELS:
        return cut_prefix_after(aword,3)
    # diff
    if aword[0:3] == 'dif' and aword[3] == 'f': 
        return cut_prefix_after(aword,3)
    # eff e en em 
    if aword[:2] == 'en' or aword[0:2] == 'em':
        return cut_prefix_after(aword,2)
    if aword[:3] == 'eff':  
        return cut_prefix_after(aword,2)
    if aword[0] == 'e' and  aword[1] in ['b', 'd', 'g', 'j' 'l' 'm' 'n' 'r' 'v']:
        return cut_prefix_after(aword,1)
    # ixx
    if aword[0:1] == 'i' and aword[1] == aword[2] and aword[1] in CONSONANTS and aword[2] in CONSONANTS :
        return cut_prefix_after(aword,2) 
    # occ off opp
    if aword[:3] == 'occ' or aword[:3] == 'opp' or aword[:3] == 'off':  
        return cut_prefix_after(aword,2)
    # red re
    if aword[:3] == 'red' and aword[3] in VOWELS:
        return cut_prefix_after(aword,3)
    # se sed 
    if aword[:3] == 'red' and aword[3] in VOWELS:
        return cut_prefix_after(aword,3)
    # sys
    if aword[:2] == 'sy' and aword[3] == 's' :
        return cut_prefix_after(aword,2)
    # not match
    return 'not match'

def do_prefix(aword):
    reslt = pre_process_prefix(aword) 
    if reslt != 'not match':
        return reslt
    else:
        for prefix in PREFIXES:
            lenth = len(prefix)
            if aword[0:lenth] == prefix:
                return cut_prefix_after(aword,lenth)
        return aword

def do_suffix(aword):
    #cut a piece from the end of aword,
    #match the largest in SUFFIXES 
    res = []
    for suffix in SUFFIXES:
        lenth = len(aword)-len(suffix)
        if aword[lenth:] == suffix:
            res.append(suffix)
    maxlen = 0
    selected = ''
    for item in res:
        if len(item) > maxlen:
            maxlen = len(item)
            selected = item
    if selected != '':
        return cut_prefix_after(aword,len(aword)-maxlen)
    else:
        return aword

def isEnglishChar(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# extract user's manual cut from Anki
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
                    return ' '.join(list(resultword))
            return ''
        else:
            return ''





def cutbypronuncation3(word,vowelend=False,len1=0,vowelbegin=False,len2=0):
    consonants = CONSONANTS
    double_consonants = DOUBLE_CONSONANTS

    def is_single_consonant(word, pos):
        return (word[pos] in consonants)

    def is_double_consonant(word, pos):
        return (pos < len(word) - 1 and word[pos:pos+2] in double_consonants)

    def is_triple_consonant(word, pos):
        return (pos < len(word) - 2 and word[pos:pos+3] in double_consonants)

    def add_dots(word):
        new_word = ""
        pos = 0
        while pos < len(word):
            if is_triple_consonant(word, pos):
                new_word = new_word+'.'+ word[pos:pos+3]
                pos += 3
            elif is_double_consonant(word, pos):
                new_word = new_word+'.'+ word[pos:pos+2]
                pos += 2
            elif is_single_consonant(word, pos):
                new_word = new_word+'.'+ word[pos]
                pos += 1
            else:
                new_word += word[pos]
                pos += 1
            # if pos < len(word) and not is_double_consonant(word, pos) and not is_triple_consonant(word, pos):
            #     new_word += "."
        return new_word
    res = add_dots(word)
    if (res[0] == '.'):
        res = res[1:]
    # merge syllable
    syllables = res.split('.')
    allconsonants = CONSONANTS.copy()
    allconsonants.extend(DOUBLE_CONSONANTS)
    merge_head, merge_tail = False, False
    print('curr word is:',syllables)
    n = len(syllables)
    i = 0
    while i < len(syllables):
        # print(syllables[i])
        # pure consonant group found
        if syllables[i] in allconsonants:
            # first element 
            if i-1 < 0:
                # if sylables[i+1] exists
                if len(syllables) > 1:
                    if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                        syllables[i] = syllables[i]+syllables[i+1]        
                        syllables.pop(i+1)
                        i-=1

                if vowelend:
                    if len(syllables[i]) + len1 < 6:
                        merge_head = True
            # last element
            if i+1 > len(syllables)-1 and len(syllables) > 1:
                if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                    syllables[i-1] = syllables[i-1]+syllables[i]        
                    syllables.pop(i)
                    i-=1
                if vowelbegin:
                    if len(syllables[i]) + len2 < 6:
                        merge_tail = True
            # middle element 
            if (i-1 >=0 )  and i+1 < len(syllables):
                if len(syllables[i-1]) < len(syllables[i+1]):
                    if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                        syllables[i-1] = syllables[i-1]+syllables[i]        
                        syllables.pop(i)
                        i-=1
                    else:
                        if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                            syllables[i] = syllables[i]+syllables[i+1]        
                            syllables.pop(i+1)
                            i-=1

                else:
                    if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                        syllables[i] = syllables[i]+syllables[i+1]        
                        syllables.pop(i+1)
                        i-=1
                    if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                        syllables[i-1] = syllables[i-1]+syllables[i]        
                        syllables.pop(i)
                        i-=1
        i+=1
    
    #  merge some small syllables 
    templength = 0
    i = 0
    counter = 0
    while i < len(syllables):
        curr_index = len(syllables)-i-1
        counter += 1
        if curr_index -1  >= 0:
            templength = len(syllables[curr_index]) + len(syllables[curr_index-1])
            if  templength <= 5:
                syllables[curr_index] = syllables[curr_index-1] + syllables[curr_index] 
                syllables.pop(curr_index-1)
                i-=1
                counter =0
                templength = 0
        i+=1

    res = '.'.join(syllables)
    if not merge_tail:
        res = res + '.'
    if not merge_head:
        res = '.' + res
    return res

                
def cutbyroot2(aword):
    print(aword)
    vowel_begin,vowel_end = False,False
    merge_head,merge_tail = False,False
    len1,len2 = 0,0
    if len(aword) < 6 :
        return aword
    did_prefix, did_suffix  = False, False
    aword = do_suffix(aword)
    if '.' in aword:
        did_suffix = True
    aword = do_prefix(aword)
    tempword = aword.split('.')
    if did_suffix and len(tempword) == 3:
        did_prefix = True
    if not did_suffix and len(tempword) == 2:
        did_prefix = True
    if did_prefix and did_suffix:
        middle = do_suffix(tempword[1])
        if not '.' in middle:
            if tempword[0][-1] in VOWELS:
                vowel_end = True
                len1 = len(tempword[0])
            if tempword[2][0] in VOWELS:
                vowel_begin =True
                len2 = len(tempword[2])
            middle= cutbypronuncation3(middle,vowel_end,len1,vowel_begin,len2)
            aword = tempword[0]+middle+tempword[2]
        else:
            middle0=middle.split('.')[0]
            middle1=middle.split('.')[1]

            if tempword[0][-1] in VOWELS:
                vowel_end = True
                len1 = len(tempword[0])
            if middle1[0] in VOWELS:
                vowel_begin =True
                len2 = len(middle1)
            middle0= cutbypronuncation3(middle0,vowel_end,len1,vowel_begin,len2)

            if middle0[-1] in VOWELS:
                vowel_end = True
                len1 = len(middle0)
            if tempword[2][0] in VOWELS:
                vowel_begin =True
                len2 = len(tempword[2])
            middle1= cutbypronuncation3(middle1,vowel_end,len1,vowel_begin,len2)

            aword = tempword[0]+middle0+middle1+'.'+tempword[2]

        return aword
    # only two or one part
    else:
        if not '.' in aword:
            aword = cutbypronuncation3(aword)
            return aword
        else :
            first = aword.split('.')[0]
            last = aword.split('.')[1]
            if last[0] in VOWELS:
                vowel_begin= True
                len2 = len(last)
            if not did_prefix:
                first = cutbypronuncation3(first,vowelbegin=vowel_begin,len2=len2)

            if first[-1] in VOWELS:
                vowel_end= True
                len1 = len(first)
            if not did_suffix:
                last = cutbypronuncation3(last,vowelend=vowel_end,len1=len1)
            aword = first + last
            return aword


    
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
    # aword = 'corpuscle'
    # print(cutbypronuncation(aword))


    # aword = 'eucalyptus'
    # print(do_suffix(aword)) 
    # print(do_prefix(aword))
    # print(do_prefix(do_suffix(aword)))

    # file = open('./testwords4cut.txt','r',encoding='utf-8')
    # i=0
    # j=20
    # for line in file:
    #     # if i > 1800:
    #     if i > 1080:
    #         aword = str.strip(line)
    #         print(cutbyroot2(aword))
    #         j-=1
    #         if j < 0:
    #             quit()
    #     i+=1
    # aword = 'arachnid'
    # print(do_suffix(aword))
    aword = []
    # aword.append('allopathy')
    # aword.append('emigrate')
    # aword.append('calcium')
    # aword.append('caldron')
    # aword.append('concession')
    # aword.append('ramification')
    # aword.append('inadvertently')
    # aword.append('parenthesis')
    # aword.append('psychosis')
    aword.append('requite')
    for word in aword:
        print(cutbyroot2(word))

    # print(cutbypronuncation3('propcastation'))

if __name__ == "__main__" :
    main()