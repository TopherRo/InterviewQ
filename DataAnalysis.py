#!/usr/bin/env python3

'''
Matrix will look like
PSD , Capacity , Baud , Sig Power , Ratio of C/B , Ratio of C/Sig Power

'''

import numpy as np
from enum import IntEnum

# Question 1
print("Question 1")

class Field(IntEnum):
    PSD = 0
    CAP = 1
    BAUD = 2
    SIG_P = 3
    CAP_TO_BAUD = 4
    CAP_TO_SIG_P = 5
    ROW = 6

num_of_samples = 30
max_baud = 3
max_sum_of_sig_p = 1

# Seed the rng
rng = np.random.default_rng(1620)

# Generate random uniform numbers between 0-1 to represent Power spectral density, Capacity, Baud
data_set = rng.uniform(low=0.0 , high = 1.0 , size=(num_of_samples , 3))

data_set = np.append(data_set, np.zeros((num_of_samples , 5)), axis = 1)

# Channel Power = PSD * Baud
data_set[:,Field.SIG_P] = data_set[:,Field.PSD]*data_set[:,Field.BAUD]
# Ratio of C/B = C / B
data_set[:,Field.CAP_TO_BAUD] = data_set[:,Field.CAP]/data_set[:,Field.BAUD]
# Ratio of C to Sig Power
data_set[:,Field.CAP_TO_SIG_P] = data_set[:,Field.CAP]/data_set[:,Field.SIG_P]
# Number the rows to keep track for future use
data_set[:,Field.ROW] = np.arange(0 , num_of_samples , 1 , dtype=int)

#Sort by the highest Spectral Efficiency
sorted_by_se = data_set[np.argsort(-data_set[:, Field.CAP_TO_BAUD])]
# -data_set makes this ascending order

# Sum using the spectral efficiency as a figure of merit.  
sum_of_baud = 0
sum_of_capacity = 0
sum_of_power = 0
idx = 0
bw_values_used = np.zeros(0)

for idx in range(0 , len(sorted_by_se)):
    if sum_of_baud + sorted_by_se[idx,Field.BAUD] < max_baud:
        sum_of_baud         += sorted_by_se[idx,Field.BAUD]
        sum_of_capacity     += sorted_by_se[idx,Field.CAP]
        sum_of_power        += sorted_by_se[idx,Field.SIG_P]
        bw_values_used      = np.append(bw_values_used, sorted_by_se[idx,Field.ROW])

print("Sum of the Baud" , sum_of_baud)
print("Sum of the capacity" , sum_of_capacity)
print("Sum of the Signal Power" , sum_of_power)

# Question 2
print("Question 2")

if sum_of_power < max_sum_of_sig_p:
    print('The data set is bandwidth limited so {:4.4} is the highest capacity achievable'.format(sum_of_capacity))
    exit()

# Else we need to see if it is power limited
sorted_by_power = data_set[np.argsort(-data_set[:, Field.CAP_TO_SIG_P])]

sum_of_baud = 0
sum_of_capacity = 0
sum_of_power = 0
idx = 0
power_values_used = np.zeros(0)

for idx in range(0 , len(sorted_by_power)):
    if sum_of_power + sorted_by_power[idx,Field.SIG_P] < max_sum_of_sig_p:
        sum_of_power        += sorted_by_power[idx,Field.SIG_P]
        sum_of_capacity     += sorted_by_power[idx,Field.CAP]
        sum_of_baud         += sorted_by_power[idx,Field.BAUD]
        power_values_used   = np.append(power_values_used, sorted_by_power[idx,Field.ROW])
        
print("Sum of the Baud" , sum_of_baud)
print("Sum of the capacity" , sum_of_capacity)
print("Sum of the Signal Power" , sum_of_power)

if sum_of_baud < max_baud:
    print('The data set is power limited so {:4.4} is the highest capacity achievable'.format(sum_of_capacity))
    exit()

print("We need to look deeper")

# If we reach here the opt solution is between bandwidth and power limited, we will generate another figure of merit
# based on a weighted average of the capacity to baud ratio and the capacity to power ratios.
# The weighting will be based on the 

weight1 = 1
weight2 = 0

data_set[:,7] = weight1*data_set[:,Field.CAP_TO_BAUD] + weight2*data_set[:,Field.CAP_TO_SIG_P]
sorted_by_bw_and_power = data_set[np.argsort(-data_set[:, 7])]

sum_of_baud = 0
sum_of_capacity = 0
sum_of_power = 0
idx = 0

for idx in range(0 , len(sorted_by_bw_and_power)):
    #if ((sum_of_power + sorted_by_bw_and_power[idx,Field.SIG_P]) < max_sum_of_sig_p):
    if ((sum_of_baud + sorted_by_bw_and_power[idx,Field.BAUD]) < max_baud):
        sum_of_baud         += sorted_by_bw_and_power[idx,Field.BAUD]
        sum_of_capacity     += sorted_by_bw_and_power[idx,Field.CAP]
        sum_of_power        += sorted_by_bw_and_power[idx,Field.SIG_P]
        
print("Sum of the Baud" , sum_of_baud)
print("Sum of the capacity" , sum_of_capacity)
print("Sum of the Signal Power" , sum_of_power)

#print(sorted_by_bw_and_power[:,7])
# print(data_set[:,Field.CAP_TO_BAUD])
# print(data_set[:,Field.CAP_TO_SIG_P])

# print(bw_values_used)
#print(power_values_used)
# print(np.intersect1d(bw_values_used,power_values_used))
# print(len(np.intersect1d(bw_values_used,power_values_used)))
# print(np.setxor1d(bw_values_used,power_values_used))