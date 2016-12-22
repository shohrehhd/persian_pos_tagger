__author__ = 'Shohreh'

import json
import operator
import time
import nltk
import re
class TRAIN:

    def POS_TAGGER_TRAIN(self,fp_name):
        t1 = time.time()
        print("Training Started...")
        #fp = open(file_address,'r',-1,'utf8')
        #fp.read(1)

        TAGS_id = dict()
        WORDS_id=dict()
        TAGS = dict()
        WORDS = dict()
        WORD_TAGS = dict()

        tag_id =0
        word_id=0
        lines=list()
        fp = open(fp_name,'r',encoding='utf8')
        #text = fp.read()
        #lines2 = text.split(sep = '\n')
        i=0

        for word in fp:
            if(word == ""):
                break
            else:

                word = re.sub(r'\s{2,100}',r'\t',word)
                word=word.replace("\n","")
                s = word.split('\t')

                if(len(s) == 2):
                    pair = [s[0],s[1]]
                    lines.append(pair)
                    try:
                        TAGS[s[1]] = TAGS[s[1]]+1
                    except:
                        TAGS[s[1]] = 1
                        TAGS_id[s[1]] = tag_id
                        tag_id = tag_id+1
                    try:
                        WORDS[s[0]] = WORDS[s[0]]+1
                    except:
                        WORDS[s[0]] = 1
                    if(WORDS_id.get(s[0]) == None):
                        WORDS_id[s[0]] = word_id
                        word_id = word_id+1

        WORDS_id["UNKNOWN"] = word_id
        unknown_word_id = word_id
        freq = dict(nltk.FreqDist(WORDS))


        for word in WORDS:
            if(freq[word]==1):
                WORDS_id[word] = unknown_word_id


        Liklihoods = [ [0.0 for i in range(len(WORDS_id))]for j in range(len(TAGS_id))]
        Tag_Transition = [ [0.0 for i in range(len(TAGS_id))]for j in range(len(TAGS_id))]
        TT0 = [0 for i in range(len(TAGS_id))]
        for line_index in range(len(lines)):
            try:
                if lines[line_index][0] in WORDS_id:
                    w = WORDS_id[lines[line_index][0]]
                else:
                    w = unknown_word_id
                Liklihoods[TAGS_id[lines[line_index][1]]][w]+=1/float(TAGS[lines[line_index][1]])
                #if(lines[line_index+1][1]!="DELM"):
                Tag_Transition[TAGS_id[lines[line_index][1]]][TAGS_id[lines[line_index+1][1]]]+=1/float(TAGS[lines[line_index][1]])
                if('.' in lines[line_index][0] or '؟' in lines[line_index][0] or  '#' in lines[line_index]):
                    TT0[TAGS_id[lines[line_index+1][1]]]+=1/float(len(TAGS))
            except:
                do_nothing=0
        fp.close()
        with open('word_id_tab.txt', 'w', encoding='utf8') as json_file:
            json.dump(WORDS_id, json_file, ensure_ascii=False)
        with open('tag_id_tab.txt', 'w', encoding='utf8') as json_file:
            json.dump(TAGS_id, json_file, ensure_ascii=False)
        with open('Tag_Transitions.txt', 'w', encoding='utf8') as json_file:
            json.dump(Tag_Transition, json_file, ensure_ascii=False)
        with open('Liklihoods.txt', 'w', encoding='utf8') as json_file:
            json.dump(Liklihoods,open("Liklihoods.txt","w",encoding='utf8'))
        with open('TT0.txt', 'w', encoding='utf8') as json_file:
            json.dump(TT0,open("TT0.txt","w",encoding='utf8'))

        print ("Training Done in %.2f seconds" % (time.time() - t1))
