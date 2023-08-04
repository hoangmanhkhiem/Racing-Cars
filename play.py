import pygame
import sys
import random
import time

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

WIDTH = 900
HEIGHT = 700

RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW =(255,255,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Racing Cars')
# pygame.display.toggle_fullscreen()	

game_over = False

truck_width = 61
truck_height = 157
truck_list = []

truck_starts =[140, 240, 330, 430, 520,630, 720, 810]

car_width = 62
car_height = 132
car_pos = [WIDTH/2-car_width//2,HEIGHT-car_height]

shift_size = 30

clock = pygame.time.Clock()
clock_speed = 100
start_time = time.time()

speed = 2
score = 0

car_image = pygame.image.load("racecar1.gif")
truck_image = pygame.image.load("truck.gif")
background = pygame.image.load("background.png")

myFont = pygame.font.SysFont("Calibri", 20);

# music section
pygame.mixer.music.load("jazzinparis.mp3")
pygame.mixer.music.set_volume(.8)
pygame.mixer.music.play(-1)


def text_objects(text,font):
	text_surface = font.render(text, True, WHITE)
	return text_surface,text_surface.get_rect()

def message_display(text):
	large_text = pygame.font.Font('freesansbold.ttf',75)
	text_surface, text_rectangle = text_objects(text, large_text)
	text_rectangle.center = ((WIDTH//2),(HEIGHT//2))
	screen.blit(text_surface,text_rectangle)
	pygame.display.update()

	time.sleep(2) 
	pygame.quit()

def crash():
	message_display("GAME OVER")

def display_car(car_pos):
	screen.blit(car_image,(car_pos[0],car_pos[1]))

def display_trucks(truck_pos):
	for truck_pos in truck_list:
		screen.blit(truck_image,(truck_pos[0],truck_pos[1]))

def overlap(truck_list,lane_number):
	for truck_pos in truck_list:
		if truck_pos[1]>=0 and truck_pos[1]<truck_height and truck_pos[0] == lane_number:
			return True
	return False

def drop_trucks(truck_list,truck_starts):
	delay = random.random()
	if len(truck_list) < 7 and delay < 0.05 :
		lane_number = random.randint(0,len(truck_starts)-1)
		if overlap(truck_list,truck_starts[lane_number]):
			return
		x_pos = truck_starts[lane_number]
		y_pos = 0
		truck_list.append([x_pos,y_pos])

def update_truck_positions(truck_list,score,speed):
	# change truck position
	for idx, truck_pos in enumerate(truck_list):
		if truck_pos[1] >=0 and truck_pos[1] <HEIGHT:
			truck_pos[1] += speed
		else:
			truck_list.pop(idx)
			score += 1
	return score

def detect_collision(car_pos,truck_pos):
	p_x = car_pos[0]
	p_y = car_pos[1]
	e_x = truck_pos[0]
	e_y = truck_pos[1]
	if (e_x>=p_x and e_x<(p_x+car_width)) or (p_x>=e_x and p_x<(e_x+truck_width)):
		if (e_y>=p_y and e_y < (p_y+car_height)) or (p_y>=e_y and p_y<(e_y+truck_height)):
			return True
	return False

def collision_check(truck_list,car_pos):
	for truck_pos in truck_list:
		if detect_collision(car_pos,truck_pos):
			return True
	return False

while not game_over:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			game_over=True
			break

		if event.type == pygame.KEYDOWN:
			x = car_pos[0]
			y = car_pos[1]
			if event.key == pygame.K_LEFT and x >= 140:
				x -= shift_size
			elif event.key == pygame.K_RIGHT and x <= 810:
				x +=  shift_size
			elif event.key == pygame.K_DOWN:
				y += shift_size
			elif event.key == pygame.K_UP:
				y -=  shift_size
			x=max(x,0)
			x=min(x,WIDTH-car_width)
			y=max(y,0)
			y=min(y,HEIGHT-car_height)
			car_pos = [ x , y ]

	# screen.fill(WHITE)
	screen.blit(background,(-3,0))
	

	drop_trucks(truck_list,truck_starts)
	score  = update_truck_positions(truck_list,score,speed)
	speed = (score//10) + 1

	time_now = round(time.time()-start_time,2)
	text1 = "Score:  "+ str(score)
	text2 = "Level:  "+ str(speed)
	label1 = myFont.render(text1, 1, WHITE)
	label2 = myFont.render(text2, 1, WHITE)
	label3 = myFont.render("Author:", 1, WHITE)
	label4 = myFont.render("Skromnyy", 1, WHITE)
	screen.blit(label1,(WIDTH-900,50))
	screen.blit(label2,(WIDTH-900,20))
	screen.blit(label3,(WIDTH-900,80))
	screen.blit(label4,(WIDTH-900,110))

	if collision_check(truck_list,car_pos):
		game_over=True
		break

	display_trucks(truck_starts)
	display_car(car_pos)
	# screen.blit(truck_image,(790,0))
	pygame.display.update()
	clock.tick(clock_speed)

crash()
pygame.quit()

