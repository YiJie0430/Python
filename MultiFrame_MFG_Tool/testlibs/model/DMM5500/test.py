import os,sys
def striback():
	a='a b c d'
	b='1 2 3 4'
	return (a,b)

a=striback(); print a
a=a[0].split(' '); print a

c=['2','3','4','5']

t=dict()
for i,v in enumerate(a):
	t.update([(v,c[i])])
print t

