import torch
import torch.nn as nn
import numpy as np
from board import Board
from net import Net
import time

gamma = 0.8
height = 5
width = 5

board = Board(width, height)
net = Net(width, height)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters())

while True:
    board.generate_random()
    steps = 0
    buff = []
    while True:
        actions = net.forward(torch.from_numpy(board.get_arr().flatten()))
        #print(actions)
        action = np.argmax(actions.data.numpy())
        reward = board.take_action(action)
        #board.print()
        #print("-----")
        #time.sleep(0.3)
        buff.append((actions, action))
        steps += 1
        if steps > 50:
            print("Took too long")
            reward = -1
        if len(buff) > 4:
            del buff[0]
        if reward == -1:
            re = -1
            print("Death")
        elif reward == 1:
            re = 1
            print("Success")
        if reward == -1 or reward == 1: #we died
            for x in reversed(range(len(buff))):
                #print(re)
                optimizer.zero_grad()
                loss = criterion(buff[x][0][buff[x][1]], torch.Tensor([re/2+0.5])[0])
                loss.backward()
                optimizer.step()
                re *= gamma
            break
