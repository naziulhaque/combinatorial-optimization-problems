import math,numpy as np

'''
--------Inputs-----------
K : capacity of the knapsack
v : the 'value' of the items 
w : the 'weight' of the items  

--------Output-----------
The output format is (n :: int, l :: list)
n : total value of the items selected
l : list containing 0 and 1. 0 means the corresponding item is not selected. 
'''

def knapsack_greedy(K,v,w):

# This function solves knapsack problem using greedy approach. This function runs very fast, but obtained result is far from optimum. 

    v,w=np.array(v,dtype=int),np.array(w,dtype=int)
    # v=np.array([3, 4, 4, 10, 4])
    # w=np.array([3, 4, 5, 9, 4])
    # K=11
    value_density=v/w
    index=[i for i in range(len(v))]
    value_density,index=zip(*sorted(zip(value_density,index),reverse=True))

    value_density=np.zeros(len(v),dtype=int)
    total_value=0
    total_weight=0

    for i in range(len(v)):
        if(w[index[i]])>(K-total_weight):
            continue
        else:
            total_value+=v[index[i]]
            value_density[index[i]]=1
            total_weight+=w[index[i]]
    return total_value,list(value_density)

# The following functions solve knapsack using 'backtracking' technique, which gives much better result than greedy algorithm

def upper_bound(j,residual_cap,v,w):  
    s=0
    ub=0
    n=len(v)-1
    while(s<=residual_cap):
        s+=w[j]
        ub+=v[j]
        j+=1
    if(j<= n-1):
        ub=ub-v[j]+(residual_cap-s+w[j])*v[j]/w[j]
    else:
        ub=sum([v[i] for i in range(j,n)])

    return int(ub)

def backtrack_i(j,current_x): 
    j-=1
    while(j>=0):
        if(current_x[j]):
            break
        j-=1
    return j


def knapsack_backtrack(K,v,w):
    v,w=np.array(v,dtype=int),np.array(w)
    n_item=v.shape[0]

    greedy_opt,_=knapsack_greedy(K,v,w)
    best_opt=upper_bound(0,K,v,w)

    #sorting according to density
    
    value_density=v/w
    index=[i for i in range(len(v))]
    _,index=zip(*sorted(zip(value_density,index),reverse=True))
    v=[v[i] for i in index]
    w=[w[i] for i in index]


    current_x=[0]*n_item
    optimal_x=[0]*n_item
    residual_cap=K
    current_profit=0
    optimal_profit=0
    v.append(0)
    w.append(math.inf)
    j=0

    while(True):
        while(j<=(n_item-1)):
            while(w[j]<=residual_cap):
                residual_cap-=w[j]
                current_profit+=v[j]
                current_x[j]=1
                j+=1
            if(j<(n_item-1)):
                current_x[j]=0
                j+=1
            if(j<(n_item-1)):
                u=upper_bound(j,residual_cap,v,w)
                while(optimal_profit >=current_profit+ u):
                    i=backtrack_i(j,current_x)
                    if(i<0):
                        _,optimal_x=zip(*sorted(zip(index,optimal_x)))
                        return optimal_profit,optimal_x
                    else:
                        residual_cap+=w[i]
                        current_profit-=v[i]
                        current_x[i]=0
                        j=i+1
                        u=upper_bound(j,residual_cap,v,w)
            if(j==(n_item-1)):
                break


        if(current_profit>optimal_profit):
            optimal_profit=current_profit
            optimal_x=current_x[:]
            j=n_item-1
            if(current_x[j]):
                residual_cap+=w[j]
                current_profit-=v[j]
                current_x[j]=0


        while(True):
            i=backtrack_i(j,current_x)
            if(i<0):
                _,optimal_x=zip(*sorted(zip(index,optimal_x)))
                return optimal_profit,optimal_x
            else:
                residual_cap+=w[i]
                current_profit-=v[i]
                current_x[i]=0
                j=i+1
                u=upper_bound(j,residual_cap,v,w)
                if(not(optimal_profit >= current_profit+ u)):
                    break
