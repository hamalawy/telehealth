from math import *
n=input("Enter number of points:")
sum_x=0
sum_y=0
sum_xx=0
sum_xy=0
for i in range(1,n+1):
    print "For point %s"%i
    x=input("Enter x:")
    y=input("Enter y:")
    sum_x=sum_x+x
    sum_y=sum_y+y
    xx=pow(x,2)
    sum_xx=sum_xx+xx
    xy=x*y
    sum_xy=sum_xy+xy
print "sum of x"+str(sum_x)
print "sum of y"+str(sum_y)
print "sum of x2"+str(sum_xx)
print "sum of xy"+str(sum_xy)
#Calculating the coefficients
a=(-sum_x*sum_xy+sum_xx*sum_y)/(n*sum_xx-sum_x*sum_x)
b=(-sum_x*sum_y+n*sum_xy)/(n*sum_xx-sum_x*sum_x)

print "The required straight line is Y=%sX+(%s)"%(b,a)

