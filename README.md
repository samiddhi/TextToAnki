# Setup

---

## Python libraries
    for tta:
        icecream
        nltk (after pip installed:)
            >> import nltk
            >> nltk.download('punkt')

    for pali extractor:
        pandas

    for whisper:
        openai
        ffmpeg (do the following in terminal)
            pip install ffmpeg-downloader
            ffdl install --add-path
        pydub

    for slovenscina.eu transcriber:
        torch
        ffmpeg + pydub (see above)
        nemo
            pip install git+https://github.com/NVIDIA/NeMo.git

---
## Files needed:
   - 

---
## Process:
   1. Make Slo lexicon .jsons using: 
      1. [lemma_forms_parser](temp_tools/json_maker.py)
      2. [reverse_json_writer](temp_tools/json_maker.py)
      3. [split_json()](temp_tools/json_maker.py)
      - Note: requires [Sloleks3.0](https://www.clarin.si/repository/xmlui/handle/11356/1745) download
   2. Make Pali lexicon .jsons using:
      1. Download dpd.db from most recent (DPD Release)[https://github.com/digitalpalidictionary/digitalpalidictionary/releases]
      2. Generate json with [dpd_extractor.py](C:\Users\sangha\Documents\Danny's\TextToAnki\temp_tools\dpd_extractor.py)
---

### Resources
  - The G.O.A.T. [Slovenščina.eu](https://www.slovenscina.eu/)
  - [GIT Large File Storage (LFS)](https://chat.openai.com/share/bbe21280-3637-4c5d-83f4-89976049507e)
  - [Add line breaks](https://textcleaner.net/add-line-breaks/)
  - [Transcript to text](https://www.browserling.com/tools/newlines-to-spaces)