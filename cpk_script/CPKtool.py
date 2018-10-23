# The Program is used to extract number data to exec format
import glob,os,re,sys,time,fnmatch,zlib
from wxPython.wx import *

version = "v1.4"

execfile("mft_log.def")
#execfile("fqc_log.def")

#stations = {"nvm":nvm,"t11":t11,"t12":t12,"t21":t21,"t22":t22,"t3":t3,"fqc1":fqc1,"fqc2":fqc2,"fqc3":fqc3}
#stations = {"T1-2":t12}
#stations = {"t20":t20}
#stations = {"nvm":nvm}
#stations = {"ate":t11}
#stations = {"T11":t11}
#stations = {"t12":t12}
stations = {"T21":t22}
#stations = {"fq1":fq1}
#stations = {"fq2":fq2}
#stations = {"fqc3":fqc3}
#stations = {"t21":t21}
#stations = {"t12":t12}
#stations = {"dscf":dscf}
#file_patterns = (("BVW-3653","*.t11"),)
#file_patterns = (("BVW-3653","*.t12"),)
#file_patterns = (("BVW-3653","*.t21"),)
file_patterns = (("SMCD3GNV","*T21"),)
programs = {"t11":"BIZ8014\\Uscal.py",
            "t12":"BIZ8014\\Dscal.py",
            "t21":"BIZ8014\\System.py"}

pathList = ["E:\\8014_log\\OrderByDate\\20060501-20060630\\",
            "E:\\8014_log\\OrderByDate\\20060701-20060831\\",
            "E:\\8014_log\\OrderByDate\\20060901-20061031\\",
            "E:\\8014_log\\OrderByDate\\20061101-20061231\\",
            "E:\\8014_log\\OrderByDate\\20070101-20070228\\",
            "E:\\8014_log\\OrderByDate\\20070301-20070430\\",
            "E:\\8014_log\\OrderByDate\\20070501-20070630\\",
            "E:\\8014_log\\T1-1\\"]

############################
# Functions                #
############################
def WalkDir(dir,pattern=""):
    "walk a directory tree, using a generator"
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in WalkDir(fullpath,pattern):  # recurse into subdir
                yield x
        else:
            if pattern and not fnmatch.fnmatch(f,pattern):
                continue
            yield fullpath



def FindFile(fname,flist_dict):
    name = ""
    try:
        name = flist_dict[fname]
    except:
        pass
    return name


def GetValue(data,l,r=0):
    li = data.find(l)
    if r:
        ri = data.find(r)
    else:
        ri = len(data)+1
    return data[li+len(l):ri].strip()



def GetCriteria(data):
    # remove "Average:" condition later for new version MFT programs
    if "Average:" in data:
        match = re.findall(r'[+-]?\d+\.?\d*',data)
        aver = float(match[2])
        offset = float(match[3])
        return "%.2f~%.2f"%(aver-offset,aver+offset)
    i = data.rfind('(')
    if i >= 0 :
        j = data.rfind(')')
        return data[i+1:j].strip()
    i = data.rfind('<')
    if i >= 0 :
        return data[i:].strip()
    i = data.rfind('>')
    if i >= 0 :
        return data[i:].strip()
    return ""



def InputPath():
    application = wxPySimpleApp()
    # Create the dialog
    dialog = wxDirDialog ( None, message = "SMC-8014 CSV Log Generator %s"%version )
    # Show the dialog and get user input
    if dialog.ShowModal() != wxID_OK:
        sys.exit(1)
    input_path = dialog.GetPath()+"\\"

    print "Working Path: %s"%input_path
    return input_path


def GetOutputName(modelname,PData,PDate,check_sum,station_name,TDate):
    #outname = "%s_%s_%s_"%(modelname,station_name,check_sum)+"%04d-%02d-%02d.csv"%time.gmtime()[:3]
    #outname = "%s_%s-%s"%(modelname,PData,PDate)+"_%04d%02d%02d"%time.gmtime()[:3]+"-%06X"%check_sum+"_HITTPE01%s_%s.csv"%(station_name.upper(),TDate)
    #outname = "%s_%s_%s_"%(model_name,station_name,check_sum)+"%04d-%02d-%02d.txt"%time.gmtime()[:3]
    outname = "%s_%s-%s"%(modelname,PData,PDate)+"_%04d%02d%02d"%time.gmtime()[:3]+"-%s"%check_sum+"_HITTPE01%s_%s.csv"%(station_name.upper(),TDate)
    print "Output file:",outname
    return outname



def CreateDeviceList(files):
    devices = {}
    for i in files:
        basename = os.path.basename(i)
        try:
            if os.path.getmtime(device[basename]) < os.path.getmtime(i):
                devices[basename] = i
        except:
            devices[basename] = i
    return devices



