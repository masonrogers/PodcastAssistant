import io

CONTENT_LINES = [
    "Whisper Transcriber User Guide",
    "",
    "Installation:",
    "1. Install Python and FFmpeg.",
    "2. Run 'python build_installer.py' to create the executable.",
    "3. Launch the installer from 'dist/'.",
    "",
    "Basic Usage:",
    "1. Drag audio files into the file list in order.",
    "2. Click 'Transcribe' to process the files.",
    "3. Search or highlight segments in the transcript.",
    "",
    "Exporting:",
    "Use the Export buttons to save TXT, JSON, SRT, or a clipped audio segment.",
    "",
    "Keyword Management:",
    "Edit 'keywords.json' via the Settings dialog to update search terms.",
    "",
    "Uninstallation:",
    "Run 'python src/uninstaller.py' to remove dependencies."
]

def create_content_stream():
    lines = []
    y = 760
    lines.append("BT")
    lines.append("/F1 18 Tf")
    lines.append(f"72 {y} Td ({CONTENT_LINES[0]}) Tj")
    lines.append("/F1 12 Tf")
    y -= 28
    for line in CONTENT_LINES[2:]:
        if not line:
            y -= 14
            continue
        lines.append(f"72 {y} Td ({line}) Tj")
        y -= 14
    lines.append("ET")
    return "\n".join(lines)

def generate_pdf(path):
    objects = []
    content_stream = create_content_stream()
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    objects.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(
        "<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>"
    )
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(f"<< /Length {len(content_stream)} >>\nstream\n{content_stream}\nendstream")

    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, 1):
        offsets.append(pdf.tell())
        pdf.write(f"{idx} 0 obj\n{obj}\nendobj\n".encode("latin-1"))

    xref_pos = pdf.tell()
    pdf.write(f"xref\n0 {len(objects)+1}\n".encode("latin-1"))
    pdf.write(b"0000000000 65535 f \n")
    for off in offsets:
        pdf.write(f"{off:010d} 00000 n \n".encode("latin-1"))
    pdf.write(
        f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode(
            "latin-1"
        )
    )

    with open(path, "wb") as f:
        f.write(pdf.getvalue())

if __name__ == "__main__":
    generate_pdf("docs/user_guide.pdf")
