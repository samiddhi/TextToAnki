import json
import nltk
import os

from typing import List, Dict, Set
from collections import Counter

FILTER_KNOWN = True

class Language:
    def __init__(self, lang: str):
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        data_path = os.path.join(base_path, 'data', 'language_packs', lang)

        std_path: str = os.path.join(data_path, 'lex', 'forward_map.json')
        self.standard: str = std_path if os.path.exists(std_path) else None

        rev_path: str = os.path.join(data_path, 'lex', 'backward_map.json')
        if os.path.exists(rev_path):
            self.reverse: str = rev_path
        elif self.standard is not None:
            raise NotImplementedError("Reverse json generator from "
                                      "SloDictGen Project not yet implemented")
        else:
            self.reverse = None

        exclusion_path: str = os.path.join(data_path, 'lex', 'exclusion_list.csv')
        self.exclusion_list: str = exclusion_path if os.path.exists(exclusion_path) else None

class Lexicon:
    """Class of lemmas and their wordform lists."""

    def __init__(
            self,
            lang: str,
            settings: Dict
    ) -> None:
        language = Language(lang)



        """Initialize the lexicon with data loaded from a JSON file."""
        if language.standard is not None:
            with open(language.reverse, "r", encoding="utf-8") as reverse:
                form_lemmas: Dict[str, List[str]] = json.load(reverse)
                self.data: Dict[str, List[str]] = form_lemmas
        else:
            self.data = {}



        if settings.get("exclusion_list_filtering") and (language.exclusion_list is not None):
            with open(language.exclusion_list, "r", encoding="utf-8") as known_file:
                self.all_known: List[str] = [line.split(',')[0].strip() for
                                             line in
                                             known_file]
        else:
            self.all_known: List[str] = []


    def find_lemmas(self, word: str) -> Set[str]:
        lemmas = self.data.get(word, [])
        unknown_lemmas = set(lemmas) - set(self.all_known)

        return unknown_lemmas if unknown_lemmas else set() if lemmas else {
            f'*{word}'}


class TextAnalyzer:
    """Class for analyzing text."""

    def __init__(self, input_text: str, lex: Lexicon) -> None:
        self.text: str = input_text
        self.tokens: List[str] = self.tokenize()
        self.token_frequencies = Counter(self.tokens)
        self.lemmas = self.get_lemmas(lex)
        self.lemma_frequencies = Counter(self.lemmas)

    def tokenize(self) -> List[str]:
        sentences = nltk.sent_tokenize(self.text)
        decapitalized_tokens = []
        for sentence in sentences:
            tokens = nltk.RegexpTokenizer(r'\w+').tokenize(sentence)
            if tokens:
                tokens[0] = tokens[0].lower()
            decapitalized_tokens.extend(tokens)
        return decapitalized_tokens

    def get_lemmas(self, lex) -> list:
        lemmas = []
        for token in self.tokens:
            if any(char.isdigit() for char in token):
                continue
            found_lemmas = lex.find_lemmas(token.lower())
            lemmas.extend(found_lemmas)
        return lemmas
