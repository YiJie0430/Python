import sys
import os,time,traceback
import random,re
execfile("configHub4.ini")

def find(pattern, string):
    match = re.search(pattern,string)                 
    if match: return match.group()
    else: 
        #raise Except("re string not find:%s"%pattern)
        return 0
    


def ParsingLog_Filter(logPath, station):
    string = os.popen("dir %s"%logPath + "Fail").read()
    pat = r"\w+_\d+.%s"%station
    faildata = re.findall(pat,string)
    pat_ = r"_\d+"
    chk =0
    fail_mac = []
    for i in faildata:
        retest_cnt = find(pat_,i)[1:]
        #print retest_cnt 
        mac = i[:12]
        if int(retest_cnt) >2:      ## Filter retest count >2 
            fail_mac.append(mac)
            os.popen("del %s\\%s"%((logPath+ "Fail"),i)).read()  # Delete fail count > 2 log
            os.popen("del %s\\%s.%s"%((logPath+ "PASS"),mac,station)).read()  # Delete fail count > 2 log in PASS folder
            print 'Del %s count %s'%(mac,retest_cnt)
    string = os.popen("dir %s"%logPath + "Fail").read()
    strpass = os.popen("dir %s"%logPath + "PASS").read()
    pat = r"\w+_\d+.%s"%station
    faildata = re.findall(pat,string)
    pat = r"\w+\.%s"%station
    passdata = re.findall(pat,strpass) 
    chk =0
    f = 0
    for i in faildata:
        mac = i[:12]
        if mac in fail_mac:
            f+=1
            os.popen("del %s\\%s"%((logPath+ "Fail"),i)).read() # Delete fail count > 2 MAC  , count < 2 in Fail folder  
            print 'Del Fail MAC: %s in Fail folder %d'%(mac,f)     
        if '%s.%s'%(mac,station) not in passdata:
            chk+=1
            os.popen("del %s\\%s"%((logPath+ "Fail"),i)).read() # Delete Fail folder MAC log not in Pass folder 
            print 'Del %s not in PASS folder %d'%(mac,chk)
    print '---------------------------------------------'
    string = os.popen("dir %s"%logPath + "Fail").read()
    strpass = os.popen("dir %s"%logPath + "PASS").read()
    pat = r"\w+_\d+.%s"%station
    faildata = re.findall(pat,string)
    print "Retest log total: %d"%len(faildata)
    pat = r"\w+\.%s"%station
    passdata = re.findall(pat,strpass)
    print "PASS log total: %d"%len(passdata)

def CountRetestRatio(csvcount,pass_total,fail_total,total_ratio,afi_dic):
    for err in afi_dic.keys():
        csvcount.write('%s,'%(err))
    csvcount.write('Others,')
    csvcount.write('Total,')    
    csvcount.write('\n')
    total = 0
    for err in afi_dic.keys():
        total+=afi_dic[err][1]
        csvcount.write('%s,'%(afi_dic[err][1]))
    csvcount.write('%d,'%(fail_total-total))
    csvcount.write('%d,'%fail_total) 
    csvcount.write('\n')
    r = 0 
    for err in afi_dic.keys():
        ratio = (afi_dic[err][1]/float(pass_total))*100
        r+=ratio
        csvcount.write('%.2f,'%(ratio)) 
    csvcount.write('%.2f,'%(total_ratio-r))    
    csvcount.write('%.2f,'%total_ratio)
    csvcount.write('\n')
    csvcount.write('\n')
  
    
