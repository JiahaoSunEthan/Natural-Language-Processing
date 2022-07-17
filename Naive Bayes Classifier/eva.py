# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 17:33:35 2022

@author: 13451
"""


eva = dict()
fr = open('nboutput.txt', "r")
while 1:
    line = fr.readline()
    if not line:
        break
    line = line.split(' ')
    label_a = line[0]
    label_b = line[1]
    true_label_a = line[2].split('\\')[2].split('_')[0]
    true_label_b = line[2].split('\\')[1].split('_')[0]
    if label_a!=true_label_a or label_b!=true_label_b:
        eva.setdefault((true_label_a,true_label_b),0)
        eva[(true_label_a,true_label_b)] +=1
    