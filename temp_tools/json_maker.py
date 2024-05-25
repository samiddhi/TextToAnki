from typing import Dict, List, Set
import xml.etree.ElementTree as Et
import json
import os


def lemma_forms_parser(directory: str) -> None:
    """
    Initialize the LemmaFormsParser with the directory containing XML files.

    :param directory: The directory path containing XML files.
    """

    data: Dict[str, List[str]] = {}

    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            filepath = os.path.join(directory, filename)
            tree = Et.parse(filepath)
            root = tree.getroot()
            for entry in root.findall(".//entry"):
                lemma = entry.find(".//lemma").text.strip()
                for orthlist in entry.findall(".//orthographyList"):
                    for form in orthlist.findall(".//form"):
                        wordform = form.text.strip()
                        if lemma in data:
                            data[lemma].append(wordform)
                        else:
                            data[lemma] = [wordform]

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def reverse_json_writer(read, write):
    with open(read, "r", encoding="utf-8") as r_file:
        data = json.load(r_file)

    search: Dict[str, Set[str]] = {}
    for lemma, forms in data.items():
        for form in forms:
            if form not in search:
                search[form] = {lemma}
            else:
                search[form].add(lemma)

    json_output: Dict[str, List[str]] = {}
    for form, lemmas in search.items():
        json_output[form] = list(lemmas)

    print("done!")
    with open(write, "w", encoding="utf-8") as w_file:
        json.dump(json_output, w_file, ensure_ascii=False, indent=4)

# Used to split because the upper case words are annoying
def split_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    upper_keys = {k: v for k, v in data.items() if k[0].isupper()}
    lower_keys = {k: v for k, v in data.items() if k[0].islower()}

    with open('uppercase_keys.json', 'w', encoding='utf-8') as f:
        json.dump(upper_keys, f, indent=4, ensure_ascii=False)

    with open('lowercase_keys.json', 'w', encoding='utf-8') as f:
        json.dump(lower_keys, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    x = r"C:\Users\sangha\Documents\Danny's\TextToAnki\data\lexicon.json"
    read = "pali_forward_mapping.json"
    write = "pali_backward_mapping.json"
    reverse_json_writer(read, write)
