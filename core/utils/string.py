
def words_separator(list_words, separator=", ", end_separator=" and "):
    """Words Separator

    Args:
        list_words (list): list of words
        separator (str): word separator
        end_separator (str): word end separator

    Returns:
        str: list of words separated. e.g. "1, 2, 3 and 4"

    """

    text = ""

    for index, word in enumerate(list_words):
        if index == 0:
            # if the current iteration is the first
            text += word
        elif index < len(list_words) - 1:
            # if the current iteration isn't the first and the last
            text += separator + word
        else:
            # if the current iteration is the last
            text += end_separator + word

    return text
