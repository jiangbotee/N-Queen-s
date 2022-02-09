"""
CISC352
ASSN1
N-Queens Problem

Yuhang Cao 10201134
Hongkai Chen 10179264
Bote Jiang 101296930
Yishan Li 10182827
Ruoran Liu 10191244

"""


import time
import random

# global var:
#    N, R[], p_diag[], n_diag[], p_check[], n_check[]
#    Note: The index of above lists always start with 0.

# N is the size of board

# R is the solution
# R[x] = y represents the Queen in the x-th row is at y-th row
R = []

# A list of the number of Queens in each positive diagonal
#   (index from bottom-right[0] to top-left[2N-1])
p_diag = []

# A list of the number of Queens in each negative diagonal
#   (index from bottom-left[0] to top-right[2N-1])
n_diag = []

# A list of boolean values for each positive diagonal
# p_check[x] == True -> a Queen can be inserted in x-th positive diagonal
p_check=[]

# A list of boolean values for each negative diagonal
# p_check[x] == True -> a Queen can be inserted in x-th negative diagonal
n_check=[]


# Get the number of Queens with conflicts according to board size
# Those numbers are from an short article(see Technical Document)
# :param n: the size of board
# :return: return the number of Queens with conflicts
def getConflict(n):
    if (n < 100):
        return n
    elif (n < 1000):
        return 30
    elif (n < 10000):
        return 50
    elif (n < 100000):
        return 80
    else:
        return 100


# The initialization of R with minimizing the number of Queens with conflicts
# :param N: the size of board
# :param conflictFree: the number of Queens without conflict
def initializeBoard(N,conflictFree):
    global R
    global p_diag
    global n_diag
    global p_check
    global n_check
    
    # Initialize global var
    p_diag=[]
    n_diag=[]
    p_check=[]
    n_check=[]
    R=[]
    # the remaining number of uninitialized Queens
    remain = N      
    
    # Initialize the solution by assigning i-th col to i-th row
    for i in range(N):
        R.append(i)

    # For a board of size N, each direction has 2N-1 diagonals
    for i in range (0, 2*N):
        p_diag.append(0)        # the positive diagonal
        n_diag.append(0)        # the negitive diagonal
        p_check.append(False)
        n_check.append(False)

    # Place a certain number of Queens have no conflicts
    for i in range(conflictFree):
        # randomly generate a number between 0 to N-1
        randomNum= i + random.randint(0,remain-1)
        # re-generate if it will lead to a conflict
        while (p_check[i-R[randomNum] +N-1] or n_check[i+R[randomNum]]):
            randomNum= i + random.randint(0,remain-1)
        R[i],R[randomNum] = R[randomNum],R[i]
        
        p_diag[i-R[i]+N-1] += 1     # update diagonal-related variables
        n_diag[i+R[i]] +=1
        p_check[i-R[i]+N-1] = True
        n_check[i+R[i]] = True
        remain -=1
    
    # Place the rest of Queens
    for i in range(conflictFree,N):
        remain = remain-1
        # randomly generate a number between conflictFree to N-1
        randomNum = i + random.randint(0,remain)  
        R[i],R[randomNum] = R[randomNum],R[i]
        p_diag[i-R[i]+N-1]+=1
        n_diag[i+R[i]]+=1
    return



