''' 
   
   >>> fact(3)
   2
   >>> gamma(1, 1e-4)[3] - 1 <= 0.0001
   True
   >>> gamma(4, 1e-4)[3] - 6 <= 0.0001
   True
   >>> gamma(1.5, 1e-4)[3] - 0.8862 <= 0.0001
   True
   >>> gamma(2.5, 1e-4)[3] - 1.3293 <= 0.0001
   True

   To run dockets in verbose mode:

   python -m doctest -v gamma.py
   
   Call signature: 

   python gamma.py -t 4. -p 1e-4
   
'''

import math
import pdb

def fact(t):
    #pdb.set_trace()
    g = 1
    for i in range(1, int(t)):
        g *= i
    return g 
      

def gamma(t, p): # p stands for fract_diff
    #pdb.set_trace()   
    dx = 2
    previous_ans = 0 
    current_ans = 1
    while abs((current_ans-previous_ans)/current_ans) >= p :
        gx = 0
        dx = dx/2.
        steps = 1000/dx
        #pdb.set_trace()
        for x in range(1, int(steps)+1):
            gx += ((x*dx)**(t-1))*math.exp(-x*dx)*dx
        
        previous_ans = current_ans
        current_ans = gx
        frac_diff = str('{:.7f}'.format((current_ans-previous_ans)*100/current_ans))+'%'
        
    return 'gamma', t, 'is', gx, 'frac_diff:', frac_diff
    

if __name__=="__main__":
    import doctest
    #doctest.testmod()
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type = float)
    parser.add_argument('-p', type = float)
    args = parser.parse_args()
    a = args.t 
    e = args.p 
    
    if a >= 1 and a <= 100:
    	if a % 1 == 0:
        	print fact(a)
    	else:
        	print gamma(a, e)
    
    else:
        print 'The value of t should be within 1 and 100'
        


    