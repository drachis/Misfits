import sys, os, pygame, random, time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin = 17
GPIO.setup(pin,GPIO.IN,GPIO.PUD_UP)
prev = False

def findSprites(directory, ext = [".gif", ".png", ".GIF", ".PNG"]):
	sprites =  []
	for r,d,f in os.walk(directory):
		for fi in f:
			split = os.path.splitext(fi)
			if split[1] in ext:
				sprites.append(os.path.join(r,fi))
				print (sprites[-1])
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
	
def pygameMain():
	pygame.init()
	clock = pygame.time.Clock()
	size = width, height = 800, 600
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
	#limit events that are listened for
	pygame.event.set_allowed(None)
	pygame.event.set_allowed(pygame.QUIT)
	pygame.event.set_allowed(pygame.KEYUP)
	prev = False
	while True:
		#pygame.time.wait(150)
		#pygame.event.wait()
		time.sleep(0.1)
		for event in pygame.event.get():
			print(event)
			if (event.type== pygame.KEYUP) or (event.type == pygame.QUIT) :
				pygame.quit()
				sys.exit()
		button = GPIO.input(pin)
		if button != prev: 
			if button:
				print (pin , ", open")
			else:
				incrementSprite(spriterect, sprites)
				print(pin , ", pressed")
			prev = button
		"""spriterect = spriterect.move(speed)
		if spriterect.left < 0 or spriterect.right > width:
			speed[0] = -speed[0]
			sprite, spriterect = incrementSprite(spriterect, sprites)
		if spriterect.top < 0 or spriterect.bottom > height:
			speed[1] = -speed[1]
			sprite, spriterect = incrementSprite(spriterect, sprites)
		"""
		screen.fill(black)
		screen.blit(sprite, spriterect)
		pygame.display.flip()
		#ms = clock.tick(60)
		#if (ms < 1000./60):
			#pygame.time.wait(int(1000./60-ms))
		#clock.tick()
if __name__ == "__main__":
	pygameMain()
