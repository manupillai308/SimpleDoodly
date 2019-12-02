#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np

mouseX = mouseY = None
FLAG = False
mouse = []
PROP = 1
pen = cv2.imread("./pen.png", cv2.IMREAD_UNCHANGED)
eraser = cv2.imread("./erase.png", cv2.IMREAD_UNCHANGED)
pen = cv2.resize(pen, (280//PROP, 500//PROP))
eraser = cv2.resize(eraser, (280//PROP, 500//PROP))


def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY, FLAG, mouse
	if event == cv2.EVENT_MOUSEMOVE and FLAG:
		mouseX,mouseY = x,y
		mouse.append((y,x))
		
	if event == cv2.EVENT_LBUTTONDOWN:
		FLAG = True
	if event == cv2.EVENT_LBUTTONUP:
		FLAG = False
		

cv2.namedWindow('board')
cv2.setMouseCallback('board',draw_circle)

def get_board():
	board = np.zeros((920//PROP, 1500//PROP, 4))
	board[...,-1] = 255
	return board

def write(board, pen, offset_x = 0, offset_y = 0):
	endr = min(offset_x+pen.shape[0], board.shape[0])
	endc = min(offset_y+pen.shape[1], board.shape[1])
	endr1 = min(pen.shape[0], board.shape[0] - offset_x)
	endc1 = min(pen.shape[1], board.shape[1] - offset_y)
	opaque = (pen[...,-1] > 210).reshape((*pen.shape[:2],1))
	pen = (opaque*pen)[0:endr1, 0:endc1] + (np.bitwise_not(opaque[0:endr1, 0:endc1]) * board[offset_x:endr, offset_y:endc])
	board[offset_x:endr, offset_y:endc] = pen
	
def play(mouse):
	new_board_t = get_board()
	for pos in mouse:
		cv2.circle(new_board_t, pos[::-1], 3, (255,255,255, 0), -1)
		new_board = new_board_t.copy()
		write(new_board, pen, *pos)
		cv2.imshow("board", new_board.astype("uint8"))
		cv2.waitKey(1)
	
	for pos in mouse[::-1]:
		new_board = new_board_t.copy()
		write(new_board, eraser, *pos)
		cv2.circle(new_board_t, pos[::-1], 3, (0,0,0, 0), -1)
		cv2.imshow("board", new_board.astype("uint8"))
		cv2.waitKey(1)

board = get_board()

while True:
	if mouseX is not None:
		cv2.circle(board,(mouseX,mouseY),3,(255,255,255, 0),-1)
	cv2.imshow('board',board.astype("uint8"))
	k = cv2.waitKey(1) & 0xFF
	if k == ord("q"):
		break
	if k == ord("r"):
		board = get_board()
		mouse = []
		mouseX = None
	if k == ord("p"):
		play(mouse)
cv2.destroyAllWindows()