# After the initialization, this function will pick a Queen A with conflicts
# and another Queen B may or maynot has conflicts. Swap them if the conflicts
# will reduce. Find a new B if the conflicts won't reduce. Repeating above
# steps until we find the solution. (Re-initialization if local optimal)
def findSolution():
    global N
    global R
    global p_diag
    global n_diag
    global conflictFree
    
    conflictFree = N - getConflict(N)
    initializeBoard(N,conflictFree)
    totalConflict = total_conflict(N,p_diag,n_diag)
    
    # record the number of switch actions it performed
    step = 0
    
    # min-conflict part
    while(totalConflict>0):
        temp =0
        for i in range(conflictFree,N):
            # if each diagonal contains only one Queen, then we skip
            if ((p_diag[i-R[i]+N-1]==1) and (n_diag[i+R[i]]==1)): 
                continue
            # if not, a swap will be performed in order to reduce the conflicts
            else:
                for j in range(N):
                    if (i != j):
                        # check if conflicts reduce after swapping R[i] R[j]
                        temp = diff_conflict(i,j,p_diag,n_diag,R,N)
                        if (temp < 0):      #if the conflicts reduce
                            break
                if(temp < 0):       #if the conflicts reduce
                    break
                
        # if the conflicts reduce, then swap R[i] R[j]
        if (temp < 0):
            step+=1
            # update their old diagonals 
            p_diag[i-R[i]+N-1] -= 1
            n_diag[i+R[i]] -= 1
            p_diag[j-R[j]+N-1] -= 1
            n_diag[j+R[j]] -= 1 
            
            R[i] , R[j] = R[j] , R[i]
            
            #update their new diagonals
            p_diag[i-R[i]+N-1] += 1
            n_diag[i+R[i]] += 1
            p_diag[j-R[j]+N-1] += 1
            n_diag[j+R[j]] += 1
            # update the total conflicts after swapping
            totalConflict += temp
        else:
            # if we cannot find a correct way to swap
            # (we may be stuck in the local optimal), re-initialization
            initializeBoard(N,conflictFree)


            totalConflict = total_conflict(N,p_diag,n_diag)
            


# Compute the difference of conflicts if switch row i and row j
# :param i: i-th row
# :param j: j-th row
# :param pdiag1: the positive diagonal
# :param ndiag2: the negative diagonal
# :param solution:
# :param nqueens: the size of the board
def diff_conflict(i,j,pdiag,ndiag,solution,nqueens):
    conflictDiff = 0

    # minus the number of queens conflict with (i,R[i]) before switch
    conflictDiff += 1 - pdiag[i-solution[i]+nqueens-1]
    conflictDiff += 1 - ndiag[i+solution[i]]
    # minus the number of queens conflict with (j,R[j]) before switch
    conflictDiff += 1 - pdiag[j-solution[j]+nqueens-1]
    conflictDiff += 1 - ndiag[j+solution[j]]
    # add the number of queens conflict with (j,R[i]) after switch
    conflictDiff += pdiag[j-solution[i]+nqueens-1]
    conflictDiff += ndiag[j+solution[i]]
    # add the number of queens conflict with (i,R[j]) after switch
    conflictDiff += pdiag[i-solution[j]+nqueens-1]
    conflictDiff += ndiag[i+solution[j]]

    # if row i and row j share the same diagonal
    if((i+solution[i]==j+solution[j]) or (i-solution[i]==j-solution[j])):
        conflictDiff += 2 #position i and j still conflict with each other

    # if the conflict difference<0, switch will reduce the total conflicts
    return conflictDiff


# Compute the total number of conflicts
# :param nqueens: the size of the board
# :param diag1: the first diagonal
# :param diag2: the second diagonal
def total_conflict(nqueens, diag1, diag2):
    total = 0
    for i in range(0,2*nqueens):
        # if there is more than one queen on a particular diagpnal
        if (diag1[i] > 1):
            total += diag1[i]*(diag1[i]-1)/2
        if (diag2[i] > 1):
            total += diag2[i] *(diag2[i]-1)/2
    return total


# Helper function of qualify()
# Return the index for the positive diagonal
def getP(row,col):
    return row-col+N-1


# Helper function of qualify()
# Return the index for the negative diagonal
def getN(row,col):
    return row+col



def main():
    global N        # the queen size
    global R        # the solution
    startTime = time.clock()
    theFile = open("nqueens.txt", "r")
    theInts = []    # a list of input N
    for val in theFile.read().split():
        theInts.append(int(val))
    print(theInts)
    fo=open("nqueens_out.txt","w")
    for i in theInts:
        N=i
        findSolution()
        print("computing finished! Size is", N)
        print("--- %s seconds ---" % (time.clock()-startTime))
        astring = "size is " + str(N) + ", solution is " + str([x+1 for x in R])
        fo.write(astring)
        fo.write("\n")
    fo.close()
    print("OVER!")

main()

    
