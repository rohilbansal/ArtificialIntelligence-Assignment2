##import random
##
##z=['w','b']
##
##for i in range (19,20):
##    n=i
##
##    st="."*(n*n)
##
##    place=[]
##
##    sig=random.randint(0,n)
##    for i in range(sig):
##        o=random.randint(0,n*n-1)
##        if o not in place:
##            place.append(o)
##    s=list(st)
##
##    for i in place:
##        o=random.randint(0,n*n-1)
##        l=random.randint(0,n*n-1)
##        if o!=l:
##                s[o]='w'
##                s[l]='b'
##    
##    print "NEXT" + str(n)
##    ss=''.join(s)
##    #   print ss
##    count=0
##    for i in ss:
##            if i in ('w','b'):
##                count+=1
##    #print "THE COUNT", count
##                    
##
##    kk= str(n)+" "+ str(3)+ " " +ss+" "+str(5)
##    
##    print kk
##    print "THE COUNT", count
##
##    print()
##    



st='.wbww.bwbw.bwbb..........'

for i in range(6,36):
        k=i*i
        j=len(st)-k
        n='.'*abs(j)
        print str(i)+' 3 '+st+n+ " 5"

