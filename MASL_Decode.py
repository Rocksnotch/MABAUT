from pathlib import Path
import re
import os

def natural_key(path: Path):
    parts = re.split(r'(\d+)', path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def unpack_9bit(data: bytes) -> str:
    if not data:
        return ""
    bits = "".join(format(b, "08b") for b in data)
    out = []
    i = 0
    n = len(bits)
    while i + 9 <= n:
        if bits[i] == "1":
            val = int(bits[i + 1:i + 9], 2)
            if 32 <= val <= 126:
                out.append(chr(val))
                i += 9
                continue
        i += 1
    return "".join(out).rstrip()

def try_decode(raw: bytes) -> str:
    if not raw:
        return ""
    data = raw
    if data and data[0] == 0x02:
        data = data[1:]
    if len(data) >= 2 and data[-2:] == b"\x03\x04":
        data = data[:-2]

    for i, b in enumerate(data):
        if 0xA0 <= b <= 0xBF:
            msg = unpack_9bit(data[i:])
            if len(msg) >= 2:
                return msg

    # Otherwise try the whole buffer
    msg = unpack_9bit(data)
    if len(msg) >= 2:
        return msg
    return ""

def extract_message(path: Path) -> str:
    raw = path.read_bytes()

    msg = try_decode(raw)
    if msg:
        return msg

    # preserves all bytes
    text = raw.decode("latin-1")  
    hex_chars = re.sub(r"[^0-9a-fA-F]", "", text)
    hex_ratio = len(hex_chars) / max(len(text), 1)
    if hex_ratio > 0.65 and len(hex_chars) >= 8:
        if len(hex_chars) % 2:
            hex_chars = hex_chars[:-1]
        try:
            as_hex = bytes.fromhex(hex_chars)
            msg = try_decode(as_hex)
            if msg:
                return msg
        except Exception:
            pass

    cleaned = "".join(
        ch for ch in text
        if 32 <= ord(ch) <= 126 or ch in "\n\t"
    )
    return cleaned.strip()

def process_folder(folder: str):
    folder_path = Path(folder).expanduser()
    print(f"Input folder: {folder_path}")

    if not folder_path.exists() or not folder_path.is_dir():
        print("ERROR: Folder does not exist or is not a directory.")
        return

    try:
        files = sorted(
            [p for p in folder_path.iterdir() if p.is_file()],
            key=natural_key
        )
    except PermissionError as e:
        print(f"ERROR: Cannot read folder: {e}")
        return

    if not files:
        print("No files found in the folder.")
        return

    out_path = Path(os.getcwd()) / "decoded_output.txt"
    print(f"Found {len(files)} files")
    print(f"Writing output to: {out_path}")

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Scanning: {folder_path}\n\n")
        for file_path in files:
            try:
                message = extract_message(file_path)
                f.write(f"{file_path.name}\n")
                f.write(f"{message if message else '<no printable message>'}\n\n")
            except Exception as e:
                f.write(f"{file_path.name}\n<error: {e}>\n\n")

    print("Finished successfully.")
    print(f"Results written to: {out_path}")

if __name__ == "__main__":
    folder = input("Folder path: ").strip().strip('"') or "."
    process_folder(folder)