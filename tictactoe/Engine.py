import random

class Engine:
    def __init__(self):
        self.table = [["_","_","_"] for _ in range(3)]

    def verify_rows(self):
        for row in self.table:
            if row[0] == row[1] and row[1] == row[2] and row[0]!='_':
                return row[0]
        return '_'

    def verify_cols(self):
        for j in range(3):
            if self.table[0][j] == self.table[1][j] and self.table[1][j] == self.table[2][j] and self.table[0][j] != '_':
                return self.table[0][j]
        return '_'
        
    def verify_diag(self):
        if self.table[0][0] == self.table[1][1] and self.table[1][1] == self.table[2][2] and self.table[0][0]!='_':
            return self.table[0][0]
        if self.table[0][2] == self.table[1][1] and self.table[1][1] == self.table[2][0] and self.table[0][2]!='_':
            return self.table[0][2]
        return '_'

    def verify_table(self):
        k=0
        for row in self.table:
            for x in row:
                if x == '_':
                    k+=1
        return k == 0

    def has_won(self):
        if self.verify_rows() != '_':
            return self.verify_rows()
        if self.verify_cols() != '_':
            return self.verify_cols()
        if self.verify_diag() != '_':
            return self.verify_diag()
        if self.verify_table():
            return '-'
        return '_'               
    
    def get_state(self):
        winner = self.has_won()
        if winner == '-':
            return "draw"
        elif winner == "_":
            return "running"
        else:
            return winner

    def computer_answer(self):
        while True:
            rand_x = random.randrange(3)
            rand_y = random.randrange(3)

            if self.table[rand_x][rand_y] == '_':
                self.table[rand_x][rand_y] = 'O'
                return (rand_x, rand_y)
            

    def make_move(self, i, j):
        if not(i>=0 and i<=2 and j>=0 and j<=2):
            return (-1, -1)
        if self.table[i][j] != '_':
            return (-1, -1)

        self.table[i][j] = 'X'

        if self.get_state() == "running":
            return self.computer_answer()
        
        return (-1, -1)

