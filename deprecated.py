import numpy as np
import itertools
import pandas as pd


WIDTH = 336  # mm
TOLERANCE = 2  # mm
MAX_CUBES = 13


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
    return bg_dict


def dict2csv(path, data):
    with open(path, "w") as f:
        for element in data:
            for i in element:
                f.write(f"{i};")
            f.write(f"\n")


def read_collection(path):
    collection = []
    with open(path, "r") as f:
        for line in f.readlines():
            item = line.split(";")[:-1]
            collection.append(item)
    return collection


def find_relative_weight(bg_dict):
    bg_list = sorted(bg_dict.items(), key=lambda x: x[1][0])
    i = 0
    for element in bg_list:
        bg_dict[element[0]][0] = i
        i += 1
    return bg_dict


def find_available_collections(target_min, target_max, weight_tolerance, bg_dict):
    valid_collections = []
    for i in range(3, 7):
        print(i)
        for seq in itertools.combinations(bg_dict, i):
            if target_min <= np.sum([bg_dict[i][1] for i in seq]) <= target_max:
                if filter_collections_by_weight(weight_tolerance, seq, bg_dict):
                    valid_collections.append(seq)
                    print(seq)
    return valid_collections


def filter_collections_by_weight(target, collection, bg_dict):
    weigth = np.array([bg_dict[i][0] for i in collection])
    return np.max(weigth) - np.min(weigth) <= target


def valid_final_collections(collections, bg_dict):
    all_possible_collections = itertools.combinations(collections, MAX_CUBES)
    valid_final_collections_list = np.array([])
    for possible_collection in all_possible_collections:
        not_here_games = 0
        for game in bg_dict.keys():
            if possible_collection.count(game) > 1:
                break
            elif possible_collection.count(game) == 0:
                not_here_games += 1
                if not_here_games >= 7:
                    break
            else:
                valid_final_collections_list = np.append(valid_final_collections_list, possible_collection)
                print(possible_collection)
    return valid_final_collections_list


def create_valid_collection_rec(possible_cube, current_collection, all_valid_collections):
    possible_cube_copy = possible_cube.copy()
    current_collection_copy = current_collection.copy()
    while len(possible_cube_copy) != 0:
        flag_break = False
        cube = possible_cube_copy[0]
        for game in cube:
            if game in current_collection:
                possible_cube_copy.remove(cube)
                flag_break = True
                break
        if flag_break:
            continue
        current_collection_copy.extend(cube)
        possible_cube_copy.remove(cube)
        create_valid_collection_rec(possible_cube_copy, current_collection_copy, all_valid_collections)
        length = len(current_collection_copy)
        if length > all_valid_collections[0]:
            all_valid_collections[0] = length
            all_valid_collections[1] = [current_collection_copy]
            print(all_valid_collections)
        elif length == all_valid_collections[0]:
            all_valid_collections[1].append(current_collection_copy)
        current_collection_copy = current_collection_copy[:-len(cube)]
    return all_valid_collections


def create_collection_dict(weight_tolerance):
    bg_dict_weight_length = csv2dict("collection.csv")
    bg_dict_weight_length = find_relative_weight(bg_dict_weight_length)
    collections = find_available_collections(WIDTH - TOLERANCE, WIDTH, weight_tolerance, bg_dict_weight_length)
    dict2csv(f"available_collections-weight_{weight_tolerance}.csv", collections)


def create_valid_collection(weight_tolerance):
    collection = read_collection(f"available_collections-weight_{weight_tolerance}.csv")
    all_valid_collections = create_valid_collection_rec(collection, [], [0, []])
    print(all_valid_collections)
    # final_collection = valid_final_collections(collection, csv2dict("collection.csv"))
    dict2csv(f"valid_final_collections_{weight_tolerance}.csv", all_valid_collections[1])


def evaluate_collection(weight_tolerance):
    bg_dict_weight_length = csv2dict("collection.csv")
    bg_dict_weight_length = find_relative_weight(bg_dict_weight_length)
    collections = read_collection(f"valid_final_collections_{weight_tolerance}.csv")

    minimum_max_diff = 100
    std_max_diff = 100
    minimum_max_diff_collection = []
    for i in range(len(collections)):
        weights = [bg_dict_weight_length[game][0] for game in collections[i]]
        diff = [weights[j] - weights[j - 1] for j in range(1, len(weights))]
        max_diff = np.max(diff)
        std_diff = np.abs(np.std(diff))
        if minimum_max_diff > max_diff:
            minimum_max_diff = max_diff
            minimum_max_diff_collection = [collections[i]]
        elif minimum_max_diff == max_diff:
            if std_diff < std_max_diff:
                std_max_diff = std_diff
                minimum_max_diff_collection = [collections[i]]
            elif std_diff == std_max_diff:
                minimum_max_diff_collection.append(collections[i])
    minimum_max_diff_collection = np.array(minimum_max_diff_collection)
    dict2csv(f"evaluated_collection_{weight_tolerance}.csv", minimum_max_diff_collection)


def divise_collection():
    collections = read_collection(f"evaluated_collection_10.csv")
    bg_dict_weight_length = csv2dict("collection.csv")
    collections_cubed = []
    for collection in collections:
        cube_collection = []
        cube = []
        length_cube = 0
        for game in collection:
            length_game = bg_dict_weight_length[game][1]
            if length_cube + length_game > WIDTH:
                cube_collection.append(cube)
                cube = []
                length_cube = 0
            cube.append(game)
            length_cube += length_game

        collections_cubed.append(cube_collection)
    dict2csv(f"evaluated_collection_cubed_10.csv", collections_cubed)


# create_collection_dict(10)
# create_valid_collection(10)
# evaluate_collection(10)
divise_collection()