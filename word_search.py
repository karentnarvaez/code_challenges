class Solution:
    self.used = list()
    self.keyword = ''
    self.board = None
    
    def exist(self, board: List[List[str]], word: str) -> bool:
        self.keyword = word
        self.board = board
        self.used = [[False for node in row] for row in board]
        self.backtracking(0, 0)
    
    
    def backtracking(self, x: int, y: int, board: List[List[str]]):
        
        
        self.get(x,y)
        
        if not self.:
            self.used[y][x] = True
            self.backtracking(x+1, y+1)
            
    
    def get(self, x: int, y: int) -> bool:
        if y > len(self.board) or x > board[0].length:
            return -1
        else:
            return self.board[y][x]