import numpy as np

class Board:
    def __init__(self, width, height):
        self.arr = np.zeros((height, width, 3), dtype=np.float32)

    def generate_random(self):
        arrshape = self.arr.shape

        # randomly distribute holes across map
        for y in range(arrshape[0]):
            for x in range(arrshape[1]):
                rand = np.random.uniform()
                if rand < 0.00:
                    self.arr[y][x][0] = 1
                else:
                    self.arr[y][x][0] = 0
                self.arr[y][x][1] = 0
                self.arr[y][x][2] = 0

        self.player_y = int(np.random.uniform()*arrshape[0])
        self.player_x = int(np.random.uniform()*arrshape[1])
        self.goal_y = int(np.random.uniform()*arrshape[0])
        self.goal_x = int(np.random.uniform()*arrshape[1])
        while self.goal_x == self.player_x and self.goal_y == self.player_y:
            self.goal_y = int(np.random.uniform()*arrshape[0])
            self.goal_x = int(np.random.uniform()*arrshape[1])
        self.arr[self.player_y][self.player_x][0] = 0
        self.arr[self.player_y][self.player_x][1] = 1
        self.arr[self.player_y][self.player_x][2] = 0
        self.arr[self.goal_y][self.goal_x][0] = 0
        self.arr[self.goal_y][self.goal_x][1] = 0
        self.arr[self.goal_y][self.goal_x][2] = 1

    def take_action(self, action):
        if action == 0: #left
            if self.player_x == 0: #edge of board
                return -1 #can't go there
            self.clear_player_spot()
            self.player_x -= 1
            rew = self.get_reward()
            self.set_player_spot()
            return rew
        elif action == 1: #right
            if self.player_x == self.arr.shape[1]-1: #edge of board
                return -1 #can't go there
            self.clear_player_spot()
            self.player_x += 1
            rew = self.get_reward()
            self.set_player_spot()
            return rew
        elif action == 2: #up
            if self.player_y == 0: #edge of board
                return -1 #can't go there
            self.clear_player_spot()
            self.player_y -= 1
            rew = self.get_reward()
            self.set_player_spot()
            return rew
        elif action == 3: #up
            if self.player_y == self.arr.shape[0]-1: #edge of board
                return -1 #can't go there
            self.clear_player_spot()
            self.player_y += 1
            rew = self.get_reward()
            self.set_player_spot()
            return rew

    def clear_player_spot(self):
        self.arr[self.player_y][self.player_x][0] = 0
        self.arr[self.player_y][self.player_x][1] = 0
        self.arr[self.player_y][self.player_x][2] = 0

    def set_player_spot(self):
        self.arr[self.player_y][self.player_x][0] = 0
        self.arr[self.player_y][self.player_x][1] = 1
        self.arr[self.player_y][self.player_x][2] = 0

    def get_reward(self):
        if self.arr[self.player_y][self.player_x][0] == 1: #hole
            return -1 #invalid position
        elif self.arr[self.player_y][self.player_x][2] == 1: #goal
            return 1 #success
        else:
            return 0 #neutral

    def get_arr(self):
        return self.arr

    def print(self):
        arrshape = self.arr.shape
        for y in range(arrshape[0]):
            for x in range(arrshape[1]):
                is_hole = self.arr[y][x][0] == 1
                is_player = self.arr[y][x][1] == 1
                is_goal = self.arr[y][x][2] == 1
                if is_hole:
                    print("H", end="")
                elif is_player:
                    print("P", end="")
                elif is_goal:
                    print("G", end="")
                else:
                    print("-", end="")
            print("")
