from config.states import morph

# Получение верного склонения слова
def match_word(word, number):
    parse_word = morph.parse(word)[0]
    correct_word = parse_word.make_agree_with_number(number).word
    return correct_word
