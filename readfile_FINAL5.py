import csv
import os
import sys
import io
from threading import Thread
import threading
import time
import subprocess
import pipes as p
from filelock import Timeout, FileLock
time1=time.time()
file_path = "data.csv"
lock_path = "data.csv.lock"

lock2 = FileLock("error.txt.lock", timeout=100)
lock = FileLock(lock_path, timeout=100)

si = subprocess.STARTUPINFO()
#si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.dwFlags |= subprocess.HIGH_PRIORITY_CLASS
si.wShowWindow = subprocess.SW_HIDE # default 
DETACHED_PROCESS = 0x00000008


def write_csv(comp_name,year,nowords,search_word,total_words):

    with FileLock(lock_path, timeout=100):
        with open('data.csv', mode='a+', newline='') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow([comp_name, year,search_word,nowords,total_words])
                data_file.close()

file_names= [a[6:len(a)-4] for a in os.listdir() if a.startswith("group") and a.endswith(".txt")]
all_groups={}

for name2 in file_names:
    with open(f'group_{name2}.txt', mode='r') as word_file:
        word_file.seek(0)
        csv_reader = csv.reader(word_file)
        temp_list=[]
        for word in csv_reader:
            temp_list.append(str(word[0].lower()))
        all_groups[f"{name2}"]= temp_list
        word_file.close()



def write_grouping(folder,filename,values2,total_words):
    group_path=f"{folder}/{filename}"
    file_size=round((os.stat(group_path).st_size)/(1024**2) , 2)
    
    combined_list=[]
    #print(values2,"ahahhah")
    for y in values2.keys():
        combined_list.append(values2[y])
        
    #print(combined_list)
    total_param=[folder,filename.replace(".pdf",""),file_size]+combined_list+[total_words]

    with FileLock("grouped_data.lock", timeout=100):
        with open('grouped_data.csv', mode='a+', newline='') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                
                data_writer.writerow(total_param)
                data_file.close()


def mymain(search_word,x,y):   

    try:
        command = f'pdftotext.exe "{x}"/{y} -'
        output,error = subprocess.Popen(command, shell=False,startupinfo=si, stdout=subprocess.PIPE,creationflags=DETACHED_PROCESS).communicate()    
        final_text=output.decode("Latin1")
        text3=final_text
        final_text=final_text.lower()
        final_text=final_text.replace("  "," ")
        if final_text == "":
            raise
        for b in search_word:                   
            final_count=final_text.count(b.lower())
            total_words=len(final_text.split())
            write_csv(x,y.replace(".pdf",""),final_count,b,total_words)

            
        temp_group_dict={}
        text3=text3.lower()
        for groups in all_groups.keys():
            total2=0

            for group_words in all_groups[groups]:    
                cur=0

                while 1==1:
                    cur=text3.find(group_words,cur)
                    if cur==-1:
                        break
                    if text3[cur-1].isalpha() or text3[cur+len(group_words)].isalpha():

                        cur=cur+1
                        continue

                    cur=cur+1
                    total2=total2+1
                    

            temp_group_dict.update({groups:total2})
    
        
        write_grouping(x,y,temp_group_dict,total_words)



    except:
        with FileLock("error.txt.lock", timeout=100):

            with open('error.txt', mode='a+') as efile:
                efile.write("\n Error occurred in " + x + " Year:" + y.replace(".pdf",""))
                efile.close()


    

with FileLock(lock_path, timeout=100):
    with open('data.csv', mode='a+', newline='') as data_file:
        data_file.close()
threads=[]

words4=(sys.argv[1]).replace("*"," ").split(',')
#print(words4)
comp1=(sys.argv[2].replace(";"," "))
tot_files=os.listdir(comp1)
for x2 in tot_files:
    t=Thread(target=mymain,args=(words4,comp1,x2))
    threads.append(t)

for x in threads:
    x.start()

for x in threads:
    x.join()

print(round(((time.time()-time1 )/ 60),3))



        
