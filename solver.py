from sudokuset import SudokuSet

# hard, KC Star 3/12
hard = [
           [3,0,4,0,0,0,0,0,0],
           [2,0,0,0,9,3,0,0,0],
           [0,6,0,1,2,0,3,0,0],
           [4,0,0,0,8,9,7,0,6],
           [0,0,0,0,1,0,0,0,0],
           [9,0,1,0,3,0,0,0,4],
           [0,0,7,0,6,8,0,9,0],
           [0,0,0,9,4,0,0,0,3],
           [0,0,0,0,0,0,6,0,2]
        ]

# easy, http://www.websudoku.com/
easy = [
           [2,0,7,0,5,6,8,0,0],
           [8,9,0,0,4,0,2,0,6],
           [6,0,0,7,0,8,0,0,5],
           [1,0,0,0,0,9,0,0,4],
           [9,0,0,0,6,0,0,0,1],
           [5,0,0,1,0,0,0,0,7],
           [0,0,0,6,0,4,0,0,8],
           [4,0,1,0,8,0,0,3,9],
           [0,0,8,5,9,0,1,0,2]
        ]

solution = hard

 
# one-dimensional array of SudokySet's
workset = [SudokuSet(solution[j][i]) for j in range(9) for i in range(9)]

def printWorkset(s, w):
    print('===== {} ====='.format(s))
    for i in range(81):
        if i%9==0:
            print()
        x = w[i]
#         if 1 == len(x):
#             for y in x:
#                 print('    {}     '.format(y), end="")
#                 break;
#         else:
#             print('- ', end="")
        for a in range(1,10):
            if a in x:
                print('{}'.format(a), end="")
            else:
                print('-', end="")
        print(' ', end="")
#             print(x, end="")
    print()
    
def get_row(m, i):
    ''' Returns array of 9 SudokuSets. '''
    return m[i*9:i*9+9]

def get_col(m, i):
    ''' Returns array of 9 SudokuSets. '''
    result = []
    for j in range(9):
        result.append(m[j*9+i])
    return result

def get_box(m, bi):
    '''
    Returns array of 9 SudokuSets.
    
    0 1 2
    3 4 5
    6 7 8
    x offset = (i%3)*3
    y offset = int(i/3)  # possible values are 0,1,2
    m[0] => (0-2)+0 + (0-2)+9 + (0-2)+18
    m[2] => (0-2)+6+(0*9) + (0-2)+6+9 + (0-2)+6+18
    m[4] => (0-2)+0 + (0-2)+9 + (0-2)+18
    m[i] => 
    '''
    result = []
    xoff =  (bi%3)*3
    yoff = int(bi/3)  # possible values are 0,1,2
    
    # 1st box row
#     print('first box row')
    for i in range(xoff + yoff*27, xoff + yoff*27 +3):
        result.append(m[i])
#         print(m[i])
    
    # 2nd box row
#     print('second box row')
    for i in range(xoff + yoff*27+9, xoff + yoff*27+9 +3):
        result.append(m[i])
#         print(m[i])
    
    # 3rd box row
#     print('third box row')
    for i in range(xoff + yoff*27+18, xoff + yoff*27+18 +3):
        result.append(m[i])
#         print(m[i])
        
    return result

def get_knowns(a):
    result = set()
    for i in a:
        if 1 == len(i):
            for x in i:
                result.add(x)
                break;
    return result
    
def remove_knowns(a):
    removes = get_knowns(a)
    for j in a:
        if 1 < len(j):
            j.discard(removes)

def do_uniques(a):
    for i in range(9):
        cell = a[i]
        if 1 == len(cell):
            continue  # remove_knowns has or will take care of this case (the case where there are more of this value in the array) 
        c = set();
        
        # copy the set, sub everything else from it.  If we have one value left, it was unique
        for z in cell:  # HACK: cell.copy() throwing fits
            c.add(z)

        for j in range(9):
            if j == i:
                continue  # skip self
            c -= a[j]
            
        if 1 == len(c):  # 
            a[i] &= c

def do_exclusive_pairs(a):
    # Look for pairs of pairs.  When found, the pair can be discarded from
    # all other cells in this array.
    pairs = {}  # lo : hi
    for i in range(9):
        s = a[i]
        if len(s) == 2:
            lo = 9
            hi = 0
            for x in s:
                lo = min(lo, x)
                hi = max(hi, x)
            if lo in pairs.keys() and pairs[lo] == hi:
                # we have a paired pair!
                for j in range(9):
                    if 2 < len(a[j]) or (lo not in a[j] and hi not in a[j]) :  # Original logic, fails (issue with SudokuSet/set): when pair s ORed with a[j] has 3+ elements, remove pair s from it
                        a[j].discard(s)
            else:
                pairs[lo] = hi  

def makekey(s):
    ''' Returns string from set of ints, ordered low to high.
    Example: if set is (5,2,6), result will be '256'. '''
    so = sorted(s)
    s=''
    for x in so:
        s+=str(x)
    return s
    
def do_exclusive_trips(a):
    # Look for triplets of triplets.  When found, the triplet can be discarded from
    # all other cells in this array.
    trips = {}  # makekey(tripset) => count
    for i in range(9):
        s = a[i]
        if len(s) == 3:
            t3 = set()
            for t in s:
                t3.add(t)
            # now check for the set in the known trips[]
            key = makekey(t3)
            if key in trips:
                trips[key] += 1
            else:
                trips[key] = 1

            # We hit 3 triplets, purge them from the rest of the array!            
            if 3 == trips[key]:
                for i in range(9):
                    # skip the 3 triplets
                    s = a[i]
                    k = makekey(s)
                    if k == key:
                        continue
                    # purge the triplets
                    a[i].discard(t3)

def solve(m):
    for i in range(9):
        remove_knowns(get_row(m, i))
        remove_knowns(get_col(m, i))
        remove_knowns(get_box(m, i))  # from left to right, top to bottom

        do_uniques(get_row(m, i))
        do_uniques(get_col(m, i))
        do_uniques(get_box(m, i))  # from left to right, top to bottom

        do_exclusive_pairs(get_row(m, i))
        do_exclusive_pairs(get_col(m, i))
        do_exclusive_pairs(get_box(m, i))  # from left to right, top to bottom
            
        # These work, but probably aren't necessary to solve:
        do_exclusive_trips(get_row(m, i))
        do_exclusive_trips(get_col(m, i))
        do_exclusive_trips(get_box(m, i))  # from left to right, top to bottom


if __name__ == '__main__':
    printWorkset('BEFORE', workset)
    for x in range(10):  # arbitrary # of attempts
        solve(workset)
    printWorkset('AFTER', workset)
