__author__ = 'Shohreh'
import re
fp = open("Collection UNI.txt","r",encoding='utf-8')


fp.seek(0)
text = fp.read()
punc ={'#','?','.','؟'}
c=0
try:
    K=int(input("Enter K to divide file into k train and k test files:(default is 1)"))
except:
    K=1
for p in punc:
    c+=text.count(p)

train_number = int(c*0.9)
test_number = c-train_number

fp.seek(0)
words = list()
i =0
counter1=0
counter2=1
y=0
for k in range(K):
    file_train = open("train_data_"+str(k+1)+".txt","w",encoding='utf-8')
    file_test = open("test_data_"+str(k+1)+".txt","w",encoding='utf-8')

    i=0
    for line in fp:
        y+=1
        line=line.replace("\n","")
        line1= re.sub(r'\s{2,100}',r'\t',line)
        word_tag=line1.split("\t")
        
        if(i<=test_number*counter1):
            file_train.write(line+"\n")
            if(word_tag[0]=='#'or word_tag[0]=='.'or word_tag[0]=='?'or word_tag[0]=='؟'):
                i+=1
        elif(i<=test_number*counter2):
            file_test.write(line+"\n")
            if(word_tag[0]=='#'or word_tag[0]=='.'or word_tag[0]=='?'or word_tag[0]=='؟'):
                i+=1
        else:
            file_train.write(line+"\n")

    file_test.close()
    file_train.close()
    counter1+=1
    counter2+=1
    fp.seek(0)













