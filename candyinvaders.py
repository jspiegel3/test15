# Candy Invaders – Student Starter Code V2 PA6
#
# YOUR NAME : Baila Kestenbaum
#
# GOAL:
#   Practice lists and list comprehensions using a simple falling-candy game.
#
# SCORING (HYBRID):
#   - If the mouth eats a candy: player gains that candy's point value.
#   - If a candy goes off-screen (row >= NUM_ROWS): computer gains +1.
#
# DATA MODEL:
#   candies is a list of tuples in this EXACT order:
#       (row, col, color, shape, points)
#
# PLEASE NOTE:
#   To play the game, you must click on the game board to give it focus.
# 

import simplegui
import random


# --- CONFIGURATION CONSTANTS ---

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 40

NUM_COLS = WIDTH // CELL_SIZE
NUM_ROWS = HEIGHT // CELL_SIZE
MOUTH_ROW = NUM_ROWS - 1

# Rainbow palette (hex colors)
CANDY_COLORS = ["#ff0000", "#ff8700", "#ffd300", "#deff0a", "#a1ff0a",
                "#0aefff", "#147df5", "#580aff", "#be0aff"]

# Shapes available
SHAPES = ["circle", "square", "triangle"]

# Candy point values
POINT_VALUES = [1, 2, 3]

SPAWN_PROB = 0.2
TIMER_INTERVAL = 200  # ms


# --- GAME STATE (GLOBALS) ---

# candies is a list of tuples.  Each tuple consists of (row, col, color, shape, points) - always in this order
candies = []

# which column the mouth is currently in
mouth_col = NUM_COLS // 2

# scores
player_score = 0
computer_score = 0


# --- LOGIC HELPERS (YOUR LIST / LIST-COMP WORK LIVES HERE) ---


def spawn_candy():
    """
    Possibly add a new candy at the top of the board.

    Candy tuple format (EXACT ORDER):
        (row, col, color, shape, points)

    Behavior:
        - With probability SPAWN_PROB:
            - choose a random column (0..NUM_COLS-1)
            - choose a random color from CANDY_COLORS
            - choose a random shape from SHAPES
            - choose a random point value from POINT_VALUES
        - append the new candy tuple at row 0 to candies

    Notes about globals:
        - You do NOT need 'global candies' here if you only use append(),
          because you are mutating the list, not rebinding it.

    TODO:
        - Implement this function.
    """
    # TODO: spawn a new candy with some probability
    if random.random() < SPAWN_PROB:
        row = 0
        col = random.randint(0, NUM_COLS - 1)
        color = random.choice(CANDY_COLORS)
        shape = random.choice(SHAPES)
        points = POINT_VALUES[SHAPES.index(shape)]
        candies.append((row, col, color, shape, points))


def move_candies_down():
    """
    Move all candies down by one row.

    Behavior:
        - For each candy (r, c, color, shape, pts) in candies,
          its new position should be (r + 1, c, color, shape, pts).

    GOAL:
        - Rebuild the candies list using a list comprehension.

    NOTE:
        - We use 'or 'global candies' here because we will REASSIGN candies
          at the end (candies = new_candies). Reassigning a global variable
          inside a function requires the global keyword.

    TODO:
        - Use a list comprehension to build the updated list.
        - Assign the updated list back to candies.
    """
    global candies
    # TODO: rebuild candies so every candy moves down 1 row
    candies = [(r + 1, c, color, shape, pts) for (r, c, color, shape, pts) in candies]


def eat_and_filter_candies():
    """
    Remove candies that are off-screen or eaten, and update scores.

    Definitions:
        - EATEN candy:
              r == MOUTH_ROW and c == mouth_col
        - OFF-SCREEN candy:
              r >= NUM_ROWS

    Scoring (HYBRID):
        - Player gains the candy's point value when eaten.
        - Computer gains +1 for each candy that goes off-screen.

    Goals:
        - Use list comprehensions for filtering and rebuilding lists.

    TODO:
        1) Build a list of eaten candies using a list comprehension.
        2) Increase player_score by the SUM of points of eaten candies.
        3) Count how many candies escaped (r >= NUM_ROWS) and add that count
           to computer_score.
        4) Rebuild candies so it keeps only candies that:
             - are still on-screen (r < NUM_ROWS)
             - are NOT eaten at the mouth position
    """
    global candies, player_score, computer_score

    # TODO 1: list of eaten candies
    eaten_candies = [(r, c, color, shape, pts) for (r, c, color, shape, pts)
                     in candies if r == MOUTH_ROW and c == mouth_col]

    # TODO 2: update player_score (sum of points eaten)
    player_score += sum(pts for (r, c, color, shape, pts) in eaten_candies)

    # TODO 3: update computer_score (+1 per escaped candy)
    escaped_candies = [(r, c, color, shape, pts) for (r, c, color, shape, pts)
                       in candies if r >= NUM_ROWS]
    computer_score += len(escaped_candies)

    # TODO 4: rebuild candies (remove eaten + off-screen)
    candies = [(r, c, color, shape, pts) for (r, c, color, shape, pts) 
               in candies if r < NUM_ROWS and not (r == MOUTH_ROW and c == mouth_col)]
               


