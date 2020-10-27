import tkinter as tk 
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
}

INVESTIGATE = "I"
QUIT = "Q"
HELP = "H"

VALID_ACTIONS = [INVESTIGATE, QUIT, HELP, *DIRECTIONS.keys()]

HELP_MESSAGE = f"Here is a list of valid actions: {VALID_ACTIONS}"

INVALID = "That's invalid."

WIN_TEXT = "You have won the game with your strength and honour!"

LOSE_TEST = "You have lost all your strength and honour."
LOSE_TEXT = "You have lost all your strength and honour."

# New Constant in Assignment_3
TASK_ONE = "1"
TASK_TWO = "2"
TASK_THREE = "3"

GAME_TITLE = "Key Cave Adventure Game"
BANNER = "Key Cave Adventure Game"
WALL_TEXT = ""
IBIS_TEXT = "Ibis"
TRASH_TEXT = "Trash"
BANANA_TEXT = "Banana"
NEST_TEXT = "Nest"

BANNER_COLOR = "medium spring green"
WALL_COLOR = "dark grey"
IBIS_COLOR = "medium spring green"
BANANA_COLOR = "orange"
TRASH_COLOR = "yellow"
NEST_COLOR = "red"
BG_COLOR = "light grey"

W_TEXT = "N"
A_TEXT = "W"
S_TEXT = "S"
D_TEXT = "E"

STATUS_BAR_HEIGHT = 100
BUTTON_NEW_TEXT = "New game"
BUTTON_QUIT_TEST = "Quit"

IMAGE_DIR = "images/"
IMAGE_CLOCK = IMAGE_DIR + "clock.gif"
IMAGE_DOOR = IMAGE_DIR + "door.gif"
IMAGE_EMPTY = IMAGE_DIR + "empty.gif"
IMAGE_KEY = IMAGE_DIR + "key.gif"
IMAGE_LIGHTNING = IMAGE_DIR + "lightning.gif"
IMAGE_LIVES = IMAGE_DIR + "lives.gif"
IMAGE_MOVE_INCREASE = IMAGE_DIR + "moveIncrease.gif"
IMAGE_PLAYER = IMAGE_DIR + "player.gif"
IMAGE_WALL = IMAGE_DIR + "wall.gif"

TIMER_TEXT_1 = "Time elapsed"
TIMER_TEXT_2 = "%dm %ds"
COUNTER_TEXT_1 = "Moves Left"
COUNTER_TEXT_2 = "%d moves remaining"

# View Classes
class AbstractGrid(tk.Canvas):
    def __init__(self, master, rows, cols, width, height, **kwargs):
        super().__init__(master=master, width=width, height=height)
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._cell_width = self._width // self._cols
        self._cell_height = self._height // self._rows

    def get_bbox(self, position): 
        # Returns the bounding box for the (row, col) position.
        pass

    def pixel_to_position(self, pixel):
        # Converts the x, y pixel position (in graphics units) to a (row, col) position.
        x, y = pixel
        return (int)(x / self._cell_width), (int)(y / self._cell_height)


    def get_position_center(self, position): 
        # Gets the graphics coordinates for the center of the cell at the given (row, col) position.
        col, row = position
        return  (int)(self._cell_width*(col+0.5)), (int)(self._cell_height*(row+0.5))

    def annotate_position(self, position, text): 
        # Annotates the cell at the given (row, col) position with the provided text.
        self.create_text(self.get_position_center(position), text = text)

class DungeonMap(AbstractGrid):
    def __init__(self, master, size, width = 600, **kwargs):
        super().__init__(master, rows = size, cols = size, width = width, height = width, kwargs = kwargs)
        self._dungeon_size = size
        self.config(bg = BG_COLOR)

    def draw_grid(self, dungeon, player_position): 
        # Draws the dungeon on the DungeonMap based on dungeon, and draws the player at the specied (row, col) position.
        self.delete(tk.ALL)
        for i in range(self._dungeon_size):
            for j in range(self._dungeon_size):
                position = (i, j)
                x = j * self._cell_width
                y = i * self._cell_height
                entity = dungeon.get(position)
                draw = False
                if entity is not None:
                    draw = True
                    char = entity.get_id()
                    if(char == KEY):
                        color = TRASH_COLOR
                        text = TRASH_TEXT
                    elif(char == DOOR):
                        color = NEST_COLOR
                        text = NEST_TEXT
                    elif(char == WALL):
                        color = WALL_COLOR
                        text = WALL_TEXT
                    elif(char == MOVE_INCREASE):
                        color = BANANA_COLOR
                        text = BANANA_TEXT
                if position == player_position:
                    draw = True
                    color = IBIS_COLOR
                    text = IBIS_TEXT
                if(draw):
                    self.create_rectangle(x, y, x+self._cell_width, y+self._cell_height, fill = color)
                    self.annotate_position((j, i), text = text)

