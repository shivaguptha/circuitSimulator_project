from operator import itemgetter
import numpy as np 

class branch:
    def __init__(self,src,dest,forced=False):
        if forced:
            self.src=src
            self.dest=dest
        else:
            self.src=min(src,dest)
            self.dest=max(src,dest)
        self.dir=(self.src,self.dest)
        self.rev_dir=(self.dest,self.src)

    def get_dir(self,loop):
        for l in loop:
            if self.dir[0]==l[0] and self.dir[1]==l[1]:
             return 1
            elif self.rev_dir[0]==l[0] and self.rev_dir[1]==l[1]:
                return -1
        return 0

    def get_other(self,node):
        if node==self.src:
            return self.dest
        elif node==self.dest:
            return self.src
        else:
             return None

    def __repr__(self):
        return str((self.src,self.dest))

    def __getitem__(self, key):
        if(key==0):
            return self.src
        if(key==1):
            return self.dest

    def __setitem__(self, key, value):
        if(key==0):
            self.src=value
        if(key==1):
            self.dest=value

    def __lt__(self, other):
     return other[0]>self[0]

    def __gt__(self, other):
     return other[0]<self[0]


class graph:
    def __init__(self):
        self.nodes=[]
        self.branches=[]
        self.matrix=None
        self.tree=None

    def generate(self,src,dest):
        if len(src)!=len(dest):
            raise Exception("Source and Destination lists do not match.")
        self.nodes=list(set.union(set(src),set(dest)))
        #creating branch instances
        for i in range(len(src)):
            self.branches.append(branch(src[i],dest[i]))
        self.branches=sorted(self.branches,key=itemgetter(0,1)) 

    def get_connections(self,node):
        #Branches connected to a particular node returned as list of branches named as connections
        connections=[]
        for b in self.branches:
            if (b.src==node) or (b.dest==node):
                connections.append(b)
        return connections

    def generate_matrix(self):
        self.matrix=np.zeros((len(self.nodes),len(self.nodes)),dtype=branch)
        for n in self.nodes: 
         for b in self.branches:
             if (b.src==n) or (b.dest==n):
                 self.matrix[b.src-1][b.dest-1]=b
        return self.matrix

    def generate_tree(self):
        if self.matrix is None:
            self.generate_matrix()
        self.tree=self.matrix[(self.matrix!=0).argmax(axis=0),range( self.matrix.shape[0] )]
        self.tree=np.delete(self.tree,0)
        self.tree=sorted(self.tree,key=itemgetter(0,1))
        return self.tree

    def maintain_tree(self,reverse=False):
        tree=dict()
        '''
        dictionary has keys as src and values as dest if reverse=False
        '''
        for b in self.tree:
            if not reverse:
             tree[b[0]]=b[1]
            else:
                tree[b[1]]=b[0]
        return tree

    def get_links(self):
        self.links= np.setdiff1d(self.branches,self.tree)
        return self.links

    def get_loops(self):
        links=self.links
        tree=self.maintain_tree(reverse=True)
        # print(tree)
        list=[]
        for l in links:
            loop=[]
            loop.append(l)
            if l[1] in tree and l[0]==tree[l[1]]:
                list.append([branch(l[1],l[0],forced=True)])
            else:
             src1=l[0]
             src2=l[1]
             while src1!=src2:
                 try:
                     temp1=tree[src1]
                 except:
                     pass
                 try:
                     temp2=tree[src2]
                 except:
                     pass
                 if(temp1!=src1):
                     loop.append(branch(temp1,src1,forced=True))
                 if(temp2!=src2):
                     loop.append(branch(src2,temp2,forced=True))
                 src1=temp1
                 src2=temp2
             loop=sorted(loop,key=itemgetter(0,1))
             list.append(loop)
        return list