def CreateHeader(data,model):
    result = ""
    for i in data:
        if type(i) == type("A"):
            if i.find("(") >= 0 :
                result += i.rstrip(":= \t-")[0:i.rstrip(":= \t-").find("(")] + ","
            else:
                result += i.rstrip(":= \t-") + ","
        else:
            if "508" in model and i[0].split()[0] in ("#9","#10","#11","#12","#P5","#P6"):
                continue
            if i[0].find("(") >=0:
                result += i[0][0:i[0].find("(")] + ","
            else:
                result += i[0] + ","
    return result

def CreateUnit(data,model):
    result = ""
    for i in data:
        if type(i) == type("A"):
            #result += i.rstrip(":= \t-")+","
            if i.find("(") >= 0 :
                result += GetValue(i,'(',')') + ","
            else:
                result += ","
        else:
            if "508" in model and i[0].split()[0] in ("#9","#10","#11","#12","#P5","#P6"):
                continue
            if i[0].find("(") >=0:
                result += GetValue(i[0],'(',')') + ","
            else:
                if i[2] == 0:
                    result += "P/F,"
                else:
                    result += ","
    return result
def CreateLog61(data,station,model):
    result = ""
    Min = ""
    Max = ""

    for i in data:
       if "Channel 1 MSE:" in i:
            print i
            result += str(i.split("Channel 1 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 1 Measure" in i and "DSPower=" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 2 MSE:" in i:
            print i
            result += str(i.split("Channel 2 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 2 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 3 MSE:" in i:
            print i
            result += str(i.split("Channel 3 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 3 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 4 MSE:" in i:
            print i
            result += str(i.split("Channel 4 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 4 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 5 MSE:" in i:
            print i
            result += str(i.split("Channel 5 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 5 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 6 MSE:" in i:
            print i
            result += str(i.split("Channel 6 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 6 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 7 MSE:" in i:
            print i
            result += str(i.split("Channel 7 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 7 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 8 MSE:" in i:
            print i
            result += str(i.split("Channel 8 MSE:")[1].split("(")[0].strip())+","
       elif "Channel 8 Measure" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "Channel 1 Measure= 40.00" in i:
            result += str(i.split("Diff:")[1].split("(")[0].strip())+","
       elif "total time:" in i:
            result += str(i.split("total time:")[1].strip())+","
    print result
    return result,Min,Max
    raw_input("debug")
def CreateLog(data,station,model):
    result = ""
    Min = ""
    Max = ""
    if not data:
        result = "N/A,"*(CreateHeader(station,model).count(",")-1)
        Min = ","*(CreateHeader(station,model).count(","))
        Max = ","*(CreateHeader(station,model).count(","))
        return result,Min,Max
    if len(data)<3:
        result = data[0]+"N/A,"*CreateHeader(station,model).count(",")
        Min = ","*(CreateHeader(station,model).count(","))
        Max = ","*(CreateHeader(station,model).count(","))
        return result,Min,Max
    for i in station:
        if type(i) == type("A"):
            item = (i,i,1)
        else:
            if "508" in model and i[0].split()[0] in ("#9","#10","#11","#12","#P5","#P6"):
                continue
            item = i
        if item[0][:4] == "Date":
            test_date = data[1].split()[-5:]
            result += "%04d%02d%02d %02d:%02d:%02d,"%time.strptime(" ".join(test_date))[:6]
            Min += ","
            Max += ","
            continue
        if item[0][:7] == "Program":
            result += GetValue(data[0],':','/')+","
            Min += ","
            Max += ","
            continue

        for j in data:
            k = j.find(item[1])
            if k >= 0:
                k += len(item[1])
                if item[2] == 0:            # found and no output
                    result += "PASS"+","
                    Min += "PASS,"
                    Max += ","
                elif item[2] == 1:          # output value
                    value = j[k:].strip()
                    value = value.replace(",",".")
                    value = value.replace("!,","")
                    if value.find("sec") >= 0:
                        value = value[0:value.find("sec")]
                    if value.find("(PASS)") >= 0:
                        value = value[0:value.find("(PASS)")]
                    if value.find("(") >= 0:
                        value = value[0:value.find("(")]
                    result += value +","
                    Min += ","
                    Max += ","
                else:                       # output value and criteria
                    value = j[k:].strip().split()[0]
                    value = value.rstrip(",")
                    criteria = GetCriteria(j)
                    if criteria.find("~")>=0:
                        Min += criteria.split("~")[0].strip() + ","
                        Max += criteria.split("~")[1].strip() + ","
                    elif criteria.find(">")>=0:
                        Min += criteria.replace(">","").replace("=","").strip() + ","
                        Max += ","
                    elif criteria.find("<")>=0:
                        Min += ","
                        Max += criteria.replace("<","").replace("=","").strip() + ","
                    else:                        
                        Min += criteria + ","
                        Max += criteria + ","

                    result += value+","
                data.remove(j)
                break
        else:
            if item[0][:6] == "Result":
               result += "FAIL"+","
               Min += ","
               Max += ","
            else:
               result += "N/A,"
               Min += ","
               Max += ","
    return result,Min,Max



def SplitCSV(filename,split_field_number=254,keep_head_field=6):
    output_name,ext = os.path.splitext(filename)
    output = []
    for i in open(filename).readlines():
        data = i.rstrip().split(",")
        fields = len(data)
        if fields <= split_field_number:
            return
        if not output:
            n = 1 + fields/split_field_number
            print "Original File:", output_name
            for j in range(n):
                outname = output_name+"_%d"%(j+1)+".csv"
                print "Split to file:",outname
                output.append(open(outname,"w"))
        for j in range(n):
            if j:
                output[j].write(",".join(data[:keep_head_field])+",")
            output[j].write(",".join(data[j*split_field_number:(j+1)*split_field_number]))
            output[j].write("\n")

    for i in output:
        i.close()

def ChangeArrisChecksum(filepath,filename):
    filedata = open(os.path.join(filepath,filename),"rb").read()
    check_sum = 0xffffffL
    check_sum &= sum(map(ord,map(None,filedata)))

    index = filename.find("_HITTPE")
    old_cs = filename[index-6:index]
    newfilename = os.path.join(filepath,filename.replace(old_cs,"%06X"%check_sum))
    os.rename(os.path.join(filepath,filename),newfilename)
    SplitCSV(newfilename)


########## convert datatime format to string format  ex.Mon Apr 24 10:19:54 2006 --> 20060424 ##########
def DateTime2String(datetime=time.localtime()):
    temp = ""
    try:
        temp = time.localtime(datetime)
    except:
        temp = time.localtime()
    return "%s%s%s"%(str(temp[0]).zfill(4),str(temp[1]).zfill(2),str(temp[2]).zfill(2))

############################
#      Main    Program     #
############################
print "8014 Serial CSV Log Generator", version
path = InputPath()
#for path in pathList:
sk = stations.keys()
sk.sort()
outputname=[]
for i in sk:
    for model_name, file_pattern in file_patterns:
        #ProgramDate = DateTime2String(os.path.getmtime("c:\\product\\" + programs[i]))
        #ProgramName = GetValue(programs[i],"\\",".py")
        #ProgramVer = ""
        #TestDate = DateTime2String()

        deviceList = CreateDeviceList(WalkDir(path,file_pattern))
        current_sn="xxxxx"
        deviceSorted = deviceList.keys()
        deviceSorted.sort()
        #print  deviceSorted
        #

        Head = ""
        Unit = ""
        Minstring = ","*(CreateHeader(stations[i],model_name).count(","))
        Maxstring = ","*(CreateHeader(stations[i],model_name).count(","))
        logstring = ""
        for basename in deviceSorted:
            if current_sn in basename:
                continue
            current_sn,ext = os.path.splitext(basename)
            print "Processing %s.*"%current_sn

            fn = FindFile(current_sn+"."+i,deviceList)
            print fn
            raw_input("debug")
            if fn:
                fn_data = open(fn).readlines()
            else:
                fn_data = [""]
             
            LogData=CreateLog61(fn_data,stations[i],model_name)
            #LogData=CreateLog(fn_data,stations[i],model_name)
            
            logstring += model_name + "," + current_sn +"," + LogData[0] + "\n"
            if len(Minstring) <= len(LogData[1]):
                Minstring = LogData[1]
            if len(Maxstring) <= len(LogData[2]):
                Maxstring = LogData[2]
        Head = "Product,Serial Number," + CreateHeader(stations[i],model_name) + "\n"
        Unit = "Unit," + "," + CreateUnit(stations[i],model_name) + "\n"
        Minstring = "MIN.," + "," + Minstring + "\n"
        Maxstring = "MAX.," + "," + Maxstring + "\n"
        #for testdata in logstring.strip().split("\n"):
            #tmp=""
            #try:
                #if TestDate > testdata.split(",")[Head.split(",").index("Date")].split()[0]:
                    #TestDate = testdata.split(",")[Head.split(",").index("Date")].split()[0]
            #except:
                #continue
            #if ProgramVer < testdata.split(",")[Head.split(",").index("Program")].strip("N/A"):
                #ProgramVer = testdata.split(",")[Head.split(",").index("Program")]

        #checksum = "XXXXXX"
        #output_name = GetOutputName(model_name,ProgramName+ProgramVer,ProgramDate,checksum,i,TestDate)
        output_name = model_name+"-"+i+".csv"
        print output_name
        outputname.append(output_name)
        output = open(path+output_name,"w")

        output.write(Head + Unit + Minstring + Maxstring + logstring)
        output.close()
        #ChangeArrisChecksum(path,output_name)