class KeyPad(AbstractGrid):
    def __init__(self, master, width=200, height=100, **kwargs):
        super().__init__(master, rows = 2, cols = 3, width = width, height = height, kwargs = kwargs)
        # draw buttons
        self.create_rectangle(self._cell_width, 0, self._cell_width*2, self._cell_height, fill = "dark gray")
        self.create_rectangle(0, self._cell_height, self._cell_width, self._cell_height*2, fill = "dark gray")
        self.create_rectangle(self._cell_width, self._cell_height, self._cell_width*2, self._cell_height*2, fill = "dark gray")
        self.create_rectangle(self._cell_width*2, self._cell_height, self._cell_width*3, self._cell_height*2, fill = "dark gray")
        self.annotate_position((1, 0), text = W_TEXT)
        self.annotate_position((0, 1), text = A_TEXT)
        self.annotate_position((1, 1), text = S_TEXT)
        self.annotate_position((2, 1), text = D_TEXT)

    def pixel_to_direction(self, pixel): 
        #Converts the x, y pixel position to the direction of the arrow depicted at that position
        col, row = self.pixel_to_position(pixel) # the input order should be x to y
        if(row == 0 and col == 1):
            return "W"
        elif(row == 1 and col == 0):
            return "A"
        elif(row == 1 and col == 1):
            return "S"
        elif(row == 1 and col == 2):
            return "D"
        else:
            return None

class AdvancedDungeonMap(DungeonMap):
    def __init__(self, master, size, width = 600, **kwargs):
        super().__init__(master, size = size, width = width, kwargs = kwargs)
        self._dungeon_size = size
        self.config(bg = BG_COLOR)
        self._image_door = ImageTk.PhotoImage(Image.open(IMAGE_DOOR).resize((self._cell_height, self._cell_width)))
        self._image_empty = ImageTk.PhotoImage(Image.open(IMAGE_EMPTY).resize((self._cell_height, self._cell_width)))
        self._image_key = ImageTk.PhotoImage(Image.open(IMAGE_KEY).resize((self._cell_height, self._cell_width)))
        self._image_move_increase = ImageTk.PhotoImage(Image.open(IMAGE_MOVE_INCREASE).resize((self._cell_height, self._cell_width)))
        self._image_player = ImageTk.PhotoImage(Image.open(IMAGE_PLAYER).resize((self._cell_height, self._cell_width)))
        self._image_wall = ImageTk.PhotoImage(Image.open(IMAGE_WALL).resize((self._cell_height, self._cell_width)))

    def draw_grid(self, dungeon, player_position): 
        # Draws the dungeon on the DungeonMap based on dungeon, and draws the player at the specied (row, col) position.
        self.delete(tk.ALL)
        for i in range(self._dungeon_size):
            for j in range(self._dungeon_size):
                position = (i, j)
                x, y = self.get_position_center((j,i))
                entity = dungeon.get(position)
                self.create_image(x, y, image = self._image_empty)
                draw = False
                if entity is not None:
                    draw = True
                    char = entity.get_id()
                    if(char == KEY):
                        image = self._image_key
                    elif(char == DOOR):
                        image = self._image_door
                    elif(char == WALL):
                        image = self._image_wall
                    elif(char == MOVE_INCREASE):
                        image = self._image_move_increase
                if(draw):
                    self.create_image(x, y, image = image)
                if position == player_position:
                    self.create_image(x, y, image = self._image_player)

