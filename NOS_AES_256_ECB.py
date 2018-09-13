#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import os
import sys
import subprocess
from functools import wraps

##########################
# Athor: Y.J. Wang @2018.08.30 
# usage:       
# 1. this py should be under the $path\openssl\bin\, run as NOS_AES_ECB.py <$string> 
# 2. variable "inword" is the string object and will be saved in in.txt for the encryption.
# 3. the encryption key is hardcode in the AES_ECB().
# 4. the password_hex from AES_ECB() is the final encrypted hex which required by customer(NOS). 
##########################

def verifyformat(func):
    @wraps(func)
    def verifictaion(*args):
        new_b = func()
        with open(os.getcwd() + '\\in.txt','rb') as f:
            b = f.read()
            f.close()
        print ('=====in.txt======\ncharacter:{}\nhex:{}\n================='.format(repr(b),b.encode('hex')))
        if r'\r\n' in repr(b) or r' ' in repr(b) and b == new_b:
            return 0
        else:
            return 1
    return verifictaion
    
def newline(func):
    @wraps(func)
    def switching(*args):
        _b = func()
        with open(os.getcwd() + '\\in.txt','wb') as f:
            b = _b.replace(' ','')
            new_b = b.replace('\r\n', '\n')
            f.write(new_b)
            f.close()
        return new_b
    return switching

@verifyformat
@newline
def checkformat():
    with open(os.getcwd() + '\\in.txt','rb') as f:
        b = f.read()
        f.close()
    return b

def AES_ECB():
    print ('AES-256-ECB encrypt start...')
    encrypt = subprocess.Popen('openssl enc -e -AES-256-ECB -K EBEBD739001462C01C8BD4A76F1B7028 -in in.txt -out out.txt -p', shell=True)
    encrypt.communicate()
    with open(os.getcwd()+'\\out.txt','rb') as f:
        b = f.read()
        f.close()
    return b.encode('hex')

    
def main():
    ### input password ###
    inword = sys.argv[1]

    ### creating in.txt in $path\openssl\bin for encrypting
    p = subprocess.Popen('echo {}>{}'.format(inword,os.getcwd()+'\\in.txt'), shell=True)
    p.communicate()

    ### windows newline is '\r\n', need to switch to linux format '\n'
    if checkformat():
        ### encrypt and encode to the hex
        password_hex = AES_ECB()
        print ('encrtyped hex:{}'.format(password_hex))

    
if __name__ == '__main__':
    main()    



    