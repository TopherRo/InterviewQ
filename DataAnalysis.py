#!/usr/bin/env python3

'''
python3 --version Python 3.8.10
The data Matrix will look like
PSD , Capacity , Baud , Sig Power , Ratio of C/B , Ratio of C/Sig Power, Row numbers, Q2 Cost
To optimize for spectral efficency we will sort the dataset by highest capacity to baud ratio.
We then add as many high spectral efficiency channels as we can while maintaining the total BW constraint.
If we include a signal power constrain this problem becomes much more difficult.
My approach has been to use both the spectral efficiency and the capacity to signal power ratio as weighted
imputs to some sort of cost function and then apply the same algorithm.
Calculating this cost function is not straightforward.
Determining whether a data set is more power limited or bandwidth limited allows us to adjust the weights 
however the two costing functions have different scales as one is based on random variable X over random 
variable Y (X/Y), while the other is X over Z times K, (X/(Z*K)) giving them much differnet scales.   

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
    COST = 7

num_of_samples = 1000
max_baud = 10
max_sum_of_sig_p = 5

# Seed the rng
rng = np.random.default_rng(1625)

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

print("The data set is neither bw or power limited so we need to find a combination of channels \
that satisfy both constraints")

# If we reach here the opt solution is between bandwidth and power limited, we will generate another figure of merit
# based on a weighted average of the capacity to baud ratio and the capacity to power ratios.
# The weighting will be based on ----

weight1 = 250
weight2 = 1

data_set[:,Field.COST] = weight1*data_set[:,Field.CAP_TO_BAUD] + weight2*data_set[:,Field.CAP_TO_SIG_P]
sorted_by_bw_and_power = data_set[np.argsort(-data_set[:, Field.COST])]

sum_of_baud = 0
sum_of_capacity = 0
sum_of_power = 0
idx = 0

for idx in range(0 , len(sorted_by_bw_and_power)):
    if ((sum_of_power + sorted_by_bw_and_power[idx,Field.SIG_P]) < max_sum_of_sig_p) and \
        ((sum_of_baud + sorted_by_bw_and_power[idx,Field.BAUD]) < max_baud):
        sum_of_baud         += sorted_by_bw_and_power[idx,Field.BAUD]
        sum_of_capacity     += sorted_by_bw_and_power[idx,Field.CAP]
        sum_of_power        += sorted_by_bw_and_power[idx,Field.SIG_P]
        
print("Sum of the Baud" , sum_of_baud)
print("Sum of the capacity" , sum_of_capacity)
print("Sum of the Signal Power" , sum_of_power)

'''
Question 1
Sum of the Baud 9.997675832267873
Sum of the capacity 77.70174600489302
Sum of the Signal Power 5.478780377417459
Question 2
Sum of the Baud 47.01731348766844
Sum of the capacity 110.79939280067428
Sum of the Signal Power 4.99942971054424
The data set is neither bw or power limited so we need to find a combination of channels that satisfy both constraints
Sum of the Baud 9.994045562154223
Sum of the capacity 71.96643516675702
Sum of the Signal Power 4.559695152113895
'''
