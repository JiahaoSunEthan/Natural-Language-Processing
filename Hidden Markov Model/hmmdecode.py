# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 22:32:34 2022

@author: 13451
"""


import sys
import copy
from math import log10

file_path = sys.argv[1]
f1 = open(file_path,encoding = 'utf_8',mode='r')
lines = f1.readlines()
f1.close()

#extract model parameter
f2 = open('hmmmodel.txt',encoding = 'utf_8',mode = 'r')
line = f2.readline()
#initialize matrix
trans_matrix = dict()
em_matrix = dict()
ini_dis_matrix = dict()
#loading parameter line by line
while not line.startswith('Emission'):
    if not line.startswith('Transition') and not line.startswith('From') and line!= '\n':
        from_state,to_state,prob = line.split(',')[0].strip(),line.split(',')[1].strip(),float(line.split(',')[2].strip())
        trans_matrix.setdefault(from_state,dict())
        trans_matrix[from_state][to_state] = prob
    line = f2.readline()

while not line.startswith('Initial'):
    if not line.startswith('Emission') and not line.startswith('State') and line!= '\n':
        state,obs,prob = line.split(', ')[0].strip(),line.split(', ')[1].strip(),float(line.split(', ')[2].strip())
        em_matrix.setdefault(state,dict())
        em_matrix[state][obs] = prob
    line = f2.readline()

while line:
    if not line.startswith('Initial') and not line.startswith('State') and line!= '\n':
        state,prob = line.split(',')[0].strip(),float(line.split(',')[1].strip())
        ini_dis_matrix[state] = prob
    line = f2.readline()
f2.close()

#construct word set & state set & high frequency open class set
word_set = set()
for key in em_matrix.keys():
    for key2 in em_matrix[key].keys():
        word_set.add(key2)
        
state_set = set(trans_matrix.keys())

frequency_sort = []
for key in em_matrix.keys():
    frequency_sort.append((key,len(em_matrix[key])))
frequency_sort.sort(key = lambda x:x[1],reverse = True)
open_class_set = set()
for i in range(3):
    open_class_set.add(frequency_sort[i][0])
    
    
'''
#viterbi decode without log
def viterbi(line):
    line = line.strip() #remove \n
    prob_map = dict()
    back_map = dict() #overwrite during iteration
    next_level_back_map = dict()
    T = 1
    for word in line.split(' '):
        if len(prob_map) == 0: #initial state 
            if word in word_set:
                for state in ini_dis_matrix.keys():
                    if word in em_matrix[state]:
                        prob = ini_dis_matrix[state] * em_matrix[state][word]
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = prob
                        back_map[state] = [state]
            else: # unseen word, ignore emission matrix, choose from open class set
                for state in ini_dis_matrix.keys():
                    if state in open_class_set:
                        prob = ini_dis_matrix[state]
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = prob
                        back_map[state] = [state]
        else:
            if word in word_set:
                for state in state_set:
                    if word in em_matrix[state]:
                        max_prob, max_pre_state = 0, None  #choose max prob from pre_state
                        for pre_state in prob_map[T-1].keys():
                            prob = prob_map[T-1][pre_state] * trans_matrix[pre_state][state] * em_matrix[state][word]
                            if prob > max_prob:
                                max_prob = prob
                                max_pre_state = pre_state
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = max_prob
                        new = copy.deepcopy(back_map[max_pre_state])
                        new.append(state)
                        next_level_back_map[state] = new
            else: # unseen word, ignore emission matrix, choose from open class set
                for state in open_class_set:
                    max_prob, max_pre_state = 0, None  #choose max prob from pre_state
                    for pre_state in prob_map[T-1].keys():
                        prob = prob_map[T-1][pre_state] * trans_matrix[pre_state][state]
                        if prob > max_prob:
                            max_prob = prob
                            max_pre_state = pre_state
                    prob_map.setdefault(T,dict())
                    prob_map[T][state] = max_prob
                    new = copy.deepcopy(back_map[max_pre_state])
                    new.append(state)
                    next_level_back_map[state] = new
            back_map = next_level_back_map
            next_level_back_map = dict()
            
        T += 1
    
    global_max = 0
    global_max_final_state = None
    for final_state in prob_map[T-1].keys():
        if prob_map[T-1][final_state] > global_max:
            global_max = prob_map[T-1][final_state]
            global_max_final_state = final_state
    return back_map[global_max_final_state]   
'''



#viterbi decode
def viterbi(line):
    line = line.strip() #remove \n
    prob_map = dict()
    back_map = dict() #overwrite during iteration
    next_level_back_map = dict()
    T = 1
    for word in line.split(' '):
        word = word.lower()
        if len(prob_map) == 0: #initial state 
            if word in word_set:
                for state in ini_dis_matrix.keys():
                    if word in em_matrix[state]:
                        prob = log10(ini_dis_matrix[state] * em_matrix[state][word])
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = prob
                        back_map[state] = [state]
            else: # unseen word, ignore emission matrix, choose from open class set
                for state in ini_dis_matrix.keys():
                    if state in open_class_set:
                        prob = log10(ini_dis_matrix[state])
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = prob
                        back_map[state] = [state]
        else:
            if word in word_set:
                for state in state_set:
                    if word in em_matrix[state]:
                        max_prob, max_pre_state = -float('inf'), None  #choose max prob from pre_state
                        for pre_state in prob_map[T-1].keys():
                            prob = prob_map[T-1][pre_state] + log10(trans_matrix[pre_state][state]) +log10(em_matrix[state][word])
                            if prob > max_prob:
                                max_prob = prob
                                max_pre_state = pre_state
                        prob_map.setdefault(T,dict())
                        prob_map[T][state] = max_prob
                        new = copy.deepcopy(back_map[max_pre_state])
                        new.append(state)
                        next_level_back_map[state] = new
            else: # unseen word, ignore emission matrix, choose from open class set
                for state in open_class_set:
                    max_prob, max_pre_state = -float('inf'), None  #choose max prob from pre_state
                    for pre_state in prob_map[T-1].keys():
                        prob = prob_map[T-1][pre_state] + log10(trans_matrix[pre_state][state])
                        if prob > max_prob:
                            max_prob = prob
                            max_pre_state = pre_state
                    prob_map.setdefault(T,dict())
                    prob_map[T][state] = max_prob
                    new = copy.deepcopy(back_map[max_pre_state])
                    new.append(state)
                    next_level_back_map[state] = new
            back_map = next_level_back_map
            next_level_back_map = dict()
            
        T += 1
    
    global_max = -float('inf')
    global_max_final_state = None
    for final_state in prob_map[T-1].keys():
        if prob_map[T-1][final_state] > global_max:
            global_max = prob_map[T-1][final_state]
            global_max_final_state = final_state
    return back_map[global_max_final_state]

#apply viterbi & output
fw = open('hmmoutput.txt',encoding = 'utf_8',mode = "w")
for line in lines:
    res = viterbi(line) 
    txt = line.strip().split(' ')
    output = ' '.join([txt[i]+'/'+res[i] for i in range(len(txt))])
    fw.write(output+'\n')
fw.close()

    