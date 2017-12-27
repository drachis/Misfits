import sys, os, pygame, random, time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    hasGPIO = True
    pin = 17
    GPIO.setup(pin,GPIO.IN,GPIO.PUD_UP)
except:
    print("unable to find GPIO, stepping over")
    pin = "DUMMY"
    hasGPIO = False

prev = False
scriptRoot = os.path.dirname(os.path.abspath(__file__))
holding = False
startTime = -2
shutdownDelay = 5

def findSprites(directory, ext = [".gif", ".png", ".GIF", ".PNG"]):
    sprites =  []
    for r,d,f in os.walk(directory):
        for fi in f:
            split = os.path.splitext(fi)
            if split[1] in ext:
                sprites.append(os.path.join(r,fi))
                print (sprites[-1])
    return sprites

def getRandomSprite(sprites):
    #make more powerful sprites a bit rarer
    rand = random.random()
    idx = 0
    if rand < 0.30:
        idx = 0
    elif rand < 0.55:
        idx = 1
    elif rand < 0.75:
        idx = 2
    elif rand < 0.9:
        idx = 3
    elif rand < 0.95:
        idx = 4
    else:
        idx = 5
    print (idx)
    return sprites[idx]

def incrementSprite(spriterect, sprites):
    scale = 8*4
    x,y,u,v = spriterect
    s = getRandomSprite(sprites)
    #print(s)
    sprite = pygame.image.load(s)
    sprite = pygame.transform.scale(sprite, (int(sprite.get_size()[0])*scale,int(sprite.get_size()[1])*scale))
    spriterect = sprite.get_rect()
    spriterect.x = x
    spriterect.y = y
    return sprite, spriterect

def checkForShutdown():
        '''
        this uses some global variables to store state;
        '''
        global holding
        global startTime
        global shutdownDelay
        if GPIO.input(pin) == 1 and not holding:
                holding = True
                startTime = time.time()
        if GPIO.input(pin) == 0:
                holding = False
        if holding and startTime + shutdownDelay < time.time():
                '''
                when the button is held down, power down the system
                '''
                #print("shutting down")
                os.system("shutdown now -h -P")

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

'''
def pygameMain():
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 800, 600
    speed = [8,8]
    black = 0, 0, 0
    white = 255, 255, 255

    screen = pygame.display.set_mode(size)
    sprites = findSprites(
                os.path.join(
                        scriptRoot,
                        "sprites/")
                )
    idx = random.randint(0,len(sprites)-1)
    s = sprites[idx]
    sprite = pygame.image.load(s)
    questionMark = pygame.image.load(
                os.path.join(scriptRoot,"questonmark_front.png")
                )
    questionMark = pygame.transform.scale(questionMark,(int(size[0]*1.2), int(size[0]*1.2)))
    questionRect = questionMark.get_rect()
    questionRect.x = size[0]/2-questionRect[2]/2
    questionRect.y = size[1]/2-questionRect[3]/2
    spriterect = sprite.get_rect()
    sprite, spriterect = incrementSprite(spriterect,sprites)
    #pygame.display.toggle_fullscreen()
    #pygame.mouse.set_visible(False)
    #limit events that are listened for
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.KEYUP)
    prev = False
    button = True
    swapped = time.time()
    hold = 3
    ready = True
    while True:
        for event in pygame.event.get():
            #print(event)
            if (event.type == pygame.KEYUP and event.key == 27) or (event.type == pygame.QUIT) :
                pygame.quit()
                sys.exit()
            if not hasGPIO and event.type == pygame.KEYUP:
                if event.key == 32:
                    button = True
                else:
                    button = False
        if hasGPIO:
            button = GPIO.input(pin)
        if button != prev and ready:
            print (button)
            if button:
                pass
                #print (pin , ", open")
            else:
                sprite, spriterect = incrementSprite(spriterect, sprites)
                #print(pin , ", pressed")
                swapped = time.time()
            prev = button
        spriterect.x = size[0]/2 - sprite.get_size()[0]/2
        spriterect.y =  size[1]/2 - sprite.get_size()[1]/2
        if swapped + hold > time.time():
            screen.fill(black)
            screen.blit(sprite, spriterect)
            pygame.display.flip()
            ready = False
        else:
            ready = True
            screen.fill(white)
            screen.blit(questionMark, questionRect)
            pygame.display.flip()
        checkForShutdown()
        time.sleep(0.1)
if __name__ == "__main__":
    pygameMain()
