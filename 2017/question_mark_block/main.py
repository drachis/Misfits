import sys
import os
import pygame 
import random


def findSprites(directory, ext = [".gif", ".png", ".GIF", ".PNG"]):
	sprites =  []
	for r,d,f in os.walk(directory):
		for fi in f:
			split = os.path.splitext(fi)
			if split[1] in ext:
				sprites.append(os.path.join(r,fi))
				print sprites[-1]
	return sprites

def incrementSprite(spriterect, sprites):
	scale = 4
	x,y,u,v = spriterect
	idx = random.randint(0,len(sprites)-1)
	s = sprites[idx]
	sprite = pygame.image.load(s)
	sprite = pygame.transform.scale(sprite, (int(sprite.get_size()[0])*scale,int(sprite.get_size()[1])*scale))
	spriterect = sprite.get_rect()
	spriterect.x = x
	spriterect.y = y
	return sprite, spriterect

pygame.init()
clock = pygame.time.Clock()
size = width, height = 640, 480
speed = [8,8]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
sprites = findSprites("./sprites/")
idx = random.randint(0,len(sprites)-1)
s = sprites[idx]
sprite = pygame.image.load(s)
spriterect = sprite.get_rect()
sprite, spriterect = incrementSprite(spriterect,sprites)
pygame.display.toggle_fullscreen()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type== pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			pygame.quit()
			sys.exit()

	spriterect = spriterect.move(speed)
	if spriterect.left < 0 or spriterect.right > width:
		speed[0] = -speed[0]
		sprite, spriterect = incrementSprite(spriterect, sprites)
	if spriterect.top < 0 or spriterect.bottom > height:
		speed[1] = -speed[1]
		sprite, spriterect = incrementSprite(spriterect, sprites)

	screen.fill(black)
	screen.blit(sprite, spriterect)
	pygame.display.flip()
	time = clock.tick(60)
	if (time < 1000/60):
		pygame.time.wait(1000/60-time)


'''
plan for slot machine

SETUP
initialize sprite locations,
Each location has a sprite / rendering slot, (class?)
Create a pool or loaded potential sprites ( to minimize disk read time)
Function
	The locations above the current are randomized from the pool of sprites
	    0 - teleport to 3 when this position is reached
	   [1] - visible
	   	2
	   	3 - start location
initilize each spin with a different , 
	Select an amount of time before result is displayed (2-5s? make this easy to tune)
INPUT LOOP
on button press / input
	disable further input until after refresh 
	animate the sprites moving up the screen space, 
		since the input comes from the user press at the bottom on the screen
		if a sprite reaches location 0 teleport it to location 3 at the bottom of the queue.
	If the result is a coin allow the user to continue to hit the block, make coin sounds?
	Then after power up is revealed have a cooldown where the block is in a deactivated state (bricks)
	Reactivate after 10-30s as a question mark [?] 
		- this is to prevent people from spamming hits.
		- make some sort of power-up available (yoshi mount?) sound 




