import itertools

import numpy as np

WIDTH = 336  # mm
TOLERANCE = 2  # mm


def csv2dict(path):
    bg_dict = {}
    with open(path, "r") as f:
        skip_first = True
        for line in f.readlines():
            if skip_first:
                skip_first = False
                continue
            item = line.split(";")
            bg_dict[item[0]] = [float(item[1].replace(",", ".")), int(item[2])]
    return find_relative_weight(bg_dict)


def find_relative_weight(bg_dict):
    bg_list = sorted(bg_dict.items(), key=lambda x: x[1][0])
    i = 0
    for element in bg_list:
        bg_dict[element[0]][0] = i
        i += 1
    return bg_dict


def sort_collection_by_weight(collection, bg_dict):
    return sorted(collection, key=lambda x: bg_dict[x][0], reverse=True)


def create_first_cube(collection, bg_dict):
    cube = []
    for game in collection:
        game_length = bg_dict[game][1]
        cube_length = 0 if len(cube) == 0 else sum([bg_dict[game][1] for game in cube])
        if cube_length + game_length < WIDTH:
            cube.append(game)
        else:
            return cube
    return cube


def sort_first_cube(cube, collection, bg_dict):
    missing_length = WIDTH - sum([bg_dict[game][1] for game in cube])
    if missing_length <= TOLERANCE:
        return cube

    for nb_rm_game in range(0, len(cube)):
        current_cube_comb = itertools.combinations(cube, len(cube) - nb_rm_game)
        for current_cube in current_cube_comb:
            missing_length = WIDTH - sum([bg_dict[game][1] for game in current_cube])
            for nb_game_to_switch in range(1, 5):
                flag = True
                for comb in itertools.combinations(collection[:9], nb_game_to_switch):
                    length = np.sum([bg_dict[game][1] for game in comb])
                    if length < missing_length and flag:
                        flag = False
                    if 0 < missing_length - length <= TOLERANCE:
                        current_cube = np.array(current_cube)
                        return np.append(current_cube, comb)
                if flag:
                    break
    print("No combination found")
    return None


def sort_cubes(bg_dict):
    sorted_cubes = []
    collection = bg_dict.keys()

    while len(collection) != 0:
        collection = sort_collection_by_weight(collection, bg_dict)
        cube = create_first_cube(collection, bg_dict)
        if len(collection) != len(cube):
            sorted_cube = sort_first_cube(cube, collection[len(cube):], bg_dict)
        else:
            sorted_cube = cube
        if sorted_cube is None:
            break
        sorted_cubes.append(sorted_cube)
        for game in sorted_cube:
            collection.remove(game)
    return sorted_cubes


def find_missing_games(sorted_cubes, bg_dict):
    games = np.array([])
    for cube in sorted_cubes:
        for game in cube:
            games = np.append(games, game)

    missing_games = np.array([])
    for game in bg_dict.keys():
        if game not in games:
            missing_games = np.append(missing_games, game)
    return missing_games


def main():
    bg_dict = csv2dict("collection.csv")
    sorted_cubes = sort_cubes(bg_dict)

    print("Total number of games: ", sum([len(cube) for cube in sorted_cubes]))
    print("Sorted cubes")
    for s in sorted_cubes:
        print(list(s))


    print()
    print("Missing Games")
    missing_games = find_missing_games(sorted_cubes, bg_dict)
    print(missing_games)

main()