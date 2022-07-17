# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 17:14:41 2022

@author: 13451
"""



import sys

file_path = sys.argv[1]
f = open(file_path,encoding = 'utf_8',mode='r')
lines = f.readlines()
f.close()

#initialize matrix
trans_matrix = dict()
em_matrix = dict()
ini_dis_matrix = dict()

def extract(s):
    i = len(s)-1
    while s[i]!= '/':
        i -= 1
    return (s[:i].strip().lower(),s[i+1:].strip())
    
def processline(line):
    global trans_matrix
    global em_matrix
    global ini_dis_matrix
    
    content = line.strip().split(' ') #remove \n
    i = 0
    cur_word,cur_tag = None,None
    while i < len(content)-1:
        if cur_word == None:
            cur_word,cur_tag = extract(content[i])
        
        if i == 0:
            ini_dis_matrix.setdefault(cur_tag,0)
            ini_dis_matrix[cur_tag] += 1
        
        em_matrix.setdefault(cur_tag,dict())
        em_matrix[cur_tag].setdefault(cur_word,0)
        em_matrix[cur_tag][cur_word] += 1
        
        next_word,next_tag = extract(content[i+1])
        trans_matrix.setdefault(cur_tag,dict())
        trans_matrix[cur_tag].setdefault(next_tag,0)
        trans_matrix[cur_tag][next_tag] += 1
        
        if i+1 == len(content)-1:
            em_matrix.setdefault(next_tag,dict())
            em_matrix[next_tag].setdefault(next_word,0)
            em_matrix[next_tag][next_word] += 1
        
        cur_word,cur_tag = next_word,next_tag
        i += 1

for line in lines:
    processline(line)

#add one smoothing for transmission matrix
state_set = set(trans_matrix.keys())
for key in trans_matrix.keys():
    for state in state_set:
        if state not in trans_matrix[key]:
            trans_matrix[key][state] = 1


#process raw martix to probablity distribution
total = 0
for key in ini_dis_matrix.keys():
    total += ini_dis_matrix[key]

for key in ini_dis_matrix.keys():
    ini_dis_matrix[key] /= total

for key in trans_matrix.keys():
    total = 0 
    for key2 in trans_matrix[key].keys():
        total += trans_matrix[key][key2]
    for key2 in trans_matrix[key].keys():
        trans_matrix[key][key2] /= total

for key in em_matrix.keys():
    total = 0 
    for key2 in em_matrix[key].keys():
        total += em_matrix[key][key2]
    for key2 in em_matrix[key].keys():
        em_matrix[key][key2] /= total


#output model file
fw = open('hmmmodel.txt',encoding = 'utf_8',mode = "w")
fw.write("Transition Matrix\n")
fw.write("From, To, Probability\n")
for key in trans_matrix.keys():
    for key2 in trans_matrix[key].keys():
        fw.write(key+', '+key2+', '+str(trans_matrix[key][key2])+'\n')
fw.write('\n')

fw.write("Emission Matrix\n")
fw.write("State, Obs, Probability\n")
for key in em_matrix.keys():
    for key2 in em_matrix[key].keys():
        fw.write(key+', '+key2+', '+str(em_matrix[key][key2])+'\n')
fw.write("\n")

fw.write("Initial Probability Distribution\n")
fw.write('State, Probability\n')
for key in ini_dis_matrix.keys():
    fw.write(key+', '+str(ini_dis_matrix[key])+'\n')
fw.close()

    

