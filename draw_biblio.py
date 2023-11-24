from PIL import Image, ImageDraw

WIDTH_BLOCK = 336  # mm
WIDTH_BEZEL = 20  # mm
WIDTH_LIBRARY = WIDTH_BEZEL * 5 + WIDTH_BLOCK * 4

class Game:
    def __init__(self, name, width, height, color):
        self.name = name
        self.width = width
        self.height = height
        self.color = color


def draw_library(draw):
    draw.rectangle((0,0,WIDTH_LIBRARY,WIDTH_LIBRARY), outline='orange', fill=None, width=WIDTH_BEZEL)
    for i in range(1,4):
        draw.rectangle((i*(WIDTH_BLOCK + WIDTH_BEZEL),0, i*(WIDTH_BLOCK + WIDTH_BEZEL) + WIDTH_BEZEL, WIDTH_LIBRARY), fill='brown')
        draw.rectangle((0, i*(WIDTH_BLOCK + WIDTH_BEZEL), WIDTH_LIBRARY, i * (WIDTH_BLOCK + WIDTH_BEZEL) + WIDTH_BEZEL), fill='brown')


def draw_game(draw, x, y, game, bloc_width):
    x_start = (x + 1) * WIDTH_BEZEL + x * WIDTH_BLOCK + bloc_width
    y_start = (y + 1) * WIDTH_BEZEL + (y + 1) * WIDTH_BLOCK
    draw.rectangle((x_start, y_start - game.height, x_start + game.width, y_start - 1), fill=game.color, outline='black', width=4)


def draw_games(draw, library):
    x, y = 0, 0
    for bloc in library:
        bloc_width = 0
        for game in bloc:
            draw_game(draw, x, y, game, bloc_width)
            bloc_width += game.width
        x += 1
        if x == 4:
            x = 0
            y += 1


def csv2dict(path):
    bg_dict = {}
    with open(path, "r") as f:
        skip_first = True
        for line in f.readlines():
            if skip_first:
                skip_first = False
                continue
            if not line.startswith('~'):
                item = line.split(";")
                bg_dict[item[0]] = [float(item[1]), float(item[2])]
    return find_relative_param(bg_dict)

def find_relative_param(bg_dict):
    bg_list = sorted(bg_dict.items(), key=lambda x: x[1][0])
    i = 0
    for element in bg_list:
        bg_dict[element[0]][0] = i
        i += 1
    return bg_dict

img = Image.new("RGBA", (WIDTH_LIBRARY, WIDTH_LIBRARY))
draw = ImageDraw.Draw(img)
draw_library(draw)

games = [
['Spirit Island', 'Power Grid', 'The 7th Continent', 'Near and Far'],
['Puerto Rico', 'Faiyum', 'Sleeping Gods: Kickstarter Edition', 'Aftermath'],
['Root', 'Everdell', 'Detective: A Modern Crime Board Game'],
["Aeon's End: Outcasts", 'Tidal Blades: Heroes of the Reef', 'Smartphone Inc.', 'Sherlock Holmes Consulting Detective: The Thames Murders & Other Cases'],
['Terraforming Mars', 'Earth', 'Wingspan', 'Fort', 'Pandemic'],
['Genotype: A Mendelian Genetics Game', 'Stardew Valley: The Board Game', 'Clank! In! Space!: A Deck-Building Adventure', 'Small World'],
['The Castles of Burgundy', 'The LOOP', 'Galaxy Trucker (Second Edition)', "It's a Wonderful World", '7 Wonders Duel'],
['Artisans of Splendent Vale', 'Photosynthesis', 'Verdant'],
['The Pursuit of Happiness', 'Stuffed Fables', 'Aquatica', 'Libertalia: Winds of Galecrest', 'Sky Team'],
['Gods Love Dinosaurs', 'Living Forest', 'Mysterium', 'Ticket to Ride', 'Fantasy Realms'],
['Fantastic Factories', 'PARKS', 'Scotland Yard', 'Splendor', 'Secret Hitler'],
['Harry Potter: Hogwarts Battle', 'Takenoko', 'Canvas', 'Project L', 'On Tour'],
['Carcassonne Big Box 6', 'Azul', 'Santorini', 'Patchwork', 'Kites'],
['Codenames: Duet', 'Celestia', 'Sushi Go Party!', 'So Clover!', 'Throw Throw Avocado']]

bg_dict = csv2dict("mod_collection.csv")

for i in range(len(games)):
    for j in range(len(games[i])):
        games[i][j] = Game(games[i][j], bg_dict[games[i][j]][1], 250, 'blue')

draw_games(draw, games)
img.show()