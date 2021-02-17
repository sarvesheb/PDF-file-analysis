import time
import os
import csv
import pipes as p
import subprocess
time1=time.time()
si = subprocess.STARTUPINFO()
#si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.dwFlags |= subprocess.HIGH_PRIORITY_CLASS
si.wShowWindow = subprocess.SW_HIDE # default 
si.dwFlags |= subprocess.DETACHED_PROCESS #= 0x00000008
DETACHED_PROCESS = 0x00000008
HIGH_PRIORITY_CLASS=0x00000080
processlist=[]
list5=[]
with open('keywords.txt', mode='r') as data_file:
        
    data_file.seek(0)
    mykeylist=data_file.readlines()
    for line in mykeylist: 
        list5.append(line.strip().replace(" ","*")) 

list_str=""
for item in list5:
        list_str=list_str+item+","
list_str=list_str[0:len(list_str)-1]



all_folders=next(os.walk(os.getcwd()))[1]
len_fol=len(all_folders) 
total_param=['Company', 'Year', 'Search Word', 'Occurrences','Total Words']
with open("data.csv", "a+") as f:
    f.seek(0)
    first_line=f.readline().strip()
    if len(first_line)==0:
        data_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(total_param)
    f.close()


file_names= [a[6:len(a)-4] for a in os.listdir() if a.startswith("group") and a.endswith(".txt")]
total_param=['Company','Year','File Size(MB)',]+file_names +['Total Words']

with open("grouped_data.csv", "a+") as f:
    f.seek(0)
    first_line=f.readline().strip()
    if len(first_line)==0:
        data_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(total_param)
    f.close()


total=0
os.system('cls')
positionStr = 'Current company: ' + str(total).rjust(5) + '     Total company: ' + str(len_fol).rjust(6)
print(positionStr)#, end='')
#print('\b' * len(positionStr), end='', flush=True)
while total<len_fol:
        

        command = f"python readfile_FINAL5.py {list_str} {all_folders[total].replace(' ',';')}"
        p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE,creationflags=DETACHED_PROCESS)#HIGH_PRIORITY_CLASS)
        total=total+1
        positionStr = 'Current company: ' + str(total).rjust(5) + '     Total company: ' + str(len_fol).rjust(6)
        print(positionStr)#, end='')

        p.wait()





time2=time.time()

print("\nTotal execution time:",round((time2-time1)/60,2), " Minutes")
