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



def cutbypronuncation2(word):
    consonants =['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
    double_consonants =['br','bl','cl','cr','ck','ch','dr','ds','dw','fl','fr','gh','gr','gl','kn','ng','ph','pl','pr','qu','sc','sl','sh','sp','sn','sm','shr','spl','spr','str','scr','squ','sph','sr','st','sw','tch','thr','thw','th','tr','tw']

    new_word = ""
    count_consonants = 0
    prev_consonant = False
    for i in range(len(word)):
        if word[i] in consonants:
            count_consonants += 1
            if count_consonants >= 2 and not prev_consonant:
                if word[i-1:i+1] not in double_consonants:
                    new_word += "."
            if count_consonants >= 3 and prev_consonant:
                if word[i-2:i+1] not in double_consonants:
                    new_word += "."
                new_word += word[i]
                count_consonants = 1
            else:
                new_word += word[i]
                prev_consonant = True
        else:
            # new_word = "."+new_word
            new_word += word[i]
            count_consonants = 0
            prev_consonant = False
    return new_word

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
            if ''.join(v[:2]) in DOUBLE_CONSONANTS:
                print('前2')
                list_newword.insert(offset+k+2,'.')
            elif ''.join(v[1:]) in DOUBLE_CONSONANTS:
                print('后2')
                list_newword.insert(offset+k+1,'.')
            else:
                # 就当后3辅音 
                list_newword.insert(offset+k,'.')
            offset += 1
        if len(v) == 4:
            if ''.join(v[:2]) in DOUBLE_CONSONANTS:
                print('前2')
                list_newword.insert(offset+k+2,'.')
            elif ''.join(v[1:]) in DOUBLE_CONSONANTS:
                print('后3')
                list_newword.insert(offset+k+1,'.')
            else:
                # 算了,就当前2后2
                list_newword.insert(offset+k+2,'.')
            offset += 1
    # print(''.join(list_newword))
    # newword = list(newword)
    # newword = ' '.join(newword)
    return ' '.join(list_newword)


def cutbyroot(aword):
    if len(aword) < 6 :
        return aword
    did_prefix, did_suffix  = False, False
    aword = do_suffix(aword)
    if '.' in aword:
        did_suffix = True
    aword = do_prefix(aword)
    tempword = aword.split('.')
    if len(tempword) == 3:
        did_prefix = True
    if did_prefix and did_suffix:
        if len(tempword[1]) < 3 :
            all_consonant = True
            for c in tempword[1]:
                if c in VOWELS or c in HALF_VOWEL:
                    all_consonant = False
            if all_consonant:
                if tempword[2][0] in VOWELS:
                    return ''.join(tempword[0])+'.'+''.join(tempword[1:])
                else: 
                    return ''.join(tempword[:2])+'.'+''.join(tempword[2:])
            else:
                if len(tempword[0]) < len(tempword[2]):
                    return ''.join(tempword[:2])+'.'+''.join(tempword[2:])
                else:
                    return ''.join(tempword[0])+'.'+''.join(tempword[1:])
        else:
            if len(tempword[1]) > 5:
                middle = do_suffix(tempword[1])
                if not '.' in middle:
                    if tempword[0][-1] in VOWELS:
                        vowel_end = True
                    if tempword[2][0] in VOWELS:
                        vowel_begin =True
                    middle = cutbypronuncation3(middle,vowel_end,vowel_begin)
                aword = tempword[0]+'.'+middle+'.'+tempword[2]
                return aword
            return aword
    # only two or one part
    else:
        if not '.' in aword:
            aword = cutbypronuncation3(aword)
            return aword
        else :
            first = aword.split('.')[0]
            last = aword.split('.')[1]
            if len(first) > 5:
                if last[0] in VOWELS:
                     vowel_end = True
                first = cutbypronuncation3(first,vowelend=vowel_end)
            if len(last) > 5:
                if first[-1] in VOWELS:
                    vowel_begin = True
                last = cutbypronuncation3(last,vowelbegin=vowel_begin)
            aword = first +'.'+ last
            return aword

def cutbypronuncation3(word,vowelend=False,vowelbegin=False):
    # consonants =['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
    # double_consonants =['br','bl','cl','cr','ck','ch','dr','ds','dw','fl','fr','gh','gr','gl','kn','ng','ph','pl','pr','qu','sc','sl','sh','sp','sn','sm','shr','spl','spr','str','scr','squ','sph','sr','st','sw','tch','thr','thw','th','tr','tw']
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
                continue
            elif is_double_consonant(word, pos):
                new_word = new_word+'.'+ word[pos:pos+2]
                pos += 2
                continue
            elif is_single_consonant(word, pos):
                new_word = new_word+'.'+ word[pos]
                pos += 1
                continue
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
    print('range',len(syllables)-1)
    newsyllables = syllables.copy()
    for i in range(len(syllables)):
        # single consonant found
        print(syllables[i])
        if syllables[i] in allconsonants:
            if i-1 < 0:
                if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                    newsyllables[i] = newsyllables[i]+newsyllables[i+1]        
                    newsyllables.pop(i+1)
                    i-=1
                    continue
                if vowelbegin:
                    merge_head = True
                    continue
            if i+1 > len(syllables)-1:
                if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                    newsyllables[i-1] = newsyllables[i-1]+newsyllables[i]        
                    newsyllables.pop(i)
                    i-=1
                    continue
                if vowelend:
                    merge_tail = True
                    continue
            # 其实不用判断了
            if (i-1 >=0 )  and i+1 < len(syllables):
                if len(syllables[i-1]) < len(syllables[i+1]):
                    if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                        newsyllables[i-1] = newsyllables[i-1]+newsyllables[i]        
                        newsyllables.pop(i)
                        i-=1
                        continue
                    else:
                        if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                            newsyllables[i] = newsyllables[i]+newsyllables[i+1]        
                            newsyllables.pop(i+1)
                            i-=1
                            continue

                else:
                    if syllables[i+1][0] in VOWELS or syllables[i+1][0] in HALF_VOWEL:    
                        newsyllables[i] = newsyllables[i]+newsyllables[i+1]        
                        newsyllables.pop(i+1)
                        continue
                    if syllables[i-1][-1] in VOWELS or syllables[i-1][-1] in HALF_VOWEL:    
                        newsyllables[i-1] = newsyllables[i-1]+newsyllables[i]        
                        newsyllables.pop(i)
                        i-=1
                        continue
    
    res = '.'.join(syllables)
    print('ori rest',res)
    if not merge_tail:
        res = res + '.'
    if not merge_head:
        res = '.' + res
    print(res)
    return res

                
def cutbyroot2(aword):
    vowel_begin,vowel_end = False,False
    merge_head,merge_tail = False,False
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
            if tempword[2][0] in VOWELS:
                vowel_begin =True
            middle= cutbypronuncation3(middle,vowel_end,vowel_begin)
        aword = tempword[0]+middle+tempword[2]
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
                vowel_end = True
            if not did_prefix:
                first = cutbypronuncation3(first,vowelend=vowel_end)

            if first[-1] in VOWELS:
                vowel_begin = True
            if not did_suffix:
                last = cutbypronuncation3(last,vowelbegin=vowel_begin)
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
    #     if i > 1800:
    #         aword = str.strip(line)
    #         print(cutbyroot2(aword))
    #         j-=1
    #         if j < 0:
    #             quit()
    #     i+=1
    aword = 'arachnid'
    # print(do_suffix(aword))
    # aword = 'allopathy'
    # aword = 'emigrate'

    print(cutbyroot2(aword))
    # print(cutbypronuncation3('propcastation'))

if __name__ == "__main__" :
    main()