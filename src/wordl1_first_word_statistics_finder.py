import csv, random

def read_words(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        words = [item[0] for item in data]
    return words

def filter_by_letter_state(word_list, input_string, letter_present):
    #letter_present = True: Accept only words containing the letter
    #letter_present = False: Accept only words not containing the letter
    new_word_list = []
    for word in word_list:
        letter_state = False
        for letter in input_string:
            if (letter in word) ^ letter_present:
                letter_state = True
                break
        if not letter_state:
            new_word_list.append(word)
    return new_word_list
def filter_by_placements(word_list, placements_list, placements_are_perfect):
    #placements_are_perfect == True: require letters to be placed in correct place
    #placements_are_perfect == False: require letters to be placed in wrong place
    new_word_list = []
    for word in word_list:
        all_placements_pass = True
        for placement in placements_list:
            x = 2
            if (word[placement[1] - 1] == placement[0]) ^  placements_are_perfect: # ^ symbol means xor
                all_placements_pass = False
        if all_placements_pass:
            new_word_list.append(word)
    return new_word_list
def filter_by_imperfect_placements2(word_list, imperfect_placements):
    present_string = ''.join(list(set([item[0] for item in imperfect_placements])))
    return filter_by_letter_state(word_list, present_string, letter_present = True)
def wordl_filters(word_list, not_present_string, perfect_placements, imperfect_placements):
    word_list2 = filter_by_letter_state(word_list, not_present_string, letter_present = False)
    word_list3 = filter_by_placements(word_list2, perfect_placements, placements_are_perfect = True)
    word_list4 = filter_by_placements(word_list3, imperfect_placements, placements_are_perfect = False)
    word_list5 = filter_by_imperfect_placements2(word_list4, imperfect_placements)
    return word_list5

def get_not_present_string(full_board, secret_word):
    all_strings_concat = ''.join(full_board)
    all_chars_missing_from_secret_word = set(all_strings_concat) - set(secret_word)
    all_chars_found_in_secret_word = set(all_strings_concat).intersection(set(secret_word))
    return ''.join(all_chars_missing_from_secret_word), ''.join(all_chars_found_in_secret_word)
def get_perfect_placements(full_board, secret_word):
    perfect_placements = []
    for row in full_board:
        for ix in range(len(row)):
            if secret_word[ix] == row[ix]:
                perfect_placements.append((row[ix], ix+1))
    return list(set(perfect_placements))
def get_imperfect_placements(full_board, present_string, perfect_placements):
    imperfect_placement_list = []
    perfect_placement_letters = ''.join([item[0] for item in perfect_placements])
    for word in full_board:
        for ix in range(len(word)):
            if (word[ix] in present_string) and (word[ix] not in perfect_placement_letters):
                imperfect_placement_list.append((word[ix], ix + 1))
    imperfect_placement_list = list(set(imperfect_placement_list))
    return imperfect_placement_list
def get_wordl_placement_information(wordl_board, hidden_word):
    not_present_string = ''
    perfect_placements = []
    imperfect_placements = []
    not_present_string, present_string = get_not_present_string(wordl_board, hidden_word)
    perfect_placements = get_perfect_placements(wordl_board, hidden_word)
    imperfect_placements = get_imperfect_placements(wordl_board, present_string, perfect_placements)
    return not_present_string, perfect_placements, imperfect_placements

def get_FOM(word_list, filtered_word_list):
    length_original_word_list = len(word_list)
    length_filtered_word_list = len(filtered_word_list)
    fraction_words_removed = (length_original_word_list - length_filtered_word_list) / length_original_word_list
    return fraction_words_removed

def update_statistics(stats_dictionary, first_guess, current_FOM):
    previous_quantity_found = stats_dictionary[first_guess][1]
    previous_average_FOM = stats_dictionary[first_guess][0]
    updated_quantity_found = previous_quantity_found + 1
    updated_average_FOM = ((previous_quantity_found * previous_average_FOM) + current_FOM) / updated_quantity_found
    stats_dictionary[first_guess] = [updated_average_FOM, updated_quantity_found]

five_letter_words = 'five_letter_words.csv'
word_list = read_words(five_letter_words)

# not_present_string = 'wetosdkcm'
# perfect_placements = [('i', 4)]
# imperfect_placements = [('a', 3), ('a', 4), ('n', 5), ('a', 2), ('n', 3)]

stats_dictionary = {item : [0, 0] for item in word_list}

ix = 0
while True:
    wordl_inputs = random.sample(word_list, 1)
    hidden_word = random.sample(word_list, 1)[0]
    not_present_string, perfect_placements, imperfect_placements =  get_wordl_placement_information(wordl_inputs, hidden_word)
    filtered_word_list = wordl_filters(word_list, not_present_string, perfect_placements, imperfect_placements)
    FOM = get_FOM(word_list, filtered_word_list)
    first_guess = wordl_inputs[0]
    update_statistics(stats_dictionary, first_guess, FOM)
    if ix % 10000 == 0:
        list_of_list_of_statistics = [[key,stats_dictionary[key][0], stats_dictionary[key][1]] for key in stats_dictionary]
        with open('output_statistics.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(list_of_list_of_statistics)
            list_of_FOMs = [item[1] for item in list_of_list_of_statistics]
            max_index = list_of_FOMs.index(max(list_of_FOMs ))
            best_word_to_guess = list_of_list_of_statistics[max_index][0]
            print(ix, best_word_to_guess)

    ix = ix + 1

x = 2