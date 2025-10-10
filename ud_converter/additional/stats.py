"""
Corpus statistics for MPDT/UD-style CoNLL files.

Computes and prints:
- Average number of tokens per sentence
- POS frequency (column 4), sorted desc
- Dependency frequency by base label (prefix before ':' or '_' in column 8/DEPREL), sorted desc
- Number of sentences with >1 root, with no root, with cycles
- Number of non-projective edges and number of sentences that contain any

Data source (default): ud_converter/data/MPDT/MPDT_2000.conll
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
import os


@dataclass
class Token:
	idx: int
	form: str
	lemma: str
	xpos_simple: str  # column 4
	tag: str          # column 5, e.g., subst:sg:nom:m
	feats: str
	head: int
	deprel: str


Sentence = List[Token]


def parse_conll(path: str) -> List[Sentence]:
	"""Parse a (MPDT) CoNLL(-U-like) file into a list of sentences.

	Expected columns (tab-separated), based on provided sample:
	1: ID (int)
	2: FORM
	3: LEMMA
	4: XPOS (simple)
	5: TAG (fine-grained, colon-separated)
	6: FEATS (pipe-separated)
	7: HEAD (int)
	8: DEPREL
	9: DEPS (ignored)
	10: MISC (ignored)
	"""
	sentences: List[Sentence] = []
	current: Sentence = []
	with open(path, encoding="utf-8") as f:
		for raw in f:
			line = raw.rstrip("\n")
			if not line or line.startswith("#"):
				# sentence boundary on blank line
				if not line and current:
					sentences.append(current)
					current = []
				continue
			parts = line.split("\t")
			if len(parts) < 8:
				# Skip malformed lines
				continue
			try:
				idx = int(parts[0])
			except ValueError:
				# Skip multiword token ranges like 3-4 if any
				continue
			form = parts[1] if len(parts) > 1 else "_"
			lemma = parts[2] if len(parts) > 2 else "_"
			xpos_simple = parts[3] if len(parts) > 3 else "_"
			tag = parts[4] if len(parts) > 4 else "_"
			feats = parts[5] if len(parts) > 5 else "_"
			try:
				head = int(parts[6])
			except Exception:
				head = 0
			deprel = parts[7] if len(parts) > 7 else "_"
			current.append(Token(idx, form, lemma, xpos_simple, tag, feats, head, deprel))
	# Append last sentence if file doesn't end with a newline
	if current:
		sentences.append(current)
	return sentences


def deprel_base(label: str) -> str:
	"""Base of dependency label: split at first ':' or '_' (if present)."""
	if not label or label == "_":
		return "_"
	colon = label.find(":")
	underscore = label.find("_")
	cuts = [p for p in (colon, underscore) if p != -1]
	if cuts:
		return label[: min(cuts)]
	return label


def detect_cycles(sent: Sentence) -> bool:
	"""Detect cycles in head pointers (ignoring HEAD=0)."""
	parent: Dict[int, int] = {tok.idx: tok.head for tok in sent}
	visiting: Set[int] = set()
	visited: Set[int] = set()

	def dfs(u: int) -> bool:
		if u in visited:
			return False
		if u in visiting:
			return True
		visiting.add(u)
		v = parent.get(u, 0)
		if v > 0:
			if dfs(v):
				return True
		visiting.remove(u)
		visited.add(u)
		return False

	for tok in sent:
		if tok.idx not in visited:
			if dfs(tok.idx):
				return True
	return False


def nonprojective_edges(sent: Sentence) -> Set[Tuple[int, int]]:
	"""Return set of non-projective edges as (head, dep) pairs."""
	arcs: List[Tuple[int, int]] = [(tok.head, tok.idx) for tok in sent if tok.head != 0]
	nonproj: Set[Tuple[int, int]] = set()
	for i in range(len(arcs)):
		h1, d1 = arcs[i]
		a, b = (h1, d1) if h1 < d1 else (d1, h1)
		for j in range(i + 1, len(arcs)):
			h2, d2 = arcs[j]
			c, d = (h2, d2) if h2 < d2 else (d2, h2)
			if (a < c < b < d) or (c < a < d < b):
				nonproj.add((h1, d1))
				nonproj.add((h2, d2))
	return nonproj


def compute_stats(path: str) -> None:
	sentences = parse_conll(path)
	if not sentences:
		print(f"No sentences found in: {path}")
		return

	total_tokens = 0
	roots_gt1 = 0
	roots_eq0 = 0
	cycles_cnt = 0
	sentences_with_nonproj = 0
	total_nonproj_edges = 0

	# POS and dependency base counts
	pos_counts: Dict[str, int] = {}
	dep_base_counts: Dict[str, int] = {}

	for sent in sentences:
		total_tokens += len(sent)

		# Roots per sentence
		roots = sum(1 for tok in sent if tok.head == 0)
		if roots > 1:
			roots_gt1 += 1
		if roots == 0:
			roots_eq0 += 1

		# Cycles
		if detect_cycles(sent):
			cycles_cnt += 1

		# Non-projectivity
		np_edges = nonprojective_edges(sent)
		if np_edges:
			sentences_with_nonproj += 1
			total_nonproj_edges += len(np_edges)

		# Per-token counts
		for tok in sent:
			pos_counts[tok.xpos_simple] = pos_counts.get(tok.xpos_simple, 0) + 1
			dep_base = deprel_base(tok.deprel)
			dep_base_counts[dep_base] = dep_base_counts.get(dep_base, 0) + 1

	avg_tokens = total_tokens / len(sentences)

	# Sort
	pos_rows = sorted(pos_counts.items(), key=lambda x: (-x[1], x[0]))
	dep_rows = sorted(dep_base_counts.items(), key=lambda x: (-x[1], x[0]))

	# Print
	print("=== Corpus summary ===")
	print(f"File: {path}")
	print(f"Sentences: {len(sentences)}")
	print(f"Tokens:    {total_tokens}")
	print(f"Avg tokens/sentence: {avg_tokens:.2f}")
	print()

	print("=== POS frequency (column 4) ===")
	print(f"{'POS':<15} {'COUNT':>9}")
	for pos, n in pos_rows:
		print(f"{pos:<15} {n:>9}")
	print()

	print("=== Dependency frequency by base (desc) ===")
	print(f"{'BASE':<20} {'COUNT':>9}")
	for base, n in dep_rows:
		print(f"{base:<20} {n:>9}")
	print()

	print("=== Structural diagnostics ===")
	print(f"Sentences with >1 root: {roots_gt1}")
	print(f"Sentences with 0 root : {roots_eq0}")
	print(f"Sentences with cycles : {cycles_cnt}")
	print(f"Non-projective edges  : {total_nonproj_edges}")
	print(f"Sentences with NP edges: {sentences_with_nonproj}")

	# Charts (no plot titles; titles will be added in the document text)
	def _save_bar_chart(items: List[Tuple[str, int]], xlabel: str, out_png: str, top_n: int = 20) -> None:
		try:
			import matplotlib
			matplotlib.use("Agg")  # non-interactive backend
			import matplotlib.pyplot as plt
		except Exception as e:
			print(f"[charts] Skipping {os.path.basename(out_png)} (matplotlib not available): {e}")
			return

		labels = [k for k, _ in items[:top_n]]
		counts = [v for _, v in items[:top_n]]
		plt.figure(figsize=(10, max(4, 0.35 * len(labels))))
		plt.barh(range(len(labels)), counts, color="#4C78A8")
		plt.yticks(range(len(labels)), labels)
		plt.gca().invert_yaxis()
		plt.xlabel(xlabel)
		plt.tight_layout()
		plt.savefig(out_png, dpi=150)
		plt.close()
		print(f"[charts] Saved: {out_png}")

	plots_dir = os.path.join(os.path.dirname(__file__), "plots")
	os.makedirs(plots_dir, exist_ok=True)
	_save_bar_chart(pos_rows, "Count", os.path.join(plots_dir, "pos_frequency.png"), top_n=20)
	_save_bar_chart(dep_rows, "Count", os.path.join(plots_dir, "dep_frequency.png"), top_n=20)


if __name__ == "__main__":
	default_path = os.path.join(
		os.path.dirname(os.path.dirname(__file__)),
		"data",
		"MPDT",
		"MPDT_2000.conll",
	)
	compute_stats(default_path)