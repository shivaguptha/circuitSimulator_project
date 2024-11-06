import numpy as np
import sympy as sp
from calc import calculate,matrices
from graph import graph,branch 
from utils.laplace import LT
from utils.utils import reorder,get_args,from_txt

np.set_printoptions(linewidth=np.inf)

def run_solver(filename):
 t=sp.Symbol('t')
 s=sp.Symbol('s')

 R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list=from_txt(filename)
 g=graph()
 g.generate(branch_src_list,branch_dest_list)
 g.generate_matrix()
 t=g.generate_tree()
 l=g.get_links()
 loops=g.get_loops()
 R_list,L_list,C_list,V_list,I_list=reorder(g,R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list)
 R_LT,C_LT,L_LT,V_LT,I_LT=LT(R_list,C_list,L_list,V_list,I_list,branch_src_list,branch_dest_list)
 B_f,Q_f,Z,Y=matrices(t,loops,R_LT,C_LT,L_LT)
 V,I=calculate(B_f,Q_f,Z,Y,V_LT,I_LT,len(g.tree))
 return V,I

if __name__=="__main__":
    args = get_args()
    V,I=run_solver(r"D:\3rd sem\EE_204\Circuit-Solver-main\input\test_data.txt")
    print(V)
    
