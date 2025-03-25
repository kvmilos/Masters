"""
A script to collect unique MPDT tags from all CoNLL files in a specified folder.
"""
import os
import glob

def collect_mpdt_tags(folder_path):
    tag_counts = {}
    # Znajdź wszystkie pliki .conll w podanym folderze (bez rekurencji)
    files = glob.glob(os.path.join(folder_path, "*.conll"))
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Pomijamy linie puste oraz komentarze (zaczynające się od "#")
                if not line or line.startswith("#"):
                    continue
                parts = line.split('\t')
                # Sprawdzamy, czy linia ma co najmniej 5 kolumn (indeks 0-4)
                if len(parts) < 5:
                    continue
                # Przyjmujemy, że oryginalny tag MPDT znajduje się w kolumnie 5 (indeks 4)
                tag = parts[4].strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return tag_counts

def main():
    folder = input("Podaj ścieżkę do folderu z plikami CoNLL: ").strip()
    if not os.path.isdir(folder):
        print("Podana ścieżka nie jest folderem lub nie istnieje.")
        return

    print("Przetwarzanie plików z folderu:", folder)
    tag_counts = collect_mpdt_tags(folder)
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[0])
    print(f"\nZnaleziono {len(sorted_tags)} unikalnych tagów MPDT:")
    for tag, count in sorted_tags:
        print(f"{tag} : {count}")

    output_file = "mpdt_tags_corrected.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for tag, count in sorted_tags:
            f.write(f"{tag}\t{count}\n")
    print(f"\nUnikalne tagi MPDT wraz z ilością wystąpień zapisane zostały do pliku: {output_file}")

if __name__ == "__main__":
    main()
