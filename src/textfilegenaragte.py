def generate_large_file(file_name, size_in_gb):
    # 1GBは約1,073,741,824バイト
    size_in_bytes = size_in_gb * 1073741824
    chunk_size = 1024 * 1024  # 1MB
    written_bytes = 0

    with open(file_name, 'w') as f:
        while written_bytes < size_in_bytes:
            remaining_bytes = size_in_bytes - written_bytes
            write_size = min(chunk_size, remaining_bytes)
            f.write('A' * write_size)
            written_bytes += write_size


file_name = "c:/temp/large_file.txt"
size_in_gb = 4  # 4GBのファイルを生成
generate_large_file(file_name, size_in_gb)

print(f"{file_name} has been created with size {size_in_gb} GB.")
