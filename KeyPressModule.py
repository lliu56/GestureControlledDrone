import pygame

#creating game window
def init():
    pygame.init()           #init:in the class fxn's
    win = pygame.display.set_mode((400,400))

def getKey(keyName):            # create key press- Fxn determine if the key is pressed from key name
    ans = False                 #default as false, pressed=true,not pressed = false
    for eve in pygame.event.get(): pass  #checking events
    keyInput = pygame.key.get_pressed ()
    myKey = getattr(pygame, 'K_{}'.format (keyName)) #e.g. if the 'LEFT' Key is pressed
                                                    # will return K_{LEFT}
    if keyInput[myKey]:        # if key is pressed, return true
        ans = True
    pygame.display.update ()
    return ans

def main ():                     #main fxn to test getKey fxn
    if getKey('LEFT'):
        print ('Left key pressed')      # LEFT is the key that would return true
    if getKey ('RIGHT'):
        print ('Right key pressed')

if __name__=='__main__':        # if running this file as the 'main' file
    init ()
    while True:
        main()



