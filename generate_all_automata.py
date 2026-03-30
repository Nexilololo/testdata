import os

automata = {}

automata[1] = {'symbols': 1, 'states': 1, 'init': [0], 'final': [0], 'trans': []}
automata[2] = {'symbols': 1, 'states': 1, 'init': [0], 'final': [0], 'trans': [(0, 'a', 0)]}
automata[3] = {'symbols': 1, 'states': 2, 'init': [0], 'final': [1], 'trans': [(0, 'a', 1)]}
automata[4] = {'symbols': 1, 'states': 2, 'init': [0], 'final': [], 'trans': [(0, 'a', 1)]}
automata[5] = {'symbols': 2, 'states': 5, 'init': [1, 3], 'final': [2, 4], 'trans': [(1, 'a', 2), (1, 'b', 0), (3, 'a', 0), (3, 'b', 4), (0, 'a', 0), (0, 'b', 0)]}
automata[6] = {'symbols': 2, 'states': 4, 'init': [1, 3], 'final': [0, 2], 'trans': [(1, 'a', 2), (3, 'b', 0)]}
automata[7] = {'symbols': 1, 'states': 2, 'init': [1], 'final': [0], 'trans': [(1, 'a', 1), (1, 'a', 0)]}
automata[8] = {'symbols': 1, 'states': 2, 'init': [1], 'final': [0], 'trans': [(1, 'a', 0), (0, 'a', 0)]}
automata[9] = {'symbols': 2, 'states': 6, 'init': [1], 'final': [0, 1], 'trans': [(1, 'a', 2), (2, 'a', 3), (2, 'b', 3), (3, 'a', 4), (4, 'a', 5), (4, 'b', 5), (5, 'a', 0), (0, 'a', 2)]}
automata[10] = {'symbols': 2, 'states': 5, 'init': [0], 'final': [0], 'trans': [(0, 'a', 1), (1, 'a', 2), (1, 'b', 2), (2, 'a', 3), (3, 'a', 4), (3, 'b', 4), (4, 'a', 0)]}
automata[11] = {'symbols': 2, 'states': 4, 'init': [0], 'final': [2], 'trans': [(2, 'a', 1), (2, 'b', 0), (0, 'a', 2), (0, 'b', 3), (1, 'a', 3), (1, 'b', 3), (3, 'b', 3), (3, 'a', 3)]}
automata[12] = {'symbols': 4, 'states': 2, 'init': [1], 'final': [1], 'trans': [(1, 'a', 1), (1, 'c', 0), (0, 'b', 0), (0, 'd', 1)]}
automata[13] = {'symbols': 1, 'states': 8, 'init': [1], 'final': [0, 3, 4, 5, 6, 7], 'trans': [(1, 'a', 2), (2, 'a', 3), (3, 'a', 4), (4, 'a', 5), (5, 'a', 6), (6, 'a', 7), (7, 'a', 0), (0, 'a', 0)]}
automata[14] = {'symbols': 4, 'states': 4, 'init': [0], 'final': [1], 'trans': [(0, 'a', 0), (0, 'b', 2), (0, 'c', 3), (0, 'd', 1), (2, 'b', 2), (2, 'c', 3), (2, 'd', 1), (3, 'c', 3), (3, 'd', 1), (1, 'd', 1)]}
automata[15] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [4], 'trans': [(1,'a',1), (1,'b',2), (1,'c',3), (1,'d',4), (2,'b',2), (2,'c',3), (2,'d',4), (2,'a',0), (3,'c',3), (3,'d',4), (3,'a',0), (3,'b',0), (4,'d',4), (4,'a',0), (4,'b',0), (4,'c',0), (0,'a',0)]}
automata[16] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [0], 'trans': [(1,'a',1), (1,'a',2), (2,'b',2), (2,'b',3), (3,'c',3), (3,'c',4), (4,'d',4), (4,'d',0)]}
automata[17] = {'symbols': 4, 'states': 6, 'init': [1,2,3,4], 'final': [5], 'trans': [(1,'a',1), (1,'a',2), (2,'b',2), (2,'b',3), (3,'c',3), (3,'c',4), (4,'d',4), (4,'d',5), (5,'a',0), (5,'b',0), (5,'c',0), (5,'d',0)]}
automata[18] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [0], 'trans': [(1,'a',2), (1,'b',3), (1,'c',4), (1,'d',0), (2,'a',2), (2,'b',3), (2,'c',4), (2,'d',0), (3,'b',3), (3,'c',4), (3,'d',0), (4,'c',4), (4,'d',0)]}
automata[19] = {'symbols': 1, 'states': 3, 'init': [1], 'final': [0], 'trans': [(1,'a',2), (2,'a',0), (0,'a',0)]}
automata[20] = {'symbols': 4, 'states': 9, 'init': [1,6,7,8,0], 'final': [5], 'trans': [(1,'a',2), (6,'a',2), (2,'b',3), (7,'b',3), (3,'c',4), (8,'c',4), (4,'d',5), (0,'d',5)]}
automata[21] = {'symbols': 4, 'states': 4, 'init': [1], 'final': [1], 'trans': [(1,'a',2), (2,'b',3), (3,'c',0), (0,'d',1)]}
automata[22] = {'symbols': 4, 'states': 4, 'init': [1], 'final': [1], 'trans': [(1,'a',2),(1,'a',3), (1,'a',0), (2,'b',3), (3,'c',0), (0,'d',1)]}
automata[23] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [0], 'trans': [(1,'a',2), (2,'a',2), (2,'b',3), (3,'b',3), (3,'c',4), (4,'c',4), (4,'d',0), (0,'d',0)]}
automata[24] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [0], 'trans': [(1,'a',2), (1,'b',3), (1,'c',4), (1,'d',0), (2,'a',2), (2,'b',3), (2,'c',4), (2,'d',0), (3,'b',3), (3,'c',4), (3,'d',0), (4,'c',4), (4,'d',0), (0,'d',0)]}
automata[25] = {'symbols': 4, 'states': 5, 'init': [1], 'final': [0], 'trans': [(1,'a',1), (1,'a',2), (1,'b',3), (1,'c',4), (1,'d',0), (2,'b',2), (2,'b',3), (2,'c',4), (2,'d',0), (3,'c',3), (3,'c',4), (3,'d',0), (4,'d',4), (4,'d',0)]}
automata[26] = {'symbols': 2, 'states': 4, 'init': [1], 'final': [3], 'trans': [(1,'a',2), (1,'b',2), (2,'a',0), (2,'b',3), (3,'a',3), (3,'b',3)]}
automata[27] = {'symbols': 2, 'states': 3, 'init': [1], 'final': [0], 'trans': [(1,'a',2), (1,'b',2), (2,'b',0), (0,'a',0), (0,'b',0)]}
automata[28] = {'symbols': 1, 'states': 6, 'init': [1,4], 'final': [3,0], 'trans': [(1,'a',2), (1,'a',4), (2,'a',3), (3,'a',2), (4,'a',5), (5,'a',0), (0,'a',4)]}
automata[29] = {'symbols': 1, 'states': 6, 'init': [1], 'final': [3, 0], 'trans': [(1, 'a', 2), (1, 'a', 4), (2, 'a', 3), (3, 'a', 2), (3, 'a', 0), (4, 'a', 3), (4, 'a', 5), (5, 'a', 0), (0, 'a', 4)]}
automata[30] = {'symbols': 1, 'states': 5, 'init': [1], 'final': [3, 4, 0], 'trans': [(1, 'a', 2), (2, 'a', 3), (3, 'a', 4), (4, 'a', 0), (0, 'a', 3)]}
automata[31] = {'symbols': 3, 'states': 8, 'init': [0], 'final': [7], 'trans': [(0, 'e', 1), (0, 'e', 4), (1, 'a', 2), (1, 'e', 3), (2, 'a', 3), (2, 'b', 1), (3, 'b', 3), (3, 'e', 7), (4, 'b', 5), (5, 'b', 6), (6, 'e', 4), (6, 'e', 7)]}
automata[32] = {'symbols': 5, 'states': 22, 'init': [0], 'final': [21], 'trans': [(0,'e',1), (0,'e',10), (1,'e',2), (1,'e',6), (2,'e',3), (3,'b',4), (4,'e',3), (4,'e',5), (2,'e',5), (5,'e',8), (6,'a',7), (7,'e',8), (8,'c',9), (9,'e',21), (10,'e',11), (10,'e',15), (11,'e',12), (12,'a',13), (13,'e',12), (13,'e',14), (11,'e',14), (14,'e',17), (15,'b',16), (16,'e',17), (17,'e',18), (17,'e',20), (18,'c',19), (19,'e', 18), (19,'e',20), (20,'e',21)]}
automata[33] = {'symbols': 5, 'states': 13, 'init': [0], 'final': [12], 'trans': [(0,'e',1), (0,'e',7), (1,'e',2), (1,'e',4), (2,'a',3), (3,'e',5), (4,'b',4), (4,'e',5), (5,'c',6), (6,'e',12), (7,'e',8), (7,'e',9), (8,'a',8), (8,'e',11), (9,'b',10), (10,'e',11), (11,'c',11), (11,'e',12)]}
automata[34] = {'symbols': 5, 'states': 7, 'init': [0], 'final': [6], 'trans': [(0,'e',1), (0,'e',4), (1,'a',2), (1,'e',2), (2,'b',3), (4,'b',5), (3,'e',2), (5,'e',4), (3,'e',6), (5,'e',6)]}
automata[35] = {'symbols': 5, 'states': 11, 'init': [0], 'final': [10], 'trans': [(0,'e',1), (0,'e',4), (1,'a',2), (2,'b',3), (4,'e',5), (5,'a',6), (6,'b',7), (7,'e',8), (7,'e',5), (4,'e',8), (8,'a',9), (9,'e',10), (3,'e',10)]}
automata[36] = {'symbols': 2, 'states': 3, 'init': [0, 2], 'final': [1, 2], 'trans': [(0,'a',1), (0,'b',1), (0,'b',2), (2,'a',0), (1,'b',2), (2,'a',1), (1,'b',0)]}
automata[37] = {'symbols': 2, 'states': 5, 'init': [0], 'final': [0, 1, 2, 3, 4], 'trans': [(0,'a',1), (1,'a',2), (2,'a',0), (3,'a',1), (1,'a',4), (4,'a',1), (0,'b',3), (3,'b',0)]}
automata[38] = {'symbols': 2, 'states': 4, 'init': [0], 'final': [0, 1, 2, 3], 'trans': [(0,'a',1), (1,'b',2), (1,'a',1), (0,'b',3), (2,'a',3), (2,'b',3), (3,'a',3), (3,'b',3)]}
automata[39] = {'symbols': 2, 'states': 4, 'init': [0, 1, 3], 'final': [1], 'trans': [(0,'a',1), (1,'a',1), (0,'b',2), (2,'a',0), (1,'b',2), (2,'b',1), (3,'a',1), (3,'a',2)]}
automata[40] = {'symbols': 2, 'states': 3, 'init': [0, 1], 'final': [0, 2], 'trans': [(0,'b',1), (1,'a',0), (1,'a',2), (1,'b',2), (2,'a',0), (0,'b',2)]}
automata[41] = {'symbols': 2, 'states': 6, 'init': [0], 'final': [1, 2, 3, 4], 'trans': [(0,'a',1), (0,'b',4), (1,'a',2), (1,'b',3), (2,'a',2), (2,'b',3), (4,'a',5), (4,'b',5), (3,'a',5), (3,'b',5), (5,'a',5), (5,'b',5)]}
automata[42] = {'symbols': 3, 'states': 5, 'init': [1], 'final': [1], 'trans': [(0,'b',1), (1,'a',0), (1,'b',2), (2,'a',1), (0,'a',3), (0,'c',3), (2,'b',4), (2,'c',4), (3,'a',3), (3,'b',3), (3,'c',3), (4,'a',4), (4,'b',4), (4,'c',4)]}
automata[43] = {'symbols': 2, 'states': 3, 'init': [0], 'final': [2], 'trans': [(0,'b',1), (1,'a',2), (0,'a',0), (0,'b',0), (2,'a',2), (2,'b',2)]}
automata[44] = {'symbols': 2, 'states': 4, 'init': [0], 'final': [2, 3], 'trans': [(0,'a',1), (0,'a',2), (0,'b',2), (1,'b',3), (2,'a',3),(3,'a',2), (3,'b',2), (2,'b',2), (3,'a',3), (3,'b',3)]}

if __name__ == "__main__":
    for i in sorted(automata.keys()):
        fname = f"FA-{i:02d}.txt"  
        data = automata[i]
        with open(fname, "w") as f:
            f.write(f"{data['symbols']}\n")
            
            # for 29+ we used max of nodes, but we stored the exact states for 1-28
            if i >= 29:
                max_st = 0
                if data['trans']:
                    max_st = max([u for u,s,v in data['trans']] + [v for u,s,v in data['trans']])
                if data['init']:
                    max_st = max(max_st, max(data['init']))
                if data['final']:
                    max_st = max(max_st, max(data['final']))
                num_states = max_st + 1
            else:
                num_states = data['states']
            f.write(f"{num_states}\n")
                
            init_str = f"{len(data['init'])}" + (" " + " ".join(map(str, data['init'])) if data['init'] else "")
            f.write(f"{init_str}\n")
            final_str = f"{len(data['final'])}" + (" " + " ".join(map(str, data['final'])) if data['final'] else "")
            f.write(f"{final_str}\n")
            f.write(f"{len(data['trans'])}\n")
            for (u, sym, v) in data['trans']:
                f.write(f"{u}{sym}{v}\n")
        print(f"Generated {fname}")
        

