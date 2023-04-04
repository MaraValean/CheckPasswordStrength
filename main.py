def count_missing_character_types(s, nr_characters):
    """
    This function determines how many character types(uppercase,lowercase,digit) are missing from the password
    :param s: the password (string)
    :param nr_characters: the number of characters in the password (int)
    :return: number of missing character types (int between 0 and 3)
    """
    nr_digits = 0
    nr_lowercase = 0
    nr_uppercase = 0

    for i in range(nr_characters):
        # for each letter in the password we check what type it is and store it in the associated variable
        letter = s[i]
        if letter.isdigit():
            nr_digits += 1
        elif letter.islower():
            nr_lowercase += 1
        elif letter.isupper():
            nr_uppercase += 1

    # now we compute how many missing character types we have
    nr_missing = 0
    if nr_uppercase == 0:
        nr_missing += 1
    if nr_lowercase == 0:
        nr_missing += 1
    if nr_digits == 0:
        nr_missing += 1

    return nr_missing


def construct_repeating_sequence_vector(s, nr_characters):
    """
    This function builds a vector whose elements are the lengths of each sequence of repeating characters
    :param s: the password (string)
    :param nr_characters: the number of characters in the password (int)
    :return: the vector we constructed (list)
    """
    i = 0
    j = 1
    repeating_sequence = []
    while i < nr_characters:
        while j < nr_characters and s[i] == s[j]:
            j += 1
        repeating_sequence.append(j - i)
        i = j
        j = j + 1
    return repeating_sequence


def check_password_strength(s):
    """
      This is the function used to check the strength of the password by analyzing 3 cases depending on the number of characters in the password
      :param s : the password(string)
      :return: the number of changes required to make the password strong : int (returns 0 if the password is already strong)
    """

    nr_changes = 0
    nr_characters = len(s)
    nr_changes_sequences = 0
    nr_changes_enough_characters = 0
    i = 0

    # I am assuming a password cannot be too long so there is no problem when it comes to time complexity

    # count the missing character types
    nr_missing = count_missing_character_types(s, nr_characters)

    # make a vector with the length of each sequence of repeating characters
    repeating_sequence = construct_repeating_sequence_vector(s, nr_characters)

    # First Case:we have enough characters so we only have to worry about the missing types and repeating characters
    # our change will be a replace in between the repeating sequences taking into account the missing types
    if 20 >= nr_characters >= 6:
        for sequence in repeating_sequence:
            nr_changes_sequences += sequence // 3
        nr_changes = max(nr_changes_sequences, nr_missing)

    # Second Case: we need to add characters
    # the change will be an add in between repeating sequences taking into account missing types
    elif nr_characters < 6:
        nr_changes_enough_characters = 6 - nr_characters
        for sequence in repeating_sequence:
            nr_changes_sequences += (sequence // 3)
        nr_changes = max(nr_changes_enough_characters, nr_missing,nr_changes_sequences)

    # Third Case: we need to remove some characters
    # the change will either be a remove or an edit in between repeating sequences taking into account missing types
    # first we need to remove from the repeating sequences until we do all the removes we need and then we will do replaces
    elif nr_characters > 20:
        nr_changes_enough_characters = nr_characters - 20
        nr_sequences = len(repeating_sequence)
        # first we remove characters from the sequences which are a multiple of 3 because those are the most useful removes
        for i in range(nr_sequences):
            if nr_changes_enough_characters >= 1 and repeating_sequence[i] % 3 == 0:
                repeating_sequence[i] -= 1
                nr_changes_enough_characters -= 1
        # we then remove the characters from the sequences from which 2 deletes solve a repeating sequence
        for i in range(nr_sequences):
            if nr_changes_enough_characters >= 2 and repeating_sequence[i] % 3 == 1 and repeating_sequence[i] > 3:
                repeating_sequence[i] -= 2
                nr_changes_enough_characters -= 2
        # then we remove from the rest of the sequences
        for i in range(nr_sequences):
            if nr_changes_enough_characters > 0 and repeating_sequence[i] > 2:
                nr_removed = min(nr_changes_enough_characters, repeating_sequence[i] - 2)
                repeating_sequence[i] -= nr_removed
                nr_changes_enough_characters -= nr_removed
        # here we do some replaces (if needed) to get rid of any repeating sequences left
        for sequence in repeating_sequence:
            nr_changes_sequences += sequence // 3
        nr_changes = max(nr_changes_sequences, nr_missing) + (nr_characters - 20)
    return nr_changes


def main(s):
    return check_password_strength(s)


print(main("aaaaaa"))
# print(check_password_strength("FFFFFFFFFFFFFFF11111111111111111111AAA"))