def ParsingLog2csv(logPath,station,afi_dic,afi_major):
    csvPath = os.getcwd() + "\\csvdata\\"+"-".join(map(str,time.gmtime()[:3]))+"\\"
    if not os.path.isdir(csvPath):
        os.system("mkdir %s"%csvPath) 
    t= str(round(time.time(),1)).split(".")
    csvlog=open(csvPath+'\\%s_testdata_%s%s.csv'%(station,t[0][7:],t[1]),'w')
    csvcount=open(csvPath+'\\%s_failrate_%s%s.csv'%(station,t[0][7:],t[1]),'w')
    csvlog.write('MAC,Test Result,Fail Isuue,\n')
    
    string = os.popen("dir %s"%logPath+"PASS\\").read()
    pat = r"\w+\.%s"%station    
    data = re.findall(pat,string)
    pass_total = len(data); print pass_total    
    string = os.popen("dir %s"%logPath+"Fail\\").read()
    pat = r"\w+_\d+.%s"%station    
    data = re.findall(pat,string)
    fail_total = len(data); print fail_total
    #raw_input('pause')
    #data = ['9050CA8F1C30.W1-1']
    err_list = []
    for i in data:
        mac = i[:12]
        print mac
        log = logPath+"Fail\\" + i
        f = open(log,'r') 
        content = f.read().upper()
        f.close() 
        #pat=r'\Result:\w+'
        pat='FAIL'
        #result = find(pat,content).split('End')[-1]; raw_input(result)
        result = find(pat,content); #raw_input(result)
        #print result
        finish = False
        testfail = 0 
        if 'FAIL' in result:
            for j in fail_list: #['failed:','FAIL:','verify FAIL']:
                if finish: break
                '''
                pat=r'\%s.*'%j  # * is >= 0 ; + is >=1 
                issue = find(pat,content)
                if issue: finish = True
                ''' 
                point=str()
                for k in content.splitlines():
                    if 'POWER...' in k:
                          try:
                             point=k.split('] CALIBRATE')[-1].split('POWER.')[0].strip()
                          except: pass
                    if 'IQ_VERIFY_RX_PER' in k:
                          try:
                             point=k.split('IQ_VERIFY_RX_PER , ')[-1].split('Path Loss')[0].strip()
                          except: pass    
                    if j in k:
                        if 'IQ_VERIFY_TX' in k:
                          try:
                             point=k.split('IQ_VERIFY_TX, ')[-1].split('FAIL')[0].strip()
                          except: pass  
                        #issue = k + '|' + point ; 
                        issue = k; info = point.replace(',',';')
                        testfail = 1; 
                    else:
                        if testfail:
                            if 'END' in k:
                                finish = True
                                break     
                            issue+=k
                        
                
                
        else: issue = "NA";finish = True
        if not finish: issue = 'not find'
        if issue <> "NA":
            #if issue not in err_list: err_list.append(issue)            
            for err in afi_dic.keys():
                if err == 'Parsing Error': 
                    if 'DOWN' in issue: continue                      
                if err == 'cli cmd': 
                    if 'temporarily unavailable' in issue: continue                    
                for err_msg in afi_dic[err][0]:
                    if err_msg in issue: 
                        afi_dic[err][1]+=1 #Count major error number
                        break 
            if  afi_major: 
                for err in afi_major.keys():
                    if err == 'Parsing Error': 
                        if 'DOWN' in issue: continue                      
                    if err == 'cli cmd': 
                        if 'temporarily unavailable' in issue: continue
                    for err_msg in afi_major[err][0]:
                        if err_msg in issue: 
                            afi_major[err][1]+=1 #Count major error number
                            break 
                               
            csvlog.write('%s,%s,%s,%s,\n'%(mac,result,issue,info))
    csvcount.write('Total,PASS,Retest,Retest Ratio\n') 
    total_ratio = (fail_total/float(pass_total))*100    
    csvcount.write('%d,%d,%d,%.2f\n\n'%(pass_total,(pass_total-fail_total),fail_total,total_ratio)) 
    for i in [afi_dic,afi_major]:
        #if i: CountRetestRatio(csvcount,pass_total,i)
        if i: CountRetestRatio(csvcount,pass_total,fail_total,total_ratio,i)
        
    csvcount.close()
          
    csvlog.close()



    
#### MAIN code ####

#fail_list = ['SNR :','OFDMA SNR :']
fail_list = ['ErrorCode']
fail_list = ['FAIL']

#ParsingLog_Filter(logPath_AFI0,'AFI0')
ParsingLog2csv(logPath, 'W1-1',w11_dic,None)
#ParsingLog_Filter(logPath_AFI1,'AFI1')
#ParsingLog2csv(logPath_AFI1, 'AFI1',afi1_dic,afi1_major)