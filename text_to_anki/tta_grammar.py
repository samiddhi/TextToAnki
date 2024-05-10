import json
import nltk

from typing import List, Dict, Set
from collections import Counter

FILTER_KNOWN = False
RETURN_KNOWN_VARIANTS = False


class Lexicon:
    """Class of sloleks lemmas and their wordform lists."""
    def __init__(
            self,
            reverse_path: str = (
                    r"C:\Users\sangha\Documents\Danny's\TextToAnki\data"
                    r"\reverse_lower.json"
            ),
            standard_path: str = (
                    r"C:\Users\sangha\Documents\Danny's\TextToAnki\data"
                    r"\lexicon_lower.json"
            ),
            known_path: str = (
                    r"C:\Users\sangha\Documents\Danny's\TextToAnki\data\known.csv"
            )
    ) -> None:
        """Initialize the lexicon with data loaded from a JSON file."""
        with open(reverse_path, "r", encoding="utf-8") as reverse:
            form_lemmas: Dict[str, List[str]] = json.load(reverse)
            self.data: Dict[str, List[str]] = form_lemmas

        if FILTER_KNOWN:
            with open(known_path, "r", encoding="utf-8") as known_file:
                self.all_known: List[str] = [line.split(',')[0].strip() for line in
                                             known_file]
        else:
            self.all_known: List[str] = []


        # Return all variants of terms in known.json
        if RETURN_KNOWN_VARIANTS:
            with open(standard_path, "r", encoding="utf-8") as std:
                lemma_forms: Dict[str, List[str]] = json.load(std)
            for i in self.all_known:
                print(i)
                for j in lemma_forms.get(i,[]):
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