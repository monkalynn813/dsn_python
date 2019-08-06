#!/usr/bin/env python3

def find_wire(file_path):
    if not file_path.endswith('.ses'):
        file_path+='.ses'
    ses=open(file_path,'r').read().splitlines()
    pathsec_list=[]
    for i in range(len(ses)):
        if 'path' in ses[i]:
            for j in range(i,len(ses)):
                if ')' in ses[j]:
                    pathsec=[i,j]
                    pathsec_list.append(pathsec)
                    break
    path_list=[]
    for sec_bry in pathsec_list:
        onepath=[]
        for j in range(sec_bry[0]+1,sec_bry[1]):
            pts_str=ses[j].split()
            ptstart=int(pts_str[0])
            ptend=int(pts_str[1])
            pts=[ptstart,ptend]
            onepath.append(pts)
        path_list.append(onepath)
    return path_list