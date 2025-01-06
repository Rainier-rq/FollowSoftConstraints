
import instructions
import taxonomy

_KEYWORD = "keywords:"

_LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_CONTENT = "detectable_content:"

_SCONTENT = "soft_content:"

_FORMAT = "detectable_format:"

_MULTITURN = "multi-turn:"

_COMBINATION = "combination:"

_STARTEND = "startend:"

_CHANGE_CASES = "change_case:"

_PUNCTUATION = "punctuation:"

_SITUATION ="situation:"

_STYLE="style:"


INSTRUCTION_CONFLICTS = {
    _KEYWORD + "existence": {_KEYWORD + "existence"},
    _KEYWORD + "frequency": {_KEYWORD + "frequency"},
    _KEYWORD + "forbidden_words": {_KEYWORD + "forbidden_words"},
    _KEYWORD + "letter_frequency": {_KEYWORD + "letter_frequency"},
    _LANGUAGE
    + "response_language": {
        _LANGUAGE + "response_language",
        _FORMAT + "multiple_sections",
        _KEYWORD + "existence",
        _KEYWORD + "frequency",
        _KEYWORD + "forbidden_words",
        _STARTEND + "end_checker",
        _CHANGE_CASES + "english_capital",
        _CHANGE_CASES + "english_lowercase",
    },
    _LENGTH + "number_sentences": {_LENGTH + "number_sentences"},
    _LENGTH + "number_paragraphs": {
        _LENGTH + "number_paragraphs",
        _LENGTH + "nth_paragraph_first_word",
        _LENGTH + "number_sentences",
        _LENGTH + "nth_paragraph_first_word",
    },
    _LENGTH + "number_words": {_LENGTH + "number_words"},
    _LENGTH + "nth_paragraph_first_word": {
        _LENGTH + "nth_paragraph_first_word",
        _LENGTH + "number_paragraphs",
    },
    _CONTENT + "number_placeholders": {_CONTENT + "number_placeholders"},
    _CONTENT + "postscript": {_CONTENT + "postscript"},
    _FORMAT + "number_bullet_lists": {_FORMAT + "number_bullet_lists"},
    _FORMAT + "constrained_response": set(taxonomy.taxonomy.keys()),
    _FORMAT
    + "number_highlighted_sections": {_FORMAT + "number_highlighted_sections"},
    _FORMAT
    + "multiple_sections": {
        _FORMAT + "multiple_sections",
        _LANGUAGE + "response_language",
        _FORMAT + "number_highlighted_sections",
        _LENGTH + "number_paragraphs",
    },
    _FORMAT
    + "json_format": set(taxonomy.taxonomy.keys()).difference({
        _KEYWORD + "forbidden_words", _KEYWORD + "existence",
        _KEYWORD + "existence",
        _KEYWORD + "frequency",
        }
    ),
    _FORMAT + 'xml_format': set(taxonomy.taxonomy.keys()).difference({
        _KEYWORD + "forbidden_words", _KEYWORD + "existence",
        _KEYWORD + "existence",
        _KEYWORD + "frequency",
        }
    ),
    _FORMAT + "title": {_FORMAT + "title"},
    _COMBINATION
    + "two_responses": set(taxonomy.taxonomy.keys()).difference({
        _KEYWORD + "forbidden_words",
        _KEYWORD + "existence",
        _LANGUAGE + "response_language",
        _FORMAT + "title",
        _PUNCTUATION + "no_comma",
        _STARTEND + "quotation"
    }),
    _COMBINATION + "repeat_prompt": set(taxonomy.taxonomy.keys()).difference({
        _KEYWORD + "existence",
        _FORMAT + "title",
        _PUNCTUATION + "no_comma",
    }),
    _STARTEND + "end_checker": {_STARTEND + "end_checker"},
    _CHANGE_CASES + "capital_word_frequency": {
        _CHANGE_CASES + "capital_word_frequency",
        _CHANGE_CASES + "english_lowercase",
        _CHANGE_CASES + "english_capital",
    },
    _CHANGE_CASES + "english_capital": {_CHANGE_CASES + "english_capital"},
    _CHANGE_CASES + "english_lowercase": {
        _CHANGE_CASES + "english_lowercase",
        _CHANGE_CASES + "english_capital",
    },
    _PUNCTUATION + "no_comma": {_PUNCTUATION + "no_comma"},
    _STARTEND + "quotation": {_STARTEND + "quotation", _FORMAT + "title"},
    _SCONTENT+"language":{_SCONTENT+"language"},
    _SCONTENT+"open_ended":{_SCONTENT+"open_ended"},
    _SITUATION+"suggestion":{_SITUATION+"suggestion"},
    _SITUATION+"role_play":{_SITUATION+"role_play"},
    _SITUATION+"story_generation":{_SITUATION+"story_generation"},
    _STYLE+"open_ended":{_STYLE+"open_ended"},
}


def conflict_make(conflicts):
  for key in conflicts:
    for k in conflicts[key]:
      conflicts[k].add(key)
    conflicts[key].add(key)
  return conflicts

