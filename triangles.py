list = [5,10,3,88,41,7,1161]
print (list)
smax=0
for i in range(len(list)):
    for j in range(i+1, len(list)):
        for k in range(j+1, len(list)):
            a=list[i]
            b=list[j]
            c=list[k]
            if a+b>c and a+c>b and c+b>a and a>0 and b>0 and c>0:
                p=(a+b+c)/2
                s=(p*(p-a)*(p-b)*(p-c))**0.5
                if s>smax:
                    smax=s
                    print (smax)
