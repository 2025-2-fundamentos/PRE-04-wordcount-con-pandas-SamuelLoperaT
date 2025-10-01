"""Taller evaluable"""
import os
import re
import shutil
import time
import pandas as pd


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILES_DIR = os.path.join(BASE_DIR, "files")


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    input_dir = os.path.join(FILES_DIR, "input")
    raw_dir = os.path.join(FILES_DIR, "raw")

    os.makedirs(input_dir, exist_ok=True)

    if not os.path.exists(raw_dir):
        print("Directorio 'files/raw' no existe, creando archivos de prueba...")
        os.makedirs(raw_dir, exist_ok=True)
        with open(os.path.join(raw_dir, "sample.txt"), "w", encoding="utf-8") as f:
            f.write("Hola mundo\nMap Reduce en Python.\nHola, ChatGPT!\n")

    raw_files = os.listdir(raw_dir)
    for i in range(n):
        for f in raw_files:
            src = os.path.join(raw_dir, f)
            dst = os.path.join(input_dir, f"copy_{i}_{f}")
            shutil.copy(src, dst)


def load_input(input_directory):
    """Load all lines into a DataFrame"""
    lines = []
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines.extend(f.readlines())
    return pd.DataFrame({"line": lines})


def preprocess_text(text):
    """Clean text: lowercase and remove punctuation"""
    text = text.strip().lower()
    text = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", text)
    return text


def run_job(input_directory, output_directory):
    # Load
    df = load_input(input_directory)

    # Preprocess
    df["clean_line"] = df["line"].apply(preprocess_text)

    # Split into words
    df["words"] = df["clean_line"].str.split()

    # Explode words to rows
    words = df.explode("words").dropna(subset=["words"])

    # Count frequencies
    word_counts = words["words"].value_counts().reset_index()
    word_counts.columns = ["word", "count"]

    # Save output
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, "part_00000")
    word_counts.to_csv(output_file, sep="\t", index=False)

    # Create marker
    with open(os.path.join(output_directory, "_SUCCESS"), "w", encoding="utf-8") as f:
        f.write("Job completed successfully.\n")


if __name__ == "__main__":
    input_dir = os.path.join(FILES_DIR, "input")
    output_dir = os.path.join(FILES_DIR, "output")

    copy_raw_files_to_input_folder(n=10)

    start_time = time.time()

    run_job(input_dir, output_dir)

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")

