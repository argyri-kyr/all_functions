import sys
from autoloaduncutgazeszoom_Procedure import  autoloaduncutgazeszoom_Procedure
    
    
bypass = 1
hardcases = 0
onlylefteye = 0
onlyrighteye = 0
firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
    

# Orizw se poia exam einai to kathe subject
exam = []


if( len(sys.argv) > 1 ):
    subs = []
    texts = []
    multiplesubjects = sys.argv[-1]

    if( multiplesubjects == "True" ):
        
        if( len(sys.argv) == 4 ):
            number = sys.argv[1]
            if(number[0]!="["):
                subs.append(int(number))
            else:
                startsub = ""
                endsub = ""
                komma = False
                for i in range(1,len(number)-1):
                    
                    if( number[i]!="," and komma==False ):
                        startsub += number[i]
                    
                    if( number[i]=="," ):
                        komma = True
                    
                    if( number[i]!="," and komma==True ):
                        endsub += number[i]
            
                subs = [i for i in range(int(startsub), int(endsub))]

        elif( len(sys.argv) > 4):
            for i in range(1, len(sys.argv)-2):
                subs.append(int(sys.argv[i]))
            
        texts = [ str(sys.argv[-2]) ]
    
    
    elif(multiplesubjects == "False"):
        subs = [ int(sys.argv[1]) ]
        for i in range(2, len(sys.argv)-1):
            texts.append(str(sys.argv[i]))
            

def autoloaduncutgazeszoom_main():
    autoloaduncutgazeszoom_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)

autoloaduncutgazeszoom_main()            