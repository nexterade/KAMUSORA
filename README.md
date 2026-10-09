# KAMUSORA

**Japanese ↔ Romaji, with English & Indonesian meaning.**

Translator uses one universal input and automatically detects Indonesian, English, Romaji, or Japanese script. The bundled dataset is finite; detection and correction are heuristic, exact valid input takes precedence, and unmatched phrases are not invented.

KAMUSORA exists to solve a small but common discovery problem: someone knows a Japanese word or meaning but does not know the name of the Latin-letter representation they are looking for — **romaji**.

## Core product

- One input auto-detects Indonesian, English, Romaji, and Japanese script.
- Results adapt to the detected input: Romaji input avoids repeating the same Romaji in the primary result; related phrase cards include complete Romaji, Japanese script, and English/Indonesian meanings. Short English/Indonesian root words can also expose up to eight clickable local phrase continuations; ambiguous roots such as `selamat` prompt for context.
- Exact phrase matches stay first; up to four relevant, deduplicated related phrases may appear below. Related cards provide Japanese/Romaji copy controls. Hybrid local auto-correction can repair high-confidence word/phrase typos and selected sentence patterns, show undo for automatic changes, and ask the user to choose when ambiguous. Valid exact matches remain untouched. Enter submits; Shift+Enter inserts a newline. On mobile, submission closes the keyboard and focuses the result.
- Large Romaji-indexed dictionary browsable A–Z

## Runtime

Standalone HTML. No external API is required for v0.3.6. Release ZIPs exclude other ZIP archives and checkpoint backups. The bundled dataset is intentionally local and finite; related phrases and corrections must be supported by local records or curated patterns, ambiguous corrections require user choice, and unmatched phrases are not silently invented.

## Build & test

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py [OUTPUT_DIR]
```

## Menjalankan di Android lewat Termux (localhost)

Panduan ini untuk menjalankan versi standalone di browser HP Android menggunakan server HTTP Python lokal. Server hanya dapat diakses dari perangkat yang sama jika menggunakan `127.0.0.1`.

### 1. Pasang kebutuhan

Buka Termux, lalu jalankan:

```bash
pkg update
pkg install python unzip
```

### 2. Simpan dan ekstrak ZIP

Unduh ZIP KAMUSORA ke folder **Download** Android. Beri Termux izin akses penyimpanan:

```bash
termux-setup-storage
```

Izinkan akses ketika diminta, lalu ekstrak arsip (sesuaikan nama ZIP jika berbeda):

```bash
cd ~/storage/downloads
unzip KAMUSORA-v0.3.6.zip -d ~/kamusora
```

### 3. Temukan folder yang berisi `index.html`

```bash
cd ~/kamusora
find . -maxdepth 3 -type f -name "index.html"
```

Masuk ke folder yang berisi `index.html`. Jika hasilnya `./index.html`, folder saat ini sudah benar. Jika hasilnya `./KAMUSORA/index.html`, jalankan `cd ~/kamusora/KAMUSORA`. ZIP release resmi menggunakan layout flat-root, sehingga biasanya hasilnya `./index.html`.

### 4. Jalankan server lokal KAMUSORA

KAMUSORA menyertakan launcher Python sederhana supaya perintahnya lebih ringkas. Dari folder utama project (folder yang berisi `index.html` dan folder `web/`), jalankan:

```bash
python -m web . --port 8080
```

Port `8080` adalah default. Kalau ingin port lain, ganti `8080`, misalnya `python -m web . --port 9000`. Secara default server hanya bind ke `127.0.0.1`, jadi hanya bisa dibuka dari HP itu sendiri. Untuk melepas bind localhost dan menerima koneksi dari perangkat lain di jaringan yang sama, jalankan `python -m web . --host 0.0.0.0 --port 8080`; buka menggunakan alamat IP lokal HP (bukan `127.0.0.1`) dari perangkat lain. Gunakan opsi ini hanya di jaringan tepercaya. Launcher memakai server HTTP bawaan Python untuk menyajikan file statis; tidak memerlukan instalasi paket tambahan.

Biarkan Termux tetap berjalan. Buka Chrome atau browser lain di HP yang sama, lalu kunjungi:

**http://127.0.0.1:8080**

### 5. Menghentikan atau menjalankan ulang

Untuk menghentikan server, kembali ke Termux dan tekan `CTRL + C`. Untuk menjalankan lagi, masuk kembali ke folder utama project dan ulangi perintah server di atas.

### Pemecahan masalah

- Jika muncul `Address already in use`, port yang dipilih sedang digunakan. Hentikan server sebelumnya atau gunakan port lain, misalnya `9000`, lalu jalankan `python -m web . --port 9000` dan buka `http://127.0.0.1:9000`.
- Jika browser menampilkan daftar file, kemungkinan server dijalankan dari folder yang salah. Hentikan dengan `CTRL + C`, masuk ke folder yang berisi `index.html`, lalu jalankan ulang.
- `python -m web` hanya menyajikan file statis. Versi standalone ini tidak memerlukan backend Python khusus atau API eksternal untuk sekadar dibuka. Fitur yang membutuhkan server backend khusus, jika ditambahkan di masa depan, perlu dijalankan terpisah.
