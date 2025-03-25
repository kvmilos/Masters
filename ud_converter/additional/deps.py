"""
A script to collect unique MPDT dependencies from all CoNLL files in a specified folder.
"""
import os
import glob

def collect_mpdt_tags(folder_path):
    dep_counts = {}
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
                # Sprawdzamy, czy linia ma co najmniej 8 kolumn (indeks 0-7)
                if len(parts) < 5:
                    continue
                # Przyjmujemy, że oryginalny depedency znajduje się w kolumnie 8 (indeks 7)
                dep = parts[7].strip()
                if dep:
                    dep_counts[dep] = dep_counts.get(dep, 0) + 1
    return dep_counts

def main():
    folder = input("Podaj ścieżkę do folderu z plikami CoNLL: ").strip()
    if not os.path.isdir(folder):
        print("Podana ścieżka nie jest folderem lub nie istnieje.")
        return

    print("Przetwarzanie plików z folderu:", folder)
    dep_counts = collect_mpdt_tags(folder)
    sorted_deps = sorted(dep_counts.items(), key=lambda x: x[0])
    print(f"\nZnaleziono {len(sorted_deps)} unikalnych depedencies:")
    for dep, count in sorted_deps:
        print(f"{dep} : {count}")

    output_file = "mpdt_deps_original.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for dep, count in sorted_deps:
            f.write(f"{dep}\t{count}\n")
    print(f"\nUnikalne depedencies wraz z ilością wystąpień zapisane zostały do pliku: {output_file}")

if __name__ == "__main__":
    main()