class StatusBar(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master=master, height=STATUS_BAR_HEIGHT)
        self._master = master
        self._app = app
        # open images
        self._image_timer = ImageTk.PhotoImage(Image.open(IMAGE_CLOCK).resize((100, 100)))
        self._image_lightning = ImageTk.PhotoImage(Image.open(IMAGE_LIGHTNING).resize((100, 100)))
        self._sec = 0
        self._count = 0
        self._timer_text_2 = tk.StringVar()
        self._counter_text_2 = tk.StringVar()
        self.update_timer()
        self.update_counter()
        self.draw_buttons()
        self.draw_timer()
        self.draw_counter()

    def update_timer(self, sec = 0):
        self._timer_text_2.set(TIMER_TEXT_2 % (sec//60, sec%60))
    def update_counter(self, count = 0):
        self._counter_text_2.set(COUNTER_TEXT_2 % (count))

    def draw_buttons(self):
        # buttons frame
        self._buttons = tk.Frame(self, width=200)
        self._buttons.pack_propagate(0)
        self._buttons.pack(side=tk.LEFT, fill=tk.Y)
        self._buttons_inner_up = tk.Frame(self._buttons)
        self._buttons_inner_up.pack(expand=1)
        self._buttons_inner = tk.Frame(self._buttons)
        self._buttons_inner.pack()
        self._buttons_inner_down = tk.Frame(self._buttons)
        self._buttons_inner_down.pack(expand=1)
        self._button_new = tk.Button(self._buttons_inner, text=BUTTON_NEW_TEXT, command = self._app.new)
        self._button_new.pack(expand=1)
        self._button_quit = tk.Button(self._buttons_inner, text=BUTTON_QUIT_TEST, command = self._app.quit)
        self._button_quit.pack(expand=1)
    def draw_timer(self):
        # timer frame
        self._timer = tk.Frame(self)
        self._timer.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self._timer_inner_up = tk.Frame(self._timer)
        self._timer_inner_up.pack(expand=1)
        self._timer_inner = tk.Frame(self._timer)
        self._timer_inner.pack(fill=tk.X)
        self._timer_inner_down = tk.Frame(self._timer)
        self._timer_inner_down.pack(expand=1)
        self._timer_pic = tk.Label(self._timer_inner, image = self._image_timer)
        self._timer_pic.pack(side=tk.LEFT)
        self._timer.pack(side=tk.LEFT)
        self._timer_texts = tk.Frame(self._timer_inner)
        self._timer_texts.pack(side=tk.LEFT)
        self._timer_text_up = tk.Label(self._timer_texts, text = TIMER_TEXT_1)
        self._timer_text_up.pack()
        self._timer_text_down = tk.Label(self._timer_texts, textvariable = self._timer_text_2)
        self._timer_text_down.pack()
    def draw_counter(self):
        # counter frame
        self._counter = tk.Frame(self)
        self._counter.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self._counter_inner_up = tk.Frame(self._counter)
        self._counter_inner_up.pack(expand=1)
        self._counter_inner = tk.Frame(self._counter)
        self._counter_inner.pack(fill=tk.X)
        self._counter_inner_down = tk.Frame(self._counter)
        self._counter_inner_down.pack(expand=1)
        self._counter_pic = tk.Label(self._counter_inner, image = self._image_lightning)
        self._counter_pic.pack(side=tk.LEFT)
        self._counter.pack(side=tk.LEFT)
        self._counter_texts = tk.Frame(self._counter_inner)
        self._counter_texts.pack(side=tk.LEFT)
        self._counter_text_up = tk.Label(self._counter_texts, text = COUNTER_TEXT_1)
        self._counter_text_up.pack()
        self._counter_text_down = tk.Label(self._counter_texts, textvariable = self._counter_text_2)
        self._counter_text_down.pack()
    def draw_lives(self):
        # lives frame 
        pass

def load_game(filename):
    """Create a 2D array of string representing the dungeon to display.
    
    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the 
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            dungeon_layout.append(list(line))

    return dungeon_layout


class Entity:
    """ """

    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with
        """
        self._collidable = True

    def get_id(self):
        """ """
        return self._id

    def set_collide(self, collidable):
        """ """
        self._collidable = collidable

    def can_collide(self):
        """ """
        return self._collidable

    def __str__(self):
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        return str(self)


class Wall(Entity):
    """ """

    _id = WALL
    
    def __init__(self):
        """ """
        super().__init__()
        self.set_collide(False)


class Item(Entity):
    """ """
    def on_hit(self, game):
        """ """
        raise NotImplementedError


class Key(Item):
    """ """
    _id = KEY
    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())


class MoveIncrease(Item):
    """ """

    _id = MOVE_INCREASE

    def __init__(self, moves=5):
        """ """
        super().__init__()
        self._moves = moves

    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.change_move_count(self._moves)
        game.get_game_information().pop(player.get_position())


class Door(Entity):
    """ """
    _id = DOOR

    def on_hit(self, game):
        """ """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game.set_win(True)
                return

        print("You don't have the key!")


class Player(Entity):
    """ """

    _id = PLAYER

    def __init__(self, move_count):
        """ """
        super().__init__()
        self._max_move = move_count
        self._move_count = move_count
        self._inventory = []
        self._position = None

    def reset_move_count(self):
        self._move_count = self._max_move
    
    def set_move_count(self, move_count):
        self._move_count = move_count

    def set_position(self, position):
        """ """
        self._position = position

    def get_position(self):
        """ """
        return self._position

    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number

    def moves_remaining(self):
        """ """
        return self._move_count

    def add_item(self, item):
        """Adds item (Item) to inventory
        """
        self._inventory.append(item)

    def get_inventory(self):
        """ """
        return self._inventory

    def has_key(self):
        for item in self.get_inventory():
            if item.get_id() == KEY:
                return True
        return False

class GameLogic:
    """ """
    def __init__(self, dungeon_name="game1.txt"):
        """ """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False
        self._time = 0

    def get_positions(self, entity):
        """ """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def init_game_information(self):
        """ """
        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)
        
        self._player.set_position(player_pos)
        self._player.reset_move_count()

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information
    
    def restore_game_information(self):
        """ """
        # there may be no key left
        key_position = self.get_positions(KEY)
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)

        information = {
            door_position: Door(),
        }

        for key in key_position:
            information[key] = Key()

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

    def get_player(self):
        """ """
        return self._player

    def get_entity(self, position):
        """ """
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """ """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self):
        """ """
        return self._game_information

    def get_dungeon_size(self):
        """ """
        return self._dungeon_size

    def move_player(self, direction):
        """ """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): a direction for the player to travel in.

        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True
        
        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)

    def new_position(self, direction):
        """ """
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """ """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """ """
        self._win = win

    def won(self):
        """ """
        return self._win

    def time_increase(self):
        self._time += 1
    
    def get_time(self):
        return self._time

    def set_time(self, time):
        self._time = time

    def load_dongeon(self, dungeon_size, dungeon):
        self._dungeon_size = dungeon_size
        dungeon_layout = []
        for line in dungeon:
            line = line.strip()
            dungeon_layout.append(list(line))
        self._dungeon = dungeon_layout
        self._game_information = self.restore_game_information()
        self._win = False

