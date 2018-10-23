import os,shutil,time

dir_path={'AFI0':os.getcwd()+'\\AFI0',\
          'AFI1':os.getcwd()+'\\AFI1',\
          'T1-0':os.getcwd()+'\\T1-0'}

def folder_create(path):
    if not os.path.exists(path): os.makedirs(path)
    

def file_move(current_path,new_path):
    shutil.move(current_path,new_path)

while True:
    act=raw_input('plz pressing "Enter" to start...'); print act
    if act != '': pass
    else:    
        print 'MAC sorting...'
        s_time=time.time()
        try:
            for walk in dir_path.keys():
                for dirpath,dirs,filename in os.walk(dir_path[walk]):
                    for name in filename:
                        f_name=name.split('.')[0]
                        folder_create(os.getcwd()+'\\'+f_name)
                        shutil.move(dirpath+'\\'+name,os.getcwd()+'\\'+f_name+'\\'+name)
                if not os.listdir(dir_path[walk]): 
                    shutil.rmtree(dir_path[walk])
            print 'Processing done, sorting time: %3.2f'%(time.time()-s_time)
        except: print 'folder error'
