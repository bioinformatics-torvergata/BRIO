import sys

f_bench=sys.argv[1]
f_seq=sys.argv[2]
out_f=sys.argv[3]

def Search_nucleotide(file_bench, file_seq, out_file):
    o=open(out_file, "w")
    f=open(file_bench)
    line=f.readline()
    pssm=[]
    while(line):
        if line=="#PSSM\n":
            pssm.append(line.split())
            while (line[0:6] != "#score"):
                line=f.readline()
                pssm.append(line.split())

        line=f.readline()

    pssm[1:-2]

    d={}
    c=0

    for el in pssm[1:-2]:
        d[c]={'A':0.0, 'C':0.0, 'U':0.0, 'G':0.0}
        for i in range(0, len(el), 3):

            d[c][el[i]] = el[i+2]

        c+=1
    m=[el[0] for el in pssm[1:-2]]
    motif=''.join(m)

    f_in=open(file_seq)
    line=f_in.readline()
    while(line):
        o.write(line[:-1].strip()+"\t")
        line=f_in.readline()
        seq=line
        line=f_in.readline()
        line=f_in.readline()
        line=f_in.readline()
        
        
        
        m_l=len(motif.strip())
        c=0
        score=-10000000.0
        start_pos=0


        for i in range(c, len(seq.strip())):
            subseq=seq[c:c+m_l].strip()
            score_provv=0
            if len(subseq)==m_l: 
                #print(subseq, len(subseq), m_l)
                for k, nt in enumerate(subseq):
                    for nuc in d[k].keys():
                        if nt.upper()!=nuc.upper():
                            score_provv+=float(d[k][nuc])*-2
                        else:
                            score_provv+=float(d[k][nuc])*3

                if score_provv>=score:
                    score=score_provv
                    start_pos=i

            c+=1

        
        o.write(seq[start_pos:start_pos+m_l].strip()+"\t")
        o.write(str(score)+"\t")
        o.write(str(len(seq))+"\t")
        o.write(str(start_pos)+"\t")
        o.write(str(start_pos+m_l)+"\n")
    o.close()
    
    
Search_nucleotide(f_bench, f_seq, out_f)
