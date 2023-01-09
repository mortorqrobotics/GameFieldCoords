from turtle import position
import pygame
import math

# activate the pygame library initiate pygame and give permission to use pygame's functionality.
pygame.init()
  
# define the RGB value for colors
bg_color = (200, 200, 200) # grey
black = (0,0,0)
white = (255,255,255)
  
# dimentions of screen in px (image dimentions are 1267 x 515)
image_width = 934
image_height = 459
screen_width = image_width + 120
screen_height = image_height + 120

# dimentions of the field in cm
field_width = 1654
field_height = 801

#conversions
pxToIn = (field_width/2.54)/image_width # (field of 1646 x 823 cm)
pxToFt = pxToIn/12
pxToCm = field_width/image_width
pxToM = pxToCm/100
conversions = [pxToIn, pxToFt, pxToCm, pxToM]
units = ["in", "ft", "cm", "m"]
conversion_mode = 0

# create the display surface object of specific dimension (X, Y).
display_surface = pygame.display.set_mode((screen_width, screen_height))
  
# set the pygame window name
pygame.display.set_caption('GameFieldCoords')
   
# create a surface object, image is drawn on it.
image = pygame.image.load('Screenshot 2023-01-08 211733.png')

#dot settings
circle_radius = 5
border_width = 0 # 0 = filled circle
circles = [] # list to hold circle positions and text

# create a font object
font = pygame.font.Font('freesansbold.ttf', 16) # style, size
font2 = pygame.font.Font('freesansbold.ttf', 12) # style, size

# line and arrow code
def draw_arrow(screen, colour, start, end):
    line = pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    point1 = (end[0]+10*math.sin(math.radians(rotation)), end[1]+10*math.cos(math.radians(rotation)))
    point2 = (end[0]+10*math.sin(math.radians(rotation-120)), end[1]+10*math.cos(math.radians(rotation-120)))
    point3 = (end[0]+10*math.sin(math.radians(rotation+120)), end[1]+10*math.cos(math.radians(rotation+120)))
    pygame.draw.polygon(screen, (0, 0, 0), (point1, point2, point3))
    return line

# infinite loop
while True :
  
    # completely fill the surface object with color
    display_surface.fill(bg_color)
  
    # display image
    display_surface.blit(image, (0, 0))

    if pygame.mouse.get_pos()[0] < image_width and pygame.mouse.get_pos()[1] < image_height:
        xUnit = round(pygame.mouse.get_pos()[0] * conversions[conversion_mode], 2) # mouse x pos in the current unit mode
        yUnit = round(pygame.mouse.get_pos()[1] * conversions[conversion_mode], 2) # mouse y pos in the current unit mode
        xPx = round(pygame.mouse.get_pos()[0], 2) # mouse x pos in px
        yPx = round(pygame.mouse.get_pos()[1], 2) # mouse y pos in px
    else:
        xUnit,yUnit,xPx,yPx = 0, 0, 0, 0

    # draws mouse position in the current unit mode
    display_surface.blit(font.render("x: " + str(xUnit) + units[conversion_mode], True, black, bg_color), (900,50))
    display_surface.blit(font.render("y: " + str(yUnit) + units[conversion_mode], True, black, bg_color), (900,75))

    # draws mouse position in px
    display_surface.blit(font.render("x: " + str(xPx) + "px", True, black, bg_color), (900,125))
    display_surface.blit(font.render("y: " + str(yPx) + "px", True, black, bg_color), (900,150))

    # draws conversion mode
    display_surface.blit(font.render("x: " + str(xPx) + "px", True, black, bg_color), (900,125))

    # loops through circles to display text and dots
    for i in range(len(circles)):

        if circles[i] != None:

            pygame.draw.circle(display_surface, black, circles[i], circle_radius, border_width) # draws each circle at the correct position

            dot_num = str(i+1) # finds the current dt number as a string

            # finds x and y values for field position in the current unit mode as a string
            x_coord = str(round(circles[i][0] * conversions[conversion_mode], 2))
            y_coord = str(round(circles[i][1] * conversions[conversion_mode], 2))

            coords_pos = (50 + 180 * (int)(i/3) , 450 + 40 * (i%3)) # position of text under image
            num_pos = (circles[i][0] + 5, circles[i][1] + 5) # position of number next to dot

            display_surface.blit(font2.render(dot_num, True, black, white), num_pos) # draws dot number next to dot
            display_surface.blit(font.render(dot_num + ": " + x_coord + units[conversion_mode] + y_coord + units[conversion_mode], True, black, bg_color), coords_pos) # draws dot coords under image
            
            # draws line between every 2 points
            if (i+1)%2 == 0 and circles[i-1] != None:

                line = draw_arrow(display_surface, black, circles[i-1], circles[i]) # calls the function to draw a line and arrow

                dist = str(round(math.dist(circles[i], circles[i-1]) * conversions[conversion_mode], 2)) # finds distance between new dot and old dot in the current unit mode as a string

                display_surface.blit(font2.render(dist + units[conversion_mode], True, black, white), (line.center)) # draws distances between dots next to the center of the line


    # iterate over the list of Event objects that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # handle MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos() # find position of mouse
            
            empty = True

            # loops through circles list to check for collition
            for i in range(len(circles)):
                 # checks if mouse collides with a dot, if dot exists, and if the left click button is used
                if event.button == 3 and circles[i] != None and pos[0] > circles[i][0] - 5 and pos[0] < circles[i][0] + 5 and pos[1] > circles[i][1] - 5 and pos[1] < circles[i][1] + 5:
                        circles[i] = None;  # sets position to none (this way the order is kept)
                        empty = False
            
            if empty and pos[0]<image_width and pos[1]< image_height and event.button == 1: # no collistions, right click, and in bounds

                # loops for list to check for missingpoint to replace
                for i in range(len(circles)):
                    if circles[i] == None:
                        empty = False
                        circles[i] = pos
                        break

                # if no mising points, and a new one
                if empty and len(circles)<15:
                    circles.append(pos)
            elif event.button == 2:
                if conversion_mode<3:
                    conversion_mode += 1
                else:
                    conversion_mode = 0

        # handle QUIT
        elif event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
  
        # Draws the surface object to the screen.  
        pygame.display.update() 
