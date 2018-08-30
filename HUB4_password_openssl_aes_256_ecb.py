#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import os
f = open(os.getcwd()+'\\in.txt','rb')
a=f.read()
print '=========in.txt==========='
print repr(a)
print a.encode('hex')
print (binascii.hexlify(a))
f.close()
print '=========================='

f = open(os.getcwd()+'\\file.txt','wb')
print repr(a)
a=a.replace('\r\n', '\n')
f.write(a)
f.close()


f = open(os.getcwd()+'\\file.txt','rb')
b=f.read()
print '=========file.txt==========='
print repr(b)
print b.encode('hex')
print (binascii.hexlify(b))
f.close()
print '=========================='


f = open(os.getcwd()+'\\password_test.txt','rb')
a=f.read()
print '=========password_test.txt==========='
print (binascii.hexlify(a))
f.close()
print '=========================='



f = open(os.getcwd()+'\\out2.txt','rU')
a=f.read()
print a.encode('hex')
f.close()