def update():
    """
    One game "tick" called by the timer.

    Behavior:
        - Move all candies down.
        - Eat/filter candies and update scores.
        - Possibly spawn a new candy at the top.

    TODO:
        - Call move_candies_down()
        - Call eat_and_filter_candies()
        - Call spawn_candy()
    """
    # TODO: call the helper functions in the correct order
    move_candies_down()
    eat_and_filter_candies()
    spawn_candy()
               

# --- DRAW HELPERS ---


def row_col_to_xy(row, col):
    """
    Convert (row, col) to the pixel (x, y) center of that cell.

    Returns:
        (x, y) tuple representing the center of the cell.
    """
    x = col * CELL_SIZE + CELL_SIZE / 2
    y = row * CELL_SIZE + CELL_SIZE / 2
    return x, y


def draw_grid(canvas):
    """
    OPTIONAL:
    Draw grid lines so you can see the cells.
    """
    # TODO (optional): draw vertical lines
    # TODO (optional): draw horizontal lines
    pass


def draw_candy_shape(canvas, x, y, color, shape):
    """
    OPTIONAL helper:
    Draw a candy centered at (x, y) using the given color and shape.

    You can use this helper, or draw shapes directly in draw_candies().

    TODO (optional):
        - Draw a circle for "circle"
        - Draw a square for "square"
        - Draw a triangle for "triangle"
    """
    # TODO (optional): implement shapes
    half = CELL_SIZE / 2 * 0.8  # candy slightly smaller than cell

    if shape == "circle":
        canvas.draw_circle((x, y), half, 1, color, color)
    elif shape == "square":
        canvas.draw_polygon([(x - half, y - half),
                             (x + half, y - half),
                             (x + half, y + half),
                             (x - half, y + half)],
                            1, color, color)
    elif shape == "triangle":
        canvas.draw_polygon([(x, y - half),
                             (x - half, y + half),
                             (x + half, y + half)],
                            1, color, color)



def draw_candies(canvas):
    """
    Draw each candy.

    Reads from:
        candies list of (row, col, color, shape, points)

    TODO:
        - Loop over candies and unpack (r, c, color, shape, pts)
        - Convert row/col to x,y using row_col_to_xy()
        - Draw the candy in its shape and color
        - (Optional) draw the point value on top of the candy
    """
    # TODO: draw candies
    for (r, c, color, shape, pts) in candies:
        x, y = row_col_to_xy(r, c)
        draw_candy_shape(canvas, x, y, color, shape)


def draw_mouth(canvas):
    """
    Draw the mouth as a rectangle on the bottom row.

    This is completed for you, but you may customize it.
    """
    x_center, y_center = row_col_to_xy(MOUTH_ROW, mouth_col)
    w = CELL_SIZE * 0.85
    h = CELL_SIZE * 0.45
    half_w = w / 2
    half_h = h / 2

    canvas.draw_polygon(
        [(x_center - half_w, y_center - half_h),
         (x_center + half_w, y_center - half_h),
         (x_center + half_w, y_center + half_h),
         (x_center - half_w, y_center + half_h)],
        3, "#ff70a6", "#db3069"
    )


# --- EVENT HANDLERS ---


def draw(canvas):
    """
    Main draw handler.

    Draws:
        - background
        - grid (optional)
        - candies
        - mouth
        - scoreboard
    """
    # background of game
    canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)],
                        1, "Black", "Black")

    # TODO these functions have to be implemented by you 
    draw_grid(canvas)
    draw_candies(canvas)
    
    # Completed code 
    draw_mouth(canvas)

    # TODO draw Scoreboard 
    canvas.draw_text(f"Player score: {player_score}", (10, 20), 18, "White")
    canvas.draw_text(f"Computer score: {computer_score}", (150, 20), 18, "White")
    

def keydown(key):
    """
    Move the mouth left/right with arrow keys.
    Keep the mouth on screen using min/max.
    Completed code 
    """
    global mouth_col
    if key == simplegui.KEY_MAP["left"]:
        mouth_col = max(0, mouth_col - 1)
    elif key == simplegui.KEY_MAP["right"]:
        mouth_col = min(NUM_COLS - 1, mouth_col + 1)


def new_game():
    """
    Reset the game state.

    Sets:
        - candies to empty list
        - mouth_col to center
        - scores to 0
        
    Completed Code
    """
    global candies, mouth_col, player_score, computer_score
    candies = []
    mouth_col = NUM_COLS // 2
    player_score = 0
    computer_score = 0


# --- SETUP FRAME & TIMER (DO NOT CHANGE THIS PART) ---

# This section contains Completed Code
frame = simplegui.create_frame("Candy Invaders", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

timer = simplegui.create_timer(TIMER_INTERVAL, update)

frame.add_button("New Game", new_game, 100)

new_game()
timer.start()
frame.start()