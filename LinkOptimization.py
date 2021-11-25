#!/usr/bin/env python3

'''
python3 --version Python 3.8.10
Q1
NSR = NSR non linear + NSR ASE
NSR = B*(Pin**2) + A/Pout
Pout = 1/L * Pin where L is the Loss
NSR = B*(Pin**2) + A*L/Pin
Max/Min Problem
(d/dPin)(NSR) = 2*B*Pin - A*L/Pin**2 = 0
Pin**3 = A*L / 2*B
Pin_opt = (A*L / 2*B)**(1/3)

Q2
G should be used to set Pin2 to the optimized Pin for the second span.
Pin1 should be selected solely based on the performance of the first span.

'''

import numpy as np
import matplotlib.pyplot as plt

# Q1, Sanity check to make sure the answer to Q1 makes sense
print("Question 1")

A = 0.1
B = 0.02
L = 100

Pin_opt = (( A*L / ( 2*B ))**( 1/3 ))
print("The optimal Pin is" , Pin_opt)

NSR_opt = B*(Pin_opt**2) + A*L/(Pin_opt)
print("The NSR is" , NSR_opt)

Pin = np.arange(1 , 10 , 0.01)

NSR = B*(Pin**2) + A*L/(Pin)

plt.figure(1)
plt.plot( Pin , NSR )
plt.xlabel("Pin"), plt.ylabel("NSR")
plt.title("NSR vs Pin")
plt.show(block=False)

# Q2
print("Question 2")

A = 0.1
B = 0.02
L1 = 100
L2 = 200

Pin1_opt = ( ( A*L1 / (2*B) )**(1/3))
Pin2_opt = ( ( A*L2 / (2*B) )**(1/3))
print ("Pin1 and Pin2 are" , Pin1_opt , Pin2_opt)

G = L1*(Pin2_opt/Pin1_opt)
print("The Gain is" , G)

NSR_opt = B*(Pin1_opt**2) + A*L1/(Pin1_opt) + B*(Pin2_opt**2) + A*L2/(Pin2_opt)
print("The resulting NSR is" , NSR_opt)

Pin1 = np.arange(1 , 10 , 0.01)
Pin2 = G*Pin1/L1

NSR1 = B*(Pin1**2) + A*L1/(Pin1)
NSR2 = B*(Pin2**2) + A*L2/(Pin2)

NSR = B*(Pin1**2) + A*L1/(Pin1) + B*(Pin2**2) + A*L2/(Pin2)

plt.figure(2)
plt.plot( Pin1 , NSR1, label="Pin1")
plt.plot( Pin2 , NSR2, label="Pin2")
plt.legend(loc="upper right")
plt.xlabel("Pin"), plt.ylabel("NSR")
plt.title("NSR vs Pin")
plt.show()

'''
Output
Question 1
The optimal Pin is 6.299605249474365
The NSR is 2.381101577952299
Question 2
Pin1 and Pin2 are 6.299605249474365 7.937005259840997
The Gain is 125.99210498948732
The resulting NSR is 6.160864727636918
'''