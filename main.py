import itertools
import numpy as np

WIDTH = 336  # mm
WIDTH_TOLERANCE = 2  # mm
MAX_PARAM_TOLERANCE = 15
PATH_TO_COLLECTION = "mod_collection.csv"


def csv2dict(path):
    bg_dict = {}
    with open(path, "r") as f:
        skip_first = True
        for line in f.readlines():
            if skip_first:
                skip_first = False
                continue
            item = line.split(";")
            bg_dict[item[0]] = [float(item[1]), int(item[2])]
    return find_relative_param(bg_dict)


def find_relative_param(bg_dict):
    bg_list = sorted(bg_dict.items(), key=lambda x: x[1][0])
    i = 0
    for element in bg_list:
        bg_dict[element[0]][0] = i
        i += 1
    return bg_dict


def sort_collection_by_param(collection, bg_dict):
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


def sort_first_cube(cube, collection, bg_dict, param_tolerance):
    missing_length = WIDTH - sum([bg_dict[game][1] for game in cube])
    if missing_length <= WIDTH_TOLERANCE:
        return cube

    for nb_rm_game in range(0, len(cube)):
        current_cube_comb = itertools.combinations(cube, len(cube) - nb_rm_game)
        for current_cube in current_cube_comb:
            missing_length = WIDTH - sum([bg_dict[game][1] for game in current_cube])
            for nb_game_to_switch in range(1, 20):
                flag = True
                for comb in itertools.combinations(collection[:param_tolerance], nb_game_to_switch):
                    length = np.sum([bg_dict[game][1] for game in comb])
                    if length < missing_length and flag:
                        flag = False
                    if 0 < missing_length - length <= WIDTH_TOLERANCE:
                        current_cube = np.array(current_cube)
                        return np.append(current_cube, comb)
                if flag:
                    break
    return None


def sort_cubes(bg_dict, param_tolerance):
    sorted_cubes = []
    collection = bg_dict.keys()

    while len(collection) != 0:
        collection = sort_collection_by_param(collection, bg_dict)
        cube = create_first_cube(collection, bg_dict)
        if len(collection) != len(cube):
            sorted_cube = sort_first_cube(cube, collection[len(cube):], bg_dict, param_tolerance)
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


def sort_cubes_auto_param(bg_dict):
    best_param_tolerance = {"value": 0, "sorted_cubes": [], "missing_games": []}
    for i in range(MAX_PARAM_TOLERANCE):
        sorted_cubes = sort_cubes(bg_dict, i)
        missing_games = find_missing_games(sorted_cubes, bg_dict)
        if len(best_param_tolerance["missing_games"]) > len(missing_games) or len(best_param_tolerance["missing_games"]) == 0:
            best_param_tolerance["value"] = i
            best_param_tolerance["sorted_cubes"] = sorted_cubes
            best_param_tolerance["missing_games"] = missing_games
            if len(missing_games) == 0:
                break
    return best_param_tolerance["value"], best_param_tolerance["sorted_cubes"], best_param_tolerance["missing_games"]


def write_result(param_tolerance, sorted_cubes, missing_games):
    with open("result.txt", "w") as f:
        f.write("Total number of games: " + str(len(sorted_cubes) + len(missing_games)))
        f.write("\nSorted cubes with a param tolerance of: " + str(param_tolerance))
        for s in sorted_cubes:
            f.write("\n" + str(list(s)))
        f.write("\n\nMissing Games\n")
        f.write(str(missing_games))


def main():
    bg_dict = csv2dict(PATH_TO_COLLECTION)
    param_tolerance, sorted_cubes, missing_games = sort_cubes_auto_param(bg_dict)
    write_result(param_tolerance, sorted_cubes, missing_games)


main()
