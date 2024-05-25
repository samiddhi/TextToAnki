import json
import nltk

from typing import List, Dict, Set
from collections import Counter

FILTER_KNOWN = True
RETURN_KNOWN_VARIANTS = False

class Language:
    def __init__(self, lang: str):
        if lang.lower() == "pali":
            self.standard: str = (
                r"C:\Users\sangha\Documents\Danny's\TextToAnki"
                r"\data\pali_lex\pali_forward_mapping.json"
            )
            self.reverse: str = (
                r"C:\Users\sangha\Documents\Danny's\TextToAnki"
                r"\data\pali_lex\pali_backward_mapping.json"
            )
            self.known = None
        elif lang.lower() == "slovene":
            self.standard: str = (
                r"C:\Users\sangha\Documents\Danny's\TextToAnki"
                r"\data\slovene_lex\lexicon_lower.json"
            )
            self.reverse: str = (
                r"C:\Users\sangha\Documents\Danny's\TextToAnki"
                r"\data\slovene_lex\reverse_lower.json"
            )
            self.known: str = (
                r"C:\Users\sangha\Documents\Danny's\TextToAnki\data"
                r"\slovene_lex\known.csv"
            )
        else:
            print(f"Language \"{lang}\" not implemented")
            raise NotImplementedError


class Lexicon:
    """Class of sloleks lemmas and their wordform lists."""

    def __init__(
            self,
            lang: str
    ) -> None:
        language = Language(lang)


        """Initialize the lexicon with data loaded from a JSON file."""
        with open(language.reverse, "r", encoding="utf-8") as reverse:
            form_lemmas: Dict[str, List[str]] = json.load(reverse)
            self.data: Dict[str, List[str]] = form_lemmas

        if FILTER_KNOWN and (language.known is not None):
            with open(language.known, "r", encoding="utf-8") as known_file:
                self.all_known: List[str] = [line.split(',')[0].strip() for
                                             line in
                                             known_file]
        else:
            self.all_known: List[str] = []

        # Return all variants of terms in known.json
        if RETURN_KNOWN_VARIANTS:
            with open(language.standard, "r", encoding="utf-8") as std:
                lemma_forms: Dict[str, List[str]] = json.load(std)
            for i in self.all_known:
                print(i)
                for j in lemma_forms.get(i, []):
                    print(j)

    def find(self, word: str) -> Set[str]:
        return set([item for item in self.data.get(word, []) if item not in
                    self.all_known])


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
            found_lemmas = lex.find(token.lower())
            lemmas.extend(found_lemmas)
        return lemmas
