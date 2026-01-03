# Trie Autocomplete

## Overview

- Random idea i had from a data structure that was not taught but was in a past year paper for a data structure course

### Dataset credit: By dwyl, released under the Unlicensed 
- [https://gist.github.com/h3xx/1976236#file-wiki-100k-txt](https://github.com/dwyl/english-words)
---

## Features

- The trie is made to accept any values, not just alphabets
- Create and save trie object using msgpack
- Update existing .msgpack to accept new words
- Autocomplete user input in command line

---

## Installation

 Required for saving object
 - msgpack chosen over JSON for storing nested dictionary easily and as binary format (Didn't test if file size is smaller that using JSON) :(

```bash
pip install msgpack

```

- Download entire folder and run the python files individually
- No point cloning cause i don't plan on continuing
- For installing in a virtual environment
- ```bash
  python -m venv venv
  pip install -r requirements.txt
  ```

---

## Running

- createNewTrieFromTxt.py replaces existing saved object
- addNewWordsToTrie.py specifies new text file with word list to add to
- runAutoCompleteInput.py shows a simple demonstration on autocomplete while typing (new: Can delete individual words by clicking enter)
