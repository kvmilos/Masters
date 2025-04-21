# Middle Polish Dependency Treebank Converter

A tool for converting the Middle Polish Dependency Treebank (MPDT) from CoNLL format to Universal Dependencies (UD) CONLL-U format.

## Overview

This project provides utilities for converting dependency trees from traditional linguistic annotations to the Universal Dependencies framework. The converter handles:

- POS tag conversion (MPDT → UD)
- Morphological feature conversion
- Dependency relation conversion

## Project Structure

```
ud_converter/
├── converter.py
├── corrector.py
├── morphosyntax/
│   ├── pos_categories/
│   ├── preconversion.py
│   ├── conversion.py
│   ├── postconversion.py
│   └── morphosyntax.py
├──dependency/
│   ├── structures/
│   ├── labels.py
│   ├── preconversion.py
│   └── conversion.py
├── utils/
│   ├── classes.py
│   ├── constants.py
│   ├── io.py
│   └── logger.py
├── additional/
└── MPDT.md
```

## Usage

To convert a CoNLL file to UD CONLL-U format:

```
python converter.py input_file.conll output_file.conllu [meta_file.json] [--tags-only]
```

Arguments:
- `input_file.conll`: Path to input file in CoNLL format
- `output_file.conllu`: Path to output file in UD CONLL-U format
- `meta_file.json` (optional): Path to JSON file with metadata
- `--tags-only` (optional): Only convert POS tags, not dependency relations

## Usage of corrector.py

To correct a CoNLL MPDT file:

```
python corrector.py input_path output_dir [--test]
```

Arguments:
- `input_path`: Path to a directory containing CoNLL files, or to one specific ConLL file
- `output_dir`: Path to a directory for the output file(s) to be saved there
- `--test` (optional): Test the corrected file for valid POS tags, features, and feature-POS combinations

## Development Status

Currently, the conversion of POS tags and morphological features is implemented.
Dependency relation conversion: Base implemented, needs corrections and further work

## References

- [Universal Dependencies](https://universaldependencies.org/)
- Middle Polish Dependency Treebank