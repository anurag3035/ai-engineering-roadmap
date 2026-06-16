# generator_pipeline.py

def read_file(file_name):
    with open(file_name, "r") as file:
        for line in file:
            yield line


def remove_blank_lines(lines):
    for line in lines:
        line = line.strip()
        if line:
            yield line


def make_chunks(lines, chunk_size):

    chunk = []

    for line in lines:
        chunk.append(line)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
        if chunk:
          yield chunk



with open("large_file.txt", "w") as file:
    for i in range(1, 10001):
        file.write(f"This is line number {i}\n")
        if i % 50 == 0:
            file.write("\n")



file_lines = read_file("large_file.txt")
clean_lines = remove_blank_lines(file_lines)
chunks = make_chunks(clean_lines, 100)

print("Processing file...\n")

chunk_count = 0
for chunk in chunks:
    chunk_count += 1

    print(
        f"Chunk {chunk_count} contains {len(chunk)} lines."
    )
    print("First line:", chunk[0])
    print("-" * 40)
    if chunk_count == 5:
        break