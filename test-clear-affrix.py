import os

def read_sort_write():
    file = open('./后缀.txt','r',encoding='utf-8')
    listword = []
    for line in file:
        word = str.strip(line)
        if word is None:
            continue
        if len(word) < 1:
            continue
        if word[0] == '-':
            word = word[1:]
        print(word)
        listword.append(word)
    listword.sort()
    print(len(listword))

    newfile = open('./aasuffix.txt','w',encoding='utf-8')
    for word in  listword:
        newfile.write(word+'\n')

def reversed_sort():
    file = open('./aasuffix.txt','r',encoding='utf-8')
    mydict = {} 
    r_list = []
    s_list = []
    for word in file:
        word = str.strip(word)
        temp = list(word)
        temp.reverse()
        r_word = ''.join(temp)
        print(r_word)
        mydict.update({r_word:word})
        r_list.append(r_word)
    r_list.sort()

    file = open('./suffix.txt','w',encoding='utf-8')
    for word in r_list:
        s_list.append(mydict[word])
        file.write(mydict[word]+'\n')
    print(s_list)




if __name__ == "__main__":

    # read_sort_write()
    reversed_sort()