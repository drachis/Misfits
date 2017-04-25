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


	