# Controller
class GameApp:
    """ """
    def __init__(self, master, task, dungeon_name):
        """ """
        self._master = master
        self._task = task
        self._dungeon_name = dungeon_name
        self._game = GameLogic(dungeon_name=dungeon_name)
        # Connect to Views
        self._master.title(GAME_TITLE)
        self._frame1 = tk.Frame(self._master)
        self._frame1.pack(fill=tk.X)
        self._banner = tk.Label(self._frame1, text=BANNER, font=("Arial", 20), bg='medium spring green')
        self._banner.pack(fill=tk.X)
        self._frame2 = tk.Frame(self._master)
        self._frame2.pack(fill=tk.X)
        # init dungeon map
        if self._task == TASK_ONE:
            self._dungeon_map = DungeonMap(self._frame2, self._game.get_dungeon_size())
        elif self._task == TASK_TWO:
            self._dungeon_map = AdvancedDungeonMap(self._frame2, self._game.get_dungeon_size())
        self._dungeon_map.pack(side = tk.LEFT)
        self._dungeon_map.draw_grid(self._game.get_game_information(), self._game.get_player().get_position())
        # init key pad
        self._key_pad = KeyPad(self._frame2)
        self._key_pad.pack(expand=1)
        self._key_pad.bind("<Button-1>", self.press_button)
        self._master.bind("<Key>", self.key_press)
        # init status bar
        if self._task == TASK_TWO:
            self._status_bar = StatusBar(self._master, self)
            self._status_bar.pack_propagate(0)
            self._status_bar.pack(fill=tk.X)
            self._status_bar.update_counter(self._game.get_player().moves_remaining())
        # init menu bar
        if self._task == TASK_TWO:
            self._menubar = tk.Menu(self._master)
            self._master.config(menu=self._menubar) # tell master what its menubar is
            # within the menu bar create the file menu
            self._filemenu = tk.Menu(self._menubar)
            self._menubar.add_cascade(label="File", menu=self._filemenu) # tell menubar what its menu is 
            # within the file menu create the file processing options
            self._filemenu.add_command(label="Save game", command=self.save)
            self._filemenu.add_command(label="Load game", command=self.load)
            self._filemenu.add_command(label="New game", command=self.new)
            self._filemenu.add_command(label="Quit", command=self.quit)
        self._master.after(1000, self.time_increase)

    def press_button(self, pixel):
        # when you press a button on the key pad
        dir = self._key_pad.pixel_to_direction((pixel.x, pixel.y))
        self.move(dir)
    
    def key_press(self, key):
        # when you press a key on the keyboard
        dir = key.char.upper()
        self.move(dir)

    def move(self, direction):
        if direction in DIRECTIONS:
            # if player does not collide move them
            if not self._game.collision_check(direction):
                self._game.move_player(direction)
                entity = self._game.get_entity(self._game.get_player().get_position())

                # process on_hit and check win state
                if entity is not None:
                    entity.on_hit(self._game)
            else:
                print(INVALID)
            self._game.get_player().change_move_count(-1)
            if self._task == TASK_TWO:
                self._status_bar.update_counter(self._game.get_player().moves_remaining())
        else:
            print(INVALID)
        self._dungeon_map.draw_grid(self._game.get_game_information(), self._game.get_player().get_position())
        if self._game.won():
            # print(WIN_TEXT)
            self.win()
        if self._game.check_game_over():
            # print(LOSE_TEST)
            self.lose()

    def save(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            fd = open(filename, 'w')
            file_text = ""
            # save player
            x,y = self._game.get_player().get_position()
            steps = self._game.get_player().moves_remaining()
            has_key = self._game.get_player().has_key()
            file_text += str(x) + "\n"
            file_text += str(y) + "\n"
            file_text += str(steps) + "\n"
            file_text += str(has_key) + "\n"
            # save time
            time = self._game.get_time()
            file_text += str(time) + "\n"
            # save map
            dungeon_size = self._game.get_dungeon_size()
            file_text += str(dungeon_size) + "\n"
            dungeon = ""
            game_information = self._game.get_game_information()
            for i in range(dungeon_size):
                rows = ""
                for j in range(dungeon_size):
                    position = (i, j)
                    entity = game_information.get(position)
                    if entity is not None:
                        char = entity.get_id()
                    else:
                        char = SPACE
                    rows += char
                rows += "\n"
                dungeon += rows
            file_text += dungeon
            fd.write(file_text)
            fd.close()

    def load(self):
        filename = filedialog.askopenfilename()
        if filename:
            fd = open(filename, 'r')
            file_lines = fd.readlines()
            # get the informations
            i = 0
            x = int(file_lines[i][:-1])
            i += 1
            y = int(file_lines[i][:-1])
            i += 1
            steps = int(file_lines[i][:-1])
            i += 1
            has_key = file_lines[i][:-1] == "True"
            i += 1
            time = int(file_lines[i][:-1])
            i += 1
            dungeon_size = int(file_lines[i][:-1])
            i += 1
            dungeon = file_lines[i : i + dungeon_size]
            # load the information
            self._game.get_player().set_position((x, y))
            self._game.get_player().set_move_count(steps)
            if has_key:
                self._game.get_player().add_item(Key())
            self._game.set_time(time)
            self._game.load_dongeon(dungeon_size, dungeon)
            self.refresh_all()
            fd.close()

    def reset(self):
        self._game = GameLogic(dungeon_name=self._dungeon_name)
        self.refresh_all()

    def new(self):
        ans = tkinter.messagebox.askyesno('Verify restart', 'Would you like to restart?')
        if ans:
            self.reset()

    def quit(self):
        ans = tkinter.messagebox.askyesno('Verify exit', 'Would you like to quit?')
        if ans:
            self._master.destroy()
    
    def win(self):
        ans = tkinter.messagebox.askyesno('You Won!', 'You have finished the level with a score of %d \n\nWould you like to play again?' % self._game.get_time())
        if ans:
            self.reset()
        else:
            self._master.destroy()

    def lose(self):
        ans = tkinter.messagebox.askyesno('You Lost :(', 'You just lost the game :( \n\nWould you like to play again?')
        if ans:
            self.reset()
        else:
            self._master.destroy()
        
    def time_increase(self):
        self._game.time_increase()
        self._status_bar.update_timer(self._game.get_time())
        self._master.after(1000, self.time_increase)

    def refresh_all(self):
        self._dungeon_map.draw_grid(self._game.get_game_information(), self._game.get_player().get_position())
        if self._task == TASK_TWO:
            self._status_bar.update_counter(self._game.get_player().moves_remaining())
            self._status_bar.update_timer(self._game.get_time())

            
def main():
    root = tk.Tk()
    GameApp(root, task = TASK_TWO, dungeon_name = "game2.txt")
    root.mainloop()


if __name__ == "__main__":
    main()
