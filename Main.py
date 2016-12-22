
from POS_Tagger_Test import TEST
from POS_Tagger_Train import TRAIN
import re
import json
import gc
def compare_dicts(a,b):
    true = 0
    false =0
    number =0
    try:
        for item in a.keys():
            if(item==''):
                number=number+1
                continue
            if(a[item]==b[item]):
                true=true+1
            else:
                false = false+1
    except:
        false = false+1
    return float(true/((max(len(a),len(b)))-number))


file_address = "input.txt"

try:
    entered = int(input("Press 1 to start training \nPress 2 to test an input string with already trained data.\nPress 3 to run a 10-fold cross validation on data(This may take a long time)\n Press 4 to save batch file input"))
except:
    print("wrong command.")
try:
    if(entered == 1 ):

        train=TRAIN()
        train.POS_TAGGER_TRAIN(file_address)
    elif(entered==2):
        WORDS_ID = json.load(open("word_id_tab.txt",'r',encoding='utf8'))
        TAGS_ID = json.load(open("tag_id_tab.txt",'r',encoding='utf8'))
        Liklihoods = json.load(open("Liklihoods.txt","r",encoding='utf8'))
        TT = json.load(open("Tag_Transitions.txt",'r',encoding='utf8'))
        TT0 = json.load(open("TT0.txt",'r',encoding='utf8'))
        input_string = input("Enter the input sentence you want to tag:")
        input_string = input_string.replace('\u06CC','\u064A')
        input_string = input_string.replace('\u06A9','\u0643')
        input_sequence = input_string.split(sep = " ")
        test = TEST()
        out = test.POS_TAGGER_TEST(input_sequence,WORDS_ID,TAGS_ID,Liklihoods,TT,TT0)
        print(out)
    elif(entered ==3 ):
        import time
        precision=list()
        try:
            K =int(input("Enter K for cross-fold validation test(default is 2):\n(Attention: files should have been created before with split_file.py)"))
        except:
            K=2
        for k in range(K):
            fp_name = "train_data_"+str(k+1)+".txt"
            train=TRAIN()
            train.POS_TAGGER_TRAIN(fp_name)
            del train
            fp1 = open("test_data_"+str(k+1)+".txt",'r',encoding='utf8')
            t=0
            f=0
            true_stage=0
            false_stage=0
            test=TEST()
            words=list()
            tags =dict()
            Flag =False
            i =0
            l=0
            t1 = time.time()
            WORDS_ID = json.load(open("word_id_tab.txt",'r',encoding='utf8'))
            TAGS_ID = json.load(open("tag_id_tab.txt",'r',encoding='utf8'))
            Liklihoods = json.load(open("Liklihoods.txt","r",encoding='utf8'))
            TT = json.load(open("Tag_Transitions.txt",'r',encoding='utf8'))
            TT0 = json.load(open("TT0.txt",'r',encoding='utf8'))

            print ("Loading Train data took %.2f" % (time.time() - t1))
            for line in fp1:

                line=line.replace("\n","")
                line1= re.sub(r'\s{2,100}',r'\t',line)
                line1=line1.replace("\n","")
                word_tag=line1.split("\t")
                words.append(word_tag[0])
                tags[i]=word_tag[1]
                i+=1
                if(word_tag[0]=='#'or word_tag[0]=='.'or word_tag[0]=='?'):
                        Flag=True
                        l+=1
                if(Flag):
                    i=0
                    output = test.POS_TAGGER_TEST(words,WORDS_ID,TAGS_ID,Liklihoods,TT,TT0)
                    for j in range(len(output)):
                        if(output[j]==tags[j]):
                            t+=1
                            true_stage+=1
                        else:
                            f+=1
                            false_stage+=1

                    words.clear()
                    tags.clear()
                    true_stage=0
                    false_stage=0


                    Flag=False
                    continue
            del test
            del output
            precision.append(t/(t+f))
            print(precision)
            fp1.close()

            del fp1
            gc.collect()

    elif (entered==4):
        input_string = input("Enter the file for batch input:")
        fp2 = open(input_string+"_output_file.txt",'w',encoding='utf8');
        fp = open(input_string,encoding='utf8')
        text = fp.read()
        lines = text.split("\n")

        WORDS_ID = json.load(open("word_id_tab.txt",'r',encoding='utf8'))
        TAGS_ID = json.load(open("tag_id_tab.txt",'r',encoding='utf8'))
        Liklihoods = json.load(open("Liklihoods.txt","r",encoding='utf8'))
        TT = json.load(open("Tag_Transitions.txt",'r',encoding='utf8'))
        TT0 = json.load(open("TT0.txt",'r',encoding='utf8'))

        for line in lines:
           if(line!=""):
            input_string = line
            input_string = input_string.replace('\u06CC','\u064A')
            input_string = input_string.replace('\u06A9','\u0643')
            input_sequence = input_string.split(sep = " ")
            test = TEST()
            out = test.POS_TAGGER_TEST(input_sequence,WORDS_ID,TAGS_ID,Liklihoods,TT,TT0)
            fp2.write(line)
            fp2.write("\t")
            for item in out :
                fp2.write(out[item]+" ")
            fp2.write("\n")
            
        fp.close()
        fp2.close()
    else:
        print('wrong command')

except:
    print("Error happened.")



