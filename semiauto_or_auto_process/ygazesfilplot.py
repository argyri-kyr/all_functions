
#Sinarthsh opou epistrefei ta kopsimata(kiklakia) san shmeia(xo,yo) se duo listes x,y kai epistrefei epishs kai thn kokkinh grammi sto grafhma dhladh to meso oro(average) twn y.
def ygazesfilPlot(filetxt, sub1, exam, text, pageno):
    file = open(filetxt)
    
    mpika = False
    find=False
    filter=False
    average=[]
    x = []
    y = []
    s=""
    for line in file:
        for word in line.split():
            if(word[0:7]=="Subject"):
                filter = False
               
        if(line.strip()=="Subject {sub1} Exam {exam} Text {text} Page {page}".format(sub1=sub1, exam=exam, text=text, page=pageno)):
            find=True
            average=[]
            x = []
            y = []
            a=""
            continue
        
        if(find==True and filter==False):
            for char in line:
                if(char=="("):
                    mpika=True
                    s+=char
                if(mpika==True):
                    s+=char
                if(char==")"):
                    mpika=False
                    s+=char

                    x.append(findPoint(s)[0])
                    y.append(findPoint(s)[1])
                    
                    s=""              
        
        if(find==True and line.strip()=="Filtered y gazes"):
                filter=True
                find=False
                continue
            
        if(filter==True):
            for char in line:
                if(char!=","):
                    a+=char
                if(char==","):
                    average.append(int(a))
                    a=""
        
    
    return x, y, average

#Boithitiki sinartish gia na brw ta kopsimata(xo,yo)
def findPoint(s):
    komma=False
    x=""
    y=""
    for i in range(len(s)):
        if(s[i]!="(" and s[i]!=")" and s[i]!="," and komma==False):
            x+=s[i]

        if(s[i]==","):
            komma=True

        if(s[i]!="(" and s[i]!=")" and s[i]!="," and komma==True):
            y+=s[i]
    
    return int(x), int(y)