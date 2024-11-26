import math
import random
import time
import pygame
pygame.init()


WIDTH, HEIGHT = 800, 600

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   #draw the window and pass your width and height
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400 #milliseconds    #delay before creating a new target
TARGET_EVENT = pygame.USEREVENT #custom event

TARGET_PADDING = 30 #pixels off the screen
BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "white"
    SECOND_COLOR = "red"
    

    def __init__(self, x, y):   #Initilazation = constructor of our target, self is target itself, x and y are positions of the targets.
        self.x = x              #place the positions randomly and place them inside the objects
        self.y = y              #place the positions randomly and place them inside the objects
        self.size = 0           #radius of the target
        self.grow = True

#Function that makes the target bigger or smaller
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE       #Shrinks the target

#Function that draws the target on the screen
    def draw(self, win):    #window object to draw the target into.
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size) #win that's where we wanna draw it, color, and center of the target i.e.i., x and y, then pass the radius or size of the target 
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)


    def collide(self, x, y):        
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)      #formula for the distance/ mouse position to check if we have collided to our circle.
        return dis <= self.size              # return if the distance is less than or equal to the size of the circle.


def draw(win, targets):     #draw on the window
    win.fill(BG_COLOR)

    for target in targets:  #loop thru all our targets
        target.draw(win)    #draw the all the targets on the window. Hence it already accepts the window up in the window function, knows how to draw it. But you haven't looped thru them and called them.
    
    
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100) #math.floor round down the number, formula that will give us the formula for milli seconds.
    seconds= int(round(secs % 60, 1)) #rounded seconds 60 percent, round to the 1 or 1st decimal place.
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"     #02d starts with 2 digits. 01:02:03

    

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))   #0,0 is the top left hand of our pygame window (0,0 top left). WIDTH of teh rectangle is the WIDTH of the WINDOW
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")  #string of text, 1, and color of the text. P.S. just put one

   
    speed = round(targets_pressed / elapsed_time, 1)     #number of targets pressed in the elapsed time. 1 is round off to 1 decimal point
    speed_label = LABEL_FONT.render(
        f"Speed: {speed} t/s", 1, "black")  #t/s targets per second

    hits_label = LABEL_FONT.render(
        f"Hits: {targets_pressed}", 1, "black")
    
    lives_label = LABEL_FONT.render(
        f"Lives: {LIVES - misses}", 1, "black")



    win.blit(time_label, (5, 5))    #blit is another way to show another surface on the screen, positiomn on the screen 5 from top & 5 from left
    win.blit(speed_label, (200, 5))    # 200 x position to space out from the time label
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(
    f"Time: {format_time(elapsed_time)}", 1, "white")  #string of text, 1, and color of the text. P.S. just put one

   
    speed = round(targets_pressed / elapsed_time, 1)     #number of targets pressed in the elapsed time. 1 is round off to 1 decimal point
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")  #t/s targets per second

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")


    win.blit(time_label, (get_middle(time_label), 100))    # get middle function is the program we made to get the center of the screen
    win.blit(speed_label, (get_middle(speed_label), 200))    # 200 x position to space out from the time label
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))


    pygame.display.update()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:       #keydown press any key
                run = False
                quit()


def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2

#Make and infinite loop to check for different events i.e., pressing on screen, qutting the window, etc.,
def main():
    run = True
    targets = []    # store all targets, loop thru the targets, update size and draw on screen, but every _ second we need to place another target on the screen for this we need CUSTOM EVENT and put inside this array
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()    #to track time, when did we start running the code, and tell how much time has elapsed. time.time() is the the current time.

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) #trigger target event, every target increment time


    while run:
        clock.tick(60)
        click = False
        mos_pos = pygame.mouse.get_pos() # get pos will give us pos = [x, y] but we need to breakdown this position beacuse we have a argument paramater in collide of x and y i.e., (self, x, y). Add astirisk in our mos_pos
        elapsed_time = time.time() - start_time


        for event in pygame.event.get():    #loop thru all events that are occuring
            if event.type == pygame.QUIT:   #in pygame when you click the X button it will trigger an event. SO you need to program a way to exit.
                run = False
                break
            
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)  # Basically generate a random position for x and within target padding, and width minus target padding so that the target wont appear off the screen
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)  # so that targets will not appear behind the top bar label 
                target = Target(x, y)
                targets.append(target)  #Pushes the new target into the targets list so that we can now loop thru it.
    
            if event.type == pygame.MOUSEBUTTONDOWN:    #this is the event
                click = True
                clicks += 1


        for target in targets:  #make sure we target all our targets before we draw them. Up there you aonly drew the target but not yet updated.
            target.update()

            if target.size <= 0:    #since our targets are becoming bigger and smaller, what we want is that after shrinking we want it to disappear.
                targets.remove(target)  #remove target from targets.
                misses += 1                #when target disappears it becomes a miss.

            if click and target.collide(*mos_pos):       #astirisk will breakdown the tuple into individual components and we will have 1 positions for each. Short way of doing (mos_pos [0], mos_pos[1])
                targets.remove(target)
                targets_pressed += 1                  

        if misses >= LIVES:
            end_screen(WINDOW, elapsed_time, targets_pressed, clicks)
                #pass #end


        draw(WINDOW, targets)   #call draw function, on the WINDOW and put the targets.
        draw_top_bar(WINDOW, elapsed_time, targets_pressed, misses)
        pygame.display.update()   #the update will only draw all that's encoded above it. Once we've drawn all the targets, then we'll call update fn.



    
    pygame.quit()

if __name__ == "__main__":
    main()








