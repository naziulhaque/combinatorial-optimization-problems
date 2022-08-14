import math,random,numpy as np,time

'''
--------INPUT--------
V : number of nodes
E : number of edges
edges : 2d array providing pairs of nodes which are connected  

--------OUTPUT-------- (n:: Int, l :: list)
n : number of colors used
l : colors used for each node

'''

def cp(V,E,edges):
    
    '''uses contraint programming approach
    '''

    class NODE:
        def __init__(self,i):
            self.label=i
            self.color=0
            self.feasible=[j for j in range(V)]
            self.neighbours=[]
        def change(self):
            self.feasible.pop(0)
            self.color=self.feasible[0]

            #update all the neighbours feasibility
            for people in self.neighbours:
                nodes[people].update_feasibility(self.color)

        def update_feasibility(self,color):
            try:
                self.feasible.remove(color)
            except ValueError:
                pass
    def add_neighbours(i,j):
        nodes[i].neighbours.append(j)
        nodes[j].neighbours.append(i)

    nodes=[NODE(i) for i in range(V)]

    for edge in edges:
        n1,n2=edge
        
        if(nodes[n1].color == nodes[n2].color):
            if(nodes[n1].feasible[1]==nodes[n2].feasible[1]):
                nodes[n1].change()
                nodes[n2].update_feasibility(nodes[n1].color)
                add_neighbours(n1,n2)
            elif(nodes[n1].feasible[1] > nodes[n2].feasible[1]):
                nodes[n2].change()
                add_neighbours(n1,n2)
            else:
                nodes[n1].change()
                add_neighbours(n1,n2)

        elif(nodes[n1].color > nodes[n2].color):
            nodes[n2].update_feasibility(nodes[n1].color)
            add_neighbours(n1,n2)
        else:
            nodes[n1].update_feasibility(nodes[n2].color)
            add_neighbours(n1,n2)




    color=[nodes[i].color for i in range(V)]

    return len(set(color)),color

def greedy(V,E,edges,ordering, adj_mat=[]):
    
    '''uses greedy approach. This function is used for the following 'iterative_greedy' function 
    '''

    class NODE:
        def __init__(self,i):
            self.label=i
            self.color=0


    nodes=[NODE(i) for i in range(V)]

    nodes[ordering[0]].color=1
    m=1
    for i in range(1,len(ordering)):
        node=nodes[ordering[i]]

        n_color=[0]*(m+1)
        for n in range(V):
            if(adj_mat[n,node.label]):
                n_color[nodes[n].color]=1
        n_color.append(1)
        try:
            node.color=n_color.index(0,1,-1)
        except ValueError:
            node.color=m+1
            m+=1

    color=[nodes[i].color-1 for i in range(V)]

    return len(set(color)),color


def iterative_greedy(V,E,edges):

    '''uses iterative greedy approach
    '''

    class perm:
        def __init__(self,type):
            self.name=type
        def gen(self,adj,c=None):
            if(self.name=='welsh_powell'):  #decreasing degree
                p=[i for i in range(len(adj))]
                p=sorted(p,key=lambda x:sum(adj_mat[x]) ,reverse=True)
                return p
            if(self.name=='ColorClass_IncreasingOrder'):
                p=[i for i in range(len(adj))]
                p=sorted(p,key=lambda x:c[x])
                return p
            if(self.name=='ColorClass_IncreasingSize'):
                p=[i for i in range(len(adj))]
                s=[0]*len(set(c))
                for i in set(c):
                    s[i]=c.count(i)
                p=sorted(p,key=lambda x:c[x])
                p=sorted(p,key=lambda x:s[c[x]])
                return p
            if(self.name=='ColorClass_DecreasingSize'):
                p=[i for i in range(len(adj))]
                s=[0]*len(set(c))
                for i in set(c):
                    s[i]=c.count(i)
                p=sorted(p,key=lambda x:c[x])
                p=sorted(p,key=lambda x:s[c[x]],reverse=True)
                return p
            if(self.name=='ColorClass_IncreasingDegree'):
                p=[i for i in range(len(adj))]
                d=[0]*len(set(c))
                for v in range(len(adj)):
                    d[c[v]]+=sum(adj[v])
                p=sorted(p,key=lambda x:c[x])
                p=sorted(p,key=lambda x:d[c[x]])
                return p

            if(self.name=='ColorClass_DecreasingDegree'):
                p=[i for i in range(len(adj))]
                d=[0]*len(set(c))
                for v in range(len(adj)):
                    d[c[v]]+=sum(adj[v])
                p=sorted(p,key=lambda x:c[x])
                p=sorted(p,key=lambda x:d[c[x]],reverse=True)
                return p

            if(self.name=='ColorClass_Random'):
                p=[i for i in range(len(adj))]
                r=[i for i in range(len(set(c)))]
                random.shuffle(r)
                p=sorted(p,key=lambda x:r[c[x]])
                return p



    adj_mat=np.zeros((V,V),dtype='bool')
    for edge in edges:
            i,j=edge
            adj_mat[i,j]=1
            adj_mat[j,i]=1
    p=[perm('welsh_powell'),perm('ColorClass_DecreasingSize'), perm('ColorClass_IncreasingOrder'),perm('ColorClass_IncreasingSize'),perm('ColorClass_Random'),
        perm('ColorClass_IncreasingDegree')]

    l,color=greedy(V,E,edges,p[0].gen(adj_mat), adj_mat=adj_mat)

    if(V>600):
        n_iter=300
    else:
        n_iter=1000

    types=[1,2,3,4,5]
    w=[70,50,10,30,10]  #p[random.choices(types,weights=w)[0]].gen(adj_mat,c=color)
    for c in range(n_iter):
        l,color=greedy(V,E,edges,p[random.choices(types,weights=w)[0]].gen(adj_mat,c=color), adj_mat=adj_mat)
        
    return len(set(color)),color


