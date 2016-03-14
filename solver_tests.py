import unittest
from sudokuset import SudokuSet
from solver import *

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

solution = hard

# one-dimensional array of SudokySet's

class TestSolver2(unittest.TestCase):

    def setUp(self):
        self.ws = [SudokuSet(solution[j][i]) for j in range(9) for i in range(9)]
        
    def assert_cell(self, s, v):
        ''' Asserts int 'v' is the only value in set 's' '''
        self.assertTrue(len(s) == 1)
        self.assertTrue(v in s, 'v[{}] in s[{}]'.format(v, s))

# HACK: Mixing SudokuSet tests in here for now
    def test_sudokuset(self):
        for x in self.ws:
            self.assertTrue(1 == len(x) or 8 <= len(x))
            self.assertTrue(9 >= len(x))
            if 8 in x:
                x.add(8)
            self.assertTrue(1 == len(x) or 8 <= len(x))
            self.assertTrue(9 >= len(x))
     
    def test_getbox(self):
        b = get_box(self.ws, 0)
#         print('b={}'.format(b))
        self.assert_cell(b[0], 3)
        self.assert_cell(b[2], 4)
        self.assert_cell(b[3], 2)
        self.assert_cell(b[7], 6)

        b = get_box(self.ws, 4)
        self.assert_cell(b[1], 8)
        self.assert_cell(b[2], 9)
        self.assert_cell(b[4], 1)
        self.assert_cell(b[7], 3)
  
    def test_get_row(self):
        r = get_row(self.ws, 0)
        self.assert_cell(r[0], 3)
        self.assert_cell(r[2], 4)
        
        r = get_row(self.ws, 8)
        self.assert_cell(r[6], 6)
        self.assert_cell(r[8], 2)

    def test_get_col(self):
        c = get_col(self.ws, 0)
        self.assertTrue(9 == len(c))
        self.assert_cell(c[0], 3)
        self.assert_cell(c[1], 2)
        self.assert_cell(c[3], 4)
        self.assert_cell(c[5], 9)
        
    def test_get_knowns(self):
        row = get_row(self.ws, 0)
        self.assertTrue(3 in row[1])
        self.assertTrue(2 in row[1])
        self.assertTrue(4 in row[1])
        k = get_knowns(row)
        self.assertTrue(3 in k)
        self.assertTrue(4 in k)
        self.assertTrue(2 not in k)
                                       
    def test_remove_knowns(self):
        r = get_col(self.ws, 2)
        pre = []
        for x in r:
            pre.append(len(x))
        remove_knowns(r)
        post = []
        for x in r:
            post.append(len(x))
        
    def test_do_exclusive_pairs(self):
        r = [1,2,3,4,5,6,0,0,0]
        w = [SudokuSet(r[i]) for i in range(9)]
        remove_knowns(w)
        print('type(w[7])={} ,w[7]={}'.format(type(w[7]), w[7]))
        s = set()
        s.add(7)
        w[7].discard(s)
        w[8].discard(s)
        
        print(w)
        do_exclusive_pairs(w)
        print(w)
        self.assertTrue(len(w[6]) == 1)
    
    def test_do_exclusive_trips(self):
        r = [1,2,3,4,5,0,0,0,0]
        w = [SudokuSet(r[i]) for i in range(9)]
        remove_knowns(w)
        s = set()
        s.add(6)
        w[6].discard(s)
        w[7].discard(s)
        w[8].discard(s)
        # w[5] still contains a 6, but will have its other members removed
        
        print(w)
        do_exclusive_trips(w)
        print(w)
        self.assertTrue(len(w[5]) == 1)

    def test_do_uniques(self):
        r = [1,2,3,4,5,0,0,0,0]
        w = [SudokuSet(r[i]) for i in range(9)]
        nine = set()
        nine.add(9)
        w[5].discard(nine)
        w[6].discard(nine)
        w[7].discard(nine)
        # now only w[8] has a 9
        do_uniques(w)
        self.assert_cell(w[8], 9)
        
    def test_makekey(self):
        s = set()
        s.add(3)
        s.add(1)
        s.add(2)
        self.assertTrue('123' == makekey(s))
        
if __name__ == '__main__':
    unittest.main()