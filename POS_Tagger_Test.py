__author__ = 'Shohreh'

import re
import time

def get_ASCII(s):
    ascii = ""
    for i in s:
        ascii+=chr(i)
        ascii+"-"
    return ascii

def get_unicode(s):
    uni = ""
    for i in s:
         uni += word(i).decode('utf-8')
         uni +="-"
    return uni

    '''TAGS_ID ={'VB':0,'TO':1,'NN':2,'PPSS':3}
    TT0=[0.019,.0043,.041,0.067]
    TT = [[.0038,.035,.047,.0070],
          [0.83,0,0.00047,0],
          [.004,.016,.087,.0045],
          [0.23,.00079,.0012,.00014]]
    WORDS_ID={'I':0,'want':1,'to':2,'race':3}

    Liklihoods =[[0,.0093,0,.00012],
                 [0,0,.99,0],
                 [0,.000054,0,0.00057],
                 [0.37,0,0,0]]
    '''
def word_by_id(word_dict,id):
    keys = list(word_dict.keys()) #in python 3, you'll need `list(i.keys())`
    values = list(word_dict.values())
    try:
        return keys[values.index(id)]
    except:
        return -1
class TEST:


    def POS_TAGGER_TEST(self,input_sequence,WORDS_ID,TAGS_ID,Liklihoods,TT,TT0):



        #input_string = input_string.replace('\u06CC','\u064A')
        #input_string = input_string.replace('\u06A9','\u0643')
        t2 =time.time()


        PStart = 1
        viterbi = [[0 for i in range(len(TAGS_ID))]for j in range(len(input_sequence)+2)]
        back_pointer= [[0 for i in range(len(TAGS_ID))]for j in range(len(input_sequence)+2)]

    #tag_id_delm = TAGS_ID['s']#todo: fix this when I computed start

        initial = True;
        word_index = 0

        for word in input_sequence:
            try:
                word_id = WORDS_ID[word]
            except:
                word_id = WORDS_ID["UNKNOWN"]
            for tag in TAGS_ID:
                try:
                    tag_id = TAGS_ID[tag]
                    if(initial): # initialization step
                        viterbi[word_index][tag_id] = Liklihoods[tag_id][word_id]*TT0[tag_id]
                        back_pointer[word_index][tag_id]= -1
                    else: #recursion step
                        v_temp = [0 for i in range(len(TAGS_ID))]
                        for prev_tag in TAGS_ID:
                            prev_tag_id = TAGS_ID[prev_tag]
                            #print("P("+tag+"|"+prev_tag+")=",TT[prev_tag_id][tag_id])
                            v_temp[prev_tag_id]=(viterbi[word_index-1][prev_tag_id]*TT[prev_tag_id][tag_id])
                            #print ("v_temp["+word_by_id(TAGS_ID,prev_tag_id)+"]=",v_temp[prev_tag_id])

                        #print ("v("+word_by_id(WORDS_ID,word_id)+","+word_by_id(TAGS_ID,tag_id)+") =max", v_temp)
                        max_val = max(v_temp)
                        argmax = v_temp.index(max_val)
                        viterbi[word_index][tag_id] = max_val*Liklihoods[tag_id][word_id]
                        #print("v("+word_by_id(WORDS_ID,word_id)+","+word_by_id(TAGS_ID,tag_id)+") =", viterbi[word_index][tag_id])
                        back_pointer[word_index][tag_id] = argmax

                except:
                    print("what's wrong here?",word_id,tag_id)

            initial = False
            word_index+=1

        v_temp = viterbi[len(input_sequence)-1]
        max_val = max(v_temp)
        argmax = v_temp.index(max_val)
        argmax_last = argmax

        back_pointer[word_index][0:len(TAGS_ID)]=(argmax_last for i in range(len(TAGS_ID)))
        back = len(back_pointer)-1
        guessed_tags=[]

        while(back >= 0):
            guessed_tags.append(word_by_id(TAGS_ID,back_pointer[back][argmax_last]))
            argmax_last = back_pointer[back][argmax_last]
            back = back-1

        guessed_tags = (guessed_tags[1:(len(guessed_tags)-1)])
        #print("Viterbi algorithm took %.2f" % (time.time() - t2))
        output = ""
        output_dic=dict()
        i =0
        back = len(guessed_tags)-1
        for word in input_sequence:
           output+=(word)
           output+=("/"+guessed_tags[back])
           output_dic[i]=guessed_tags[back]
           back=back-1
           i+=1

        #print(output)
        return output_dic