def chromatic_number(V,edges):
    '''produces exact chromatic number, runs
       in exponential time.
    '''

    nodes=list(set(np.array(edges).flatten()))
    #else use the recurrence relation
    #first find a non-edge (good if they share a lot of common neighbours)
    # adj_mat=sorted(adj_mat,key=lambda  ,reverse=True)

    u,v=-1,-1
    for i in nodes:
        for j in nodes:
            if(i-j):
                if(((i,j) not in edges) and ((j,i) not in edges)):
                    u,v=i,j
                    break
    if(u==-1):    #complete graph
        return V

    #forming the contracted graph
    contracted_edges=edges.copy()
    for i in nodes:
        edge__with_u=(((i,u) in edges) or ((u,i) in edges))
        edge__with_v= (((i,v) in edges) or ((v,i) in edges))
        if(edge__with_u and edge__with_v):     #will remove u
            try:
                contracted_edges.remove((i,u))
            except ValueError:
                contracted_edges.remove((u,i))
        elif(edge__with_u and not edge__with_v):     #will remove u
            try:
                contracted_edges.remove((i,u))
                contracted_edges.append((i,v))
            except ValueError:
                contracted_edges.remove((u,i))
                contracted_edges.append((i,v))



    return min(chromatic_number(V,edges+[(u,v)]),chromatic_number(V-1,contracted_edges))


def backtracking(V,E,edges):

    def color_to_string(color):
        s='Branch: '
        for i in color[1:]:
            s=s+str(i)+'-'
        return s
    def conflict(id,c):
        if(c==m):
            return False
        flag=False
        for i in range(1,id):
            if(adj_mat[id,i]):
                if(color[i]==c):
                    flag=True
                    break
        return flag
    def pre_ordering(name):
        if(name=='maximum_mutual_friends'):
            maximum_mutual_friends=[]
            maximum_length=-1
            for f in range(V):
                mutual_friends=[f]
                for node1 in range(V):
                    if(f==node1):
                        continue
                    flag=1
                    for node2 in mutual_friends:
                        if(not adj_mat[node2+1,node1+1]):
                            flag=0
                    if(flag):
                        mutual_friends.append(node1)
                if(len(mutual_friends)>maximum_length):
                    maximum_length=len(mutual_friends)
                    maximum_mutual_friends=mutual_friends
            ordering=maximum_mutual_friends+sorted([i for i in range(V) if (i not in maximum_mutual_friends)],key=lambda x:sum(adj_mat[x+1,1:]),reverse=True)

            return ordering,maximum_length

        elif(name=='decreasing_degree'):
            ordering=[i for i in range(V)]
            ordering=sorted(ordering,key=lambda x:sum(adj_mat[x+1,1:]),reverse=True)  #decreasing degree
            return ordering,1




    #create adjacency matrix
    adj_mat=np.zeros((V+1,V+1),dtype='bool')
    for edge in edges:
        i,j=edge
        adj_mat[i+1,j+1]=1
        adj_mat[j+1,i+1]=1


    #decreasing degree ordering
    ordering,depth=pre_ordering('maximum_mutual_friends')
    _,reverse_ordering=zip(*sorted(zip(ordering,[i for i in range(V)])))

    adj_mat=np.zeros((V+1,V+1),dtype='bool')
    for edge in edges:
        i,j=edge
        i,j=reverse_ordering[i],reverse_ordering[j]
        adj_mat[i+1,j+1]=1
        adj_mat[j+1,i+1]=1

    m,color_min=greedy(V,E,edges,[i for i in range(V) ], adj_mat=adj_mat[1:,1:])

    l_min=m
    color=[-1 for i in range(V+1)]
    iter=0
    max_iter=int(5e18/V)

    #
    current_node_label=depth   #default is 0
    for i in range(depth):
        color[i+1]=i

    tic=time.time()

    while(True):
        iter+=1
        if(iter>max_iter):
            break
        current_node_label+=1
        color[current_node_label]+=1

        #while current node color is not valid increase color by 1 everytime
        while(True):
            if(conflict(current_node_label,color[current_node_label])):
                color[current_node_label]+=1
            else:
                break

        if(current_node_label==depth):   #first two nodes can be colored as-wish, so only one combination is imposed, and tree is stopped at node2 | this concept is generalized then
            if(color[current_node_label]==depth):
                break


        #pruning using l_min
        if(current_node_label>l_min):
            if(color[current_node_label]>=m):   # checking greater or equal rather previous just equality
                color[current_node_label]=-1
                current_node_label-=2
                continue
            l=len(set(color[1:current_node_label+1]))
            if(l>=l_min):
                current_node_label-=1

        if(color[current_node_label]>=m):  #all branching of that node is finished
            color[current_node_label]=-1     # checking greater or equal rather previous just equality
            current_node_label-=2
            continue

        if(current_node_label==V):
            current_node_label-=1
            l=len(set(color[1:]))
            # print(l)
            if(l<l_min):
                l_min=l
                m=l      #changing 'm'
                color_min=color[1:]
                # print('Current Min: ',l_min)


    tac=time.time()
    print('Time: ',tac-tic)
    _,color_min=zip(*sorted(zip(ordering,color_min)))

    return l_min,color_min
