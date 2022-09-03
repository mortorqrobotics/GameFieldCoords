from turtle import position
import pygame
import math

# activate the pygame library initiate pygame and give permission to use pygame's functionality.
pygame.init()
  
# define the RGB value for colors
bg_color = (200, 200, 200) # grey
black = (0,0,0)
white = (255,255,255)
  
# dimentions of screen in px (image dimentions are 890 x 442)
screen_width = 1000
screen_height = 550

# dimentions of the field in in
field_width = 1646
field_height = 823

pxToIn = (field_width/2.54)/screen_width # px to in conversion (field of 1646 x 823)

# create the display surface object of specific dimension (X, Y).
display_surface = pygame.display.set_mode((screen_width, screen_height))
  
# set the pygame window name
pygame.display.set_caption('GameFieldCoords')
  
# create a surface object, image is drawn on it.
image = pygame.image.load('Gamefield.png')

#dot settings
circle_radius = 5
border_width = 0 # 0 = filled circle
circles = [] # list to hold circle positions and text

# create a font object
font = pygame.font.Font('freesansbold.ttf', 16) # style, size
font2 = pygame.font.Font('freesansbold.ttf', 12) # style, size

# infinite loop
while True :
  
    # completely fill the surface object with color
    display_surface.fill(bg_color)
  
    # display image
    display_surface.blit(image, (0, 0))

    if pygame.mouse.get_pos()[0] < 890 and pygame.mouse.get_pos()[1] < 442:
        xIn = round(pygame.mouse.get_pos()[0] * pxToIn, 2) # mouse x pos in inches
        yIn = round(pygame.mouse.get_pos()[1] * pxToIn, 2) # mouse y pos in inches
        xPx = round(pygame.mouse.get_pos()[0], 2) # mouse x pos in px
        yPx = round(pygame.mouse.get_pos()[1], 2) # mouse y pos in px
    else:
        xIn,yIn,xPx,yPx = 0, 0, 0, 0

    # draws mouse position in inches
    display_surface.blit(font.render("x: " + str(xIn) + "in", True, black, bg_color), (900,50))
    display_surface.blit(font.render("y: " + str(yIn) + "in", True, black, bg_color), (900,75))

    # draws mouse position in inches
    display_surface.blit(font.render("x: " + str(xPx) + "px", True, black, bg_color), (900,125))
    display_surface.blit(font.render("y: " + str(yPx) + "px", True, black, bg_color), (900,150))

    # loops through circles to display text and dots
    for i in range(len(circles)):

        if circles[i] != None:

            pygame.draw.circle(display_surface, black, circles[i], circle_radius, border_width) # draws each circle at the correct position

            dot_num = str(i+1) # finds the current dt number as a string

            # finds x and y values for field position in inches as a string
            x_coord = str(round(circles[i][0]*pxToIn, 2))
            y_coord = str(round(circles[i][1]*pxToIn, 2))

            coords_pos = (50 + 170 * (int)(i/3) , 450 + 40 * (i%3)) # position of text under image
            num_pos = (circles[i][0] + 5, circles[i][1] + 5) # position of number next to dot

            display_surface.blit(font2.render(dot_num, True, black, white), num_pos) # draws dot number next to dot
            display_surface.blit(font.render(dot_num + ": " + x_coord + "in" + y_coord + "in", True, black, bg_color), coords_pos) # draws dot coords under image
            
            # draws line between every 2 points
            if (i+1)%2 == 0 and circles[i-1] != None:
                line = pygame.draw.line(display_surface, black, circles[i-1], circles[i])

                dist = str(round(math.dist(circles[i], circles[i-1]) * pxToIn, 2)) # finds distance between new dot and old dot in inches as a string

                display_surface.blit(font2.render(dist + "in", True, black, white), (line.center)) # draws distances between dots next to the center of the line


    # iterate over the list of Event objects that was returned by pygame.event.get() method.
    for event in pygame.event.get() :

        # handle MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos() # find position of mouse
            
            empty = True

            # loops through circles list to check for collition
            for i in range(len(circles)):
                if circles[i] != None and pos[0] > circles[i][0] - 5 and pos[0] < circles[i][0] + 5 and pos[1] > circles[i][1] - 5 and pos[1] < circles[i][1] + 5: # checks if mouse collides with a dot
                    circles[i] = None;  # sets position to none (this way the order is kept)
                    empty = False
            
            if empty and pos[0]<890 and pos[1]< 442: # no collistions and in bounds

                # loops for list to check for missingpoint to replace
                for i in range(len(circles)):
                    if circles[i] == None:
                        empty = False
                        circles[i] = pos
                        break

                # if no mising points, and a new one
                if empty and len(circles)<15:
                    circles.append(pos)

        # handle QUIT
        elif event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
  
        # Draws the surface object to the screen.  
        pygame.display.update() 
