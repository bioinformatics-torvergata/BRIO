import re
import sys
import subprocess

pattern_seq='^[ACGUTacgut]*$'
pattern_dot='^[\.\(\)]*$'

#check file type
f=open(sys.argv[1])
o=open(sys.argv[2], 'w')

#check file length
out=subprocess.check_output('wc -l '+sys.argv[1], shell=True).decode('utf-8')

len_file=int(out.split()[0])
#print(len_file)

seq_len=0
f_type=''

first=f.readline().strip()
second=f.readline().strip()


##########prima parte controllo tipo di file##########
if len_file < 2:
    #file vuoto o solo nome
    f_type='wrong'
    
elif len_file == 2:
    #ho solo nome e seq
    if first[0]!=">":
        o.write('1')
    else:
        f_type='fasta'
        
elif len_file == 3:
    third=f.readline().strip()
    if first[0]!=">":
        o.write('1')
    else:
        f_type='dot'

else:
    third=f.readline().strip()
    #non mettere strip qui!
    quart=f.readline()
    
    if first[0]!=">":
        o.write('1')
    
    if quart[0]==">" or len(quart)==1:
        f_type='dot'
    
    else:
        if re.search(pattern_seq, quart) != None and third[0]==">":
            f_type='fasta'
        else:
            f_type="bear"
            
            
            
            
            
#print(f_type)
#print(len_file)


##########seconda parte controllo file riga x riga##########
#check all lines
check_list=[]
if f_type != 'wrong':
    f=open(sys.argv[1])
    #prima riga name
    line=f.readline()
        
    if f_type=='fasta':
        #seconda riga seq
        line=f.readline()
        if re.search(pattern_seq, line) != None and line != '\n':
            #print('prova1')
            check_list.append(0)
        else:
            #print('prova2')
            check_list.append(1)
        
        if len_file >2:
            while(line):
                #name
                line=f.readline()
                #seq
                line=f.readline()
        
                if re.search(pattern_seq, line) != None and line != '\n':
                    check_list.append(0)
                else:
                    #print('prova3')
                    check_list.append(1)
                
    elif f_type=='dot':        
        while(line):
            #seconda riga seq
            line=f.readline()
            if re.search(pattern_seq, line) != None and line != '\n':
                seq_len=len(line)
                check_list.append(0)
            else:
                #print('prova4')
                check_list.append(1)
                        
            #dot
            line=f.readline()
            if re.search(pattern_dot, line) != None and len(line)==seq_len:
                check_list.append(0)
                
            else:
                #print('prova5')
                check_list.append(1)
                
            #name
            line=f.readline()
    
    else:
        while(line):
            #seconda riga seq
            line=f.readline()
            if re.search(pattern_seq, line) != None and line != '\n':
                seq_len=len(line)
                check_list.append(0)
            else:
                #print('prova6')
                check_list.append(1)
                    
            #dot
            line=f.readline()
            
            if re.search(pattern_dot, line) != None and len(line)==seq_len:
                check_list.append(0)
            else:
                #print('prova7')
                check_list.append(1)
            
            #bear
            line=f.readline()
            if len(line)==seq_len:
                check_list.append(0)
            else:
                #print('prova8')
                check_list.append(1)
                
            #name
            line=f.readline()
else:
    #print('error')
    check_list.append(1)


#print(check_list)

if 1 in check_list:
    #print('input_error')
    o.write('input_error')
    
else:
    #print('input_ok')
    o.write('input_ok')