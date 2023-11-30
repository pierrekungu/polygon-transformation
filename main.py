# Import the important libraries
import turtle as T
import csv
import sys
from math import sin, cos, pi

# List to store polygon vertices including those for tranformed shapes
vertices = []

# List to store the initial polygon vertices to perfom transformation
initial_vertices = []

# Third element in the homogeneous coordinates and set to default value 1
S = 1

# Variable to keep track of mouse clicks
click_number = 0

# Create a custom size for the Turtle window size 
width = 1000
height = 600

# Initialize the Turtle graphics screen
window = T.Screen()
window.setup(width=width, height=height)
window.title("Polygon Transformation")

# Hide the turtle and set the speed to 0 (fastest)
T.hideturtle()
T.speed(-1)

# Function to wait for mouse clicks
def create_polygon_clicks():
    global initial_click

    # Initialize the first mouse click
    initial_click = True

    T.clear()

    # Display the message at the top
    T.pu()
    T.goto(0, height // 2 - 20)
    T.color("black")
    T.write("PRESS 'D' TO SAVE    RIGHT-CLICK MOUSE FOR MAIN MENU", align="center", font=("Arial", 12, "bold"))
    T.color("red")

    # Indicate the origin
    T.goto(0, 0)
    T.pd()
    T.dot(5)

    # Print the coordinates on the dot
    T.write(f"({0}, {0})", align="left", font=("Arial", 8, "normal"))

    # Create a window mainloop to allow for mouse and keyboard inputs
    T.listen()

    # Left mouse click to draw polygon
    T.onscreenclick(on_click_polygon, btn=1) 
    T.onkey(save_menu, 'd') 

    # Right mouse click to exit for main menu
    T.onscreenclick(on_exit, btn=3)    
    T.mainloop()

# Function to draw polygon from mouse clicks
def on_click_polygon(x, y):
    global initial_click
    global vertices
    global S
    
    if initial_click == True:
        vertices = []
        initial_click = False        

        # Move to the starting point
        T.pu()
        T.goto(x, y)
        T.pd()
        T.dot(5)

        # Print the coordinates on the dot
        T.write(f"({x}, {y})", align="left", font=("Arial", 8, "normal"))
    
    else:     
        # Draw a line and dot at the clicked position
        T.goto(x, y)
        T.dot(5)

        # Print the coordinates on the dot
        T.write(f"({x}, {y})", align="left", font=("Arial", 8, "normal"))

    # Store the coordinates
    vertex = {'x': x, 'y': y, 'S': S, 'type': 'straight'}
    vertices.append(vertex)

def on_exit(x, y):
    global initial_vertices
    global vertices

    # Store the initial vertices to perform tranformations
    initial_vertices = list(vertices)

    main()
    T.bye()
    sys.exit()
    
# Function to create a straight-line polygon one vertex at a time
def create_straight_polygon():
    global vertices
    global initial_vertices
    global S

    # Set variables to blank when the user wants to design a new polygon
    vertices = []
    initial_vertices = []

    # Set the color for drawing and clear the window
    T.color("red")
    T.clear()

    start = False

    while True:
        try:
            # Get vertex input from the user
            user_input = T.textinput("Vertex Input", "To save polygon, enter 'D' \nTo perform transformations, enter 'T' \n\nEnter vertex coordinates (x, y): ")

            # Load the the menu for blank input or user presses 'cancel'
            if not user_input:
                break

            elif user_input.lower() == 'd':
                save_menu()
                break

            # If user selects transformations
            elif user_input.lower() == 't':
                transformation_menu()
                break                    
            
            else:
                # Parse the input into x and y coordinates
                x, y = map(float, user_input.split(","))
                vertex = {'x': x, 'y': y, 'S': S, 'type': 'straight'}
                vertices.append(vertex)

                if not start:
                    # Draw a dot at the starting point
                    T.pu()
                    T.goto(x, y)
                    T.pd()
                    T.dot(5)

                    start = True

                else:
                    T.goto(x, y)
                    T.dot(5)

        except (ValueError, TypeError):
            print("Invalid input. Please enter coordinates as 'x, y'. Try again.")

    # Store the initial vertices to perform tranformation
    initial_vertices = list(vertices)

# Function to create a polygon with straight and curved lines (Bezier curve)
def create_bezier_polygon():
    global vertices
    global initial_vertices
    global S
    vertices = []

    T.clear()

    while True:
        try:
            # Get the user's choice for straight or curved line
            user_input = T.textinput("Selection Input", "Choose an option below \n(Note: Enter 'D' to save to file) \n\nS: Straight line \nC: Curved line")

            if not user_input:
                break

            if user_input.lower() == 'd':
                save_menu()
                break

            # Check user choice is valid
            if user_input.lower() not in ['s', 'c']:
                raise ValueError

            if user_input.lower() == 's':
                while True:
                    try:
                        # Get input for straight-line coordinates
                        coordinates = T.textinput("Vertices Input", "Enter start and end coordinates (x, y, x, y): ")

                        if not coordinates:
                            break

                        # Split the coordinates and store
                        coordinates = list(map(float, coordinates.split(",")))

                        # Create list for drawing the shape
                        bezier_vertices = []

                        vertex = {'x': 0, 'y': 0, 'S': S, 'type': 'transformation'}
                        vertices.append(vertex)

                        for i in range(0, len(coordinates), 2):
                            vertex = {'x': coordinates[i], 'y': coordinates[i + 1], 'S': S, 'type': 'straight'}
                            vertices.append(vertex)
                            bezier_vertices.append(vertex)
                        
                        draw_polygon(bezier_vertices, "red")
                        break

                    except (ValueError, TypeError):
                        print("Invalid input. Please enter coordinates as 'x, y, x, y'. Try again.")

            elif user_input.lower() == 'c':
                while True:
                    try:
                        # Get input for curved-line coordinates 
                        coordinates = T.textinput("Vertices Input [P0, P1, P2, P3]", "Enter four coordinates (x, y, x, y, x, y, x, y): ")

                        if not coordinates:
                            break

                        # Split the coordinates and store
                        coordinates = list(map(float, coordinates.split(",")))

                        # Create list for drawing the shape
                        bezier_vertices = []

                        vertex = {'x': 0, 'y': 0, 'S': S, 'type': 'transformation'}
                        vertices.append(vertex)

                        for i in range(0, len(coordinates), 2):
                            vertex = {'x': coordinates[i], 'y': coordinates[i + 1], 'S': S, 'type': 'curved'}
                            vertices.append(vertex)
                            bezier_vertices.append(vertex)
                        
                        draw_polygon(bezier_vertices, "red")
                        break                        

                    except (ValueError, TypeError):
                        print("Invalid input. Please enter coordinates as 'x, y, x, y'. Try again.")

        except (ValueError, TypeError):
            print("Invalid input. Please enter 's' for a straight line or 'c' for a curved line. Try again.")

    # Store the initial vertices to perform tranformations
    initial_vertices = list(vertices)

# Function to load a polygon from a file
def load_menu():
    global vertices
    global initial_vertices
    vertices = []

    while True:
        try:
            file_name = T.textinput("Load Polygon from File", "Enter the filename (without extension):")

            if not file_name:
                break
            
            with open(f'{file_name}.csv', 'r') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    vertices.append(row)

                T.clear()
                draw_polygon(vertices, "red")
                break

        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    # Store the initial vertices to perform transformation
    initial_vertices = list(vertices)

# Write the list of vertices to a CSV file
def save_polygon(file_name):
    global vertices
    try:
        with open(f'{file_name}.csv', 'w', newline='') as file:
            fieldnames = vertices[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()  
            for row in vertices:
                writer.writerow(row)

    except Exception as e:
        print(f"Error writing to file '{file_name}': {str(e)}")

# Menu for the save function
def save_menu():
    file_name = T.textinput("Save Polygon to File", "Enter the filename (without extension):")
    if file_name:
        save_polygon(file_name)

# Function to scale the polygon by (dx, dy)
def transform_polygon(dx=0, dy=0, angle=0, transformation='none', color='None'):    
    global vertices
    global initial_vertices
    get_center = True

    # Convert angle to radians
    angle = angle * pi / 180 

    # Indicate the start of the transformation 
    tf_vertices = [{'x': 0, 'y': 0, 'S': S, 'type': 'transformation'}]

    # Translate the polygon    
    for vertex in initial_vertices:
        x = float(vertex['x']) / float(vertex['S'])
        y = float(vertex['y']) / float(vertex['S'])
        shape = vertex['type']
        
        # Reflect the polygon in the X-axis
        if transformation == 'reflect_x':
            y = -y     

        # Reflect the polygon in the X-axis
        elif transformation == 'reflect_y':
            x = -x          
        
        # Rotate the polygon about the origin
        elif transformation == 'rotate':
            x_1 = x
            y_1 = y

            x = round(x_1 * cos(angle) - y_1 * sin(angle), 2)
            y = round(x_1 * sin(angle) + y_1 * cos(angle), 2)
               
        # Scale the polygon (Anchor point is the center of the polygon)
        elif transformation == 'scale':
            # Get coordinates for the center of the polygon
            if get_center:
                total_x = 0
                total_y = 0

                for vertex in initial_vertices:
                    total_x += float(vertex['x'])
                    total_y += float(vertex['y'])

                center_x = total_x / len(initial_vertices) 
                center_y = total_y / len(initial_vertices) 

                get_center = False

            #  Translate to anchor point
            x -= center_x
            y -= center_y

            # Perform scaling
            x = x * dx
            y = y * dy  

            # Translate to new position
            x =  x + center_x
            y =  y + center_y           

        # Translate the polygon
        elif transformation == 'translate':
            x = x + dx
            y = y + dy 
        
        # Store the new coordinates
        vertex = {'x': x, 'y': y, 'S': S, 'type': shape}
        tf_vertices.append(vertex)

    # Add the new vertices to the global variable
    vertices += tf_vertices

    draw_polygon(tf_vertices, color)

# Function to draw the polygon
def draw_polygon(vertices, color):
    T.color(color)
    T.pu()

    bezier_vertices = []

    for vertex in vertices:
        x = float(vertex['x']) / float(vertex['S'])
        y = float(vertex['y']) / float(vertex['S'])
        shape = vertex['type']
        
        # Check for teh start of transformation vertices
        if shape == 'transformation':
            T.pu()
            continue
        
        # When drawing a bezier curve
        elif shape == 'curved':
            bezier_vertices.append((x, y))
            if len(bezier_vertices) > 3:
                draw_curve(bezier_vertices, color)
                bezier_vertices = []

        # When drawing a straight line
        else:   
            T.goto(x, y)
            T.dot(5)
            T.pd()

# Function to draw curves
def draw_curve(P, color):
   # Draw the Bezier curve as 100 tiny segments
   T.pu()
   T.color(color)
   for i in range(101):
      t = i/100
      x = P[0][0]*(1-t)**3 + 3*P[1][0]*t*(1-t)**2 + 3*P[2][0]*t*t*(1-t) + P[3][0]*t**3
      y = P[0][1]*(1-t)**3 + 3*P[1][1]*t*(1-t)**2 + 3*P[2][1]*t*t*(1-t) + P[3][1]*t**3
      T.goto(x, y)
      T.pd()

def transformation_menu():
    while True:
        tf = T.numinput("Transformation", "1. Reflect (X Axis) \n2. Reflect (Y Axis) \n3. Rotate \n4. Scale \n5. Translate \n6. Save to file \n7. Exit", minval=1, maxval=7)

        if not tf:
            break

        if tf == 1:            
            transform_polygon(transformation='reflect_x', color='green')
        
        elif tf == 2:            
            transform_polygon(transformation='reflect_y', color='magenta')

        elif tf == 3:
            angle = T.numinput("Rotation", "Enter rotation angle (degrees)")
            if not angle:
                break

            transform_polygon(angle=angle, transformation='rotate', color='blue')                     

        elif tf == 4:
            while True:
                try:                
                    dx, dy = T.textinput("Scaling", "Enter scaling values (dx, dy): ").split(",")
                    transform_polygon(dx=float(dx), dy=float(dy), transformation='scale', color='purple')
                    break
                except (ValueError, TypeError):
                    print("Invalid input. Please enter numeric values for scaling. Try again.")  
                except(AttributeError):
                    break          
        
        elif tf == 5:
            while True:
                try:
                    dx, dy = T.textinput("Translation", "Enter translating values (dx, dy): ").split(",")
                    transform_polygon(dx=float(dx), dy=float(dy), transformation='translate', color='black')
                    break
                except (ValueError, TypeError):
                    print("Invalid input. Please enter numeric values for translation. Try again.")
                except(AttributeError):
                    break 

        elif tf == 6:
            save_menu()
            break

        elif tf == 7:
            break

def main():
    global vertices
    while True:
        try: 
            user_input = T.numinput("Menu", "1. Create Straight-Line Polygon \n2. Create Bezier Polygon \n3. Load Polygon \n4. Save Polygon \n5. Transform Polygon \n6. Exit",
                minval=1, maxval=6)
            
            if not user_input:
                break

            elif user_input == 1:
                while True:                
                    choice = T.numinput("Menu", "1. Keyboard \n2. Mouse Clicks", minval=1, maxval=2)
                    if not choice:
                        break
                
                    elif choice == 1:
                        create_straight_polygon()

                    elif choice == 2:
                        create_polygon_clicks() 
                        break                                           

            elif user_input == 2:
                create_bezier_polygon()

            elif user_input == 3:
                load_menu()

            elif user_input == 4:
                save_menu()

            elif user_input == 5:
                transformation_menu()

            elif user_input == 6:
                break
        
        except T.Terminator:
            user_input = None

if __name__ == "__main__":
    main()