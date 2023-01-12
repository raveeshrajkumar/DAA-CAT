import os
import re
import sys
import time
from pandas import *


#Initialization
seqA = 'TTAGTAGCTATCGA'
seqB = 'TAGCTTATCTTAGC'

match = 3
mismatch = -1
 



def main():  
    
    print('The substitution matrix for the alphabet {0} is:'.format(alphabet))
    Substi = create_Substi(alphabet, match, mismatch)
    print(DataFrame(Substi))
    
    rows = len(seqA) + 1
    cols = len(seqB) + 1
    
    score_matrix, start_pos, max_score, path_matrix = create_score_matrix(rows, cols)  
                                                                
    print('Scoring Matrix : \n')
    print_matrix(score_matrix)         
    print('Highest score = ', max_score)
    print('start_pos=',start_pos)
    print('The path to 0 is:')
    time.sleep(0.5)
     
    seqA_aligned, seqB_aligned = traceback(path_matrix, start_pos, score_matrix)
    assert len(seqA_aligned) == len(seqB_aligned), 'aligned strings are not the same size'
    
    Graphical_display(seqA_aligned, seqB_aligned)
    print('Score of the alignment = ')
    print(max_score)
    return(0)

def traceback(path_matrix, start_pos, score_matrix):

    x,y = start_pos
    aligned_seqA = []
    aligned_seqB = []
    
    
    while path_matrix[x][y] != [0, 'NULL'] :
        d, direction = path_matrix[x][y][0], path_matrix[x][y][1]
        if direction == 'DIAG' :
            assert d ==1, 'path_matrix wrongly constructed !'
            aligned_seqA.append(seqA[x - 1])     
            aligned_seqB.append(seqB[y - 1])
            x -= 1
            y -= 1
            print('DIAG',score_matrix[x][y])
        elif direction == 'UP' : 
            for c in range(d):
                aligned_seqA.append(seqA[x - 1])
                aligned_seqB.append('-')             
                x -= 1
                print('UP',score_matrix[x][y])
        elif direction == 'LEFT' :
            for c in range(d):
                aligned_seqA.append('-')            
                aligned_seqB.append(seqB[y - 1])
                y -= 1
                print('LEFT',score_matrix[x][y])
    print('Traceback reached a 0 at :',(x,y))
    
    return ''.join(reversed(aligned_seqA)), ''.join(reversed(aligned_seqB))

def create_score_matrix(rows, cols):
    '''The function creates the score_matrix and the path_matrix'''
    score_matrix = [[0 for col in range(cols)] for row in range(rows)]
    path_matrix = [[[0 , 'NULL'] for col in range(cols)] for row in range(rows)]  
    
    max_score = 0
    max_pos   = None    
    for i in range(1, rows): 
        for j in range(1, cols):
            score, antecedent = calc_score(score_matrix, i, j)
            if score > max_score:                  
                max_score = score
                max_pos   = (i, j)

            score_matrix[i][j],path_matrix[i][j] = score, antecedent           

    assert max_pos is not None, 'No maximum found'

    return score_matrix, max_pos, max_score, path_matrix   



def alignment_string(aligned_seqA, aligned_seqB): 

    idents, gaps, mismatches = 0, 0, 0
    alignment_string = []                           
    for base1, base2 in zip(aligned_seqA, aligned_seqB):
        if base1 == base2:
            alignment_string.append('|')
            idents += 1
        elif '-' in (base1, base2):
            alignment_string.append(' ')
            gaps += 1
        else:
            alignment_string.append(':')
            mismatches += 1

    return ''.join(alignment_string), idents, gaps, mismatches

def print_matrix(matrix): 
    print('\n'.join([''.join(['     {:4}'.format(item) for item in row])for row in matrix]))
    
if __name__ == '__main__':
    sys.exit(main())