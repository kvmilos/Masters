from utils.io import read_conll

all_sentences = read_conll("data/MPDT/MPDT_1.conll")

for i, sent in enumerate(all_sentences, start=1):
    print(f"Sentence {i}, root = {sent.get_root().form if sent.get_root() else '(no root)'}")
    print([child.form for child in sent.get_root().children])
