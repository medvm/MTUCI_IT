a = int(input('a ~> '))
b = int(input('b ~> '))
c = int(input('c ~> '))
d=b**2-4*a*c
if d == 0:
    x=(-b + d**(0.5))/(2*a)
    print ('x ~>', x)
elif d > 0:
    x1=(-b + d**(0.5))/(2*a)
    x2=(-b - d**(0.5))/(2*a)
    print ('x1 ~>', x1,'\nx2 ~>', x2)
else:
    print ('Real roots does not exists')
