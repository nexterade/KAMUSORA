# Project — Tutorial

## Bootstrap

1. Define project identity in `PROJECT_BOOT.md` and `docs/STATE.md`.
2. Define the first useful behavior in `docs/BACKLOG.md`.
3. Define architecture boundaries in `docs/ARCHITECTURE.md`.
4. Implement only after the plan is clear.
5. Test the actual implementation.
6. Sync documentation.
7. Package and validate the exact artifact.

## New-chat continuation

Upload the latest project ZIP and use the continuation protocol defined in
`docs/CHECKPOINT.md` and `PROJECT_CONTINUATION.md`.

## Mengubah Perjalanan

Perjalanan punya presentation layer terkunci (tema, layout, search, index) dan content layer append-only.
1. Tambahkan `article.entry-card` baru HANYA di antara `PERJALANAN CONTENT START` dan `END`, urut kronologis. Skema entry ada di komentar paling atas file.
2. `python3 scripts/perjalanan_tool.py manifest --append`
3. `python3 scripts/perjalanan_tool.py check`
4. `python3 -m unittest discover -s tests -v`

Koreksi entry lama atau perubahan tema butuh persetujuan eksplisit user, lalu `manifest --accept-correction ID` atau `lock --accept-presentation-change`.

## Perjalanan adoption gate

Genesis Starter mengirim `docs/Perjalanan.html` dalam keadaan kosong. Setelah Starter
menjadi Project X, Perjalanan wajib dipakai sebagai historical record canonical. Entry
pertama harus merekam konsep yang telah dipilih dan disetujui user dengan:

- `data-origin="selected-concept"`
- `data-approval="user-approved"`

Jalankan `python3 scripts/perjalanan_tool.py adoption` sebelum melanjutkan development.
Starter kosong memang akan ditolak oleh gate ini; itu normal.


## Project identity and birth
After the user explicitly selects a project concept, record that decision in `PROJECT_ACCEPTANCE.json`. Only then may the derived project activate Brand Replacement Exception in `PROJECT_IDENTITY.json`. Provenance is retained separately from active branding.

## Translator universal input

Masukkan teks dalam Bahasa Indonesia, English, Romaji, atau tulisan Jepang pada satu form. Tidak perlu memilih bahasa sumber. Tekan **TRANSLATE** atau **Enter**; gunakan **Shift+Enter** untuk baris baru yang disengaja. Pada perangkat mobile, submit menutup keyboard virtual dan membawa panel hasil ke layar; hasil menampilkan tulisan Jepang, Romaji, dan arti yang tersedia pada dataset lokal. Untuk frasa yang punya grup relasi, exact match tetap tampil pertama lalu maksimal empat hasil terkait unik ditampilkan di bawahnya; setiap kartu terkait memiliki tombol salin Japanese dan Romaji. Untuk kata dasar seperti `good`, KAMUSORA dapat menampilkan pilihan frasa terkait yang bisa diketuk, misalnya `good night` atau `good morning`. Untuk kata kontekstual seperti `selamat`, pilih frasa yang sesuai sebelum menerjemahkan. Opsi bersumber dari dataset lokal, dideduplikasi, dan dibatasi maksimal delapan; frasa yang belum ada tetap dapat tidak ditemukan. Contoh di placeholder bukan jaminan bahwa seluruh variasi frasa tersedia. Auto-detect dan auto-correction berbasis heuristik/dataset lokal. Typo berkeyakinan tinggi dapat dikoreksi otomatis dengan opsi mengembalikan teks asli; kasus ambigu menampilkan saran tanpa mengubah input. Koreksi kalimat memakai pola lokal terbatas, bukan pemeriksa tata bahasa universal.

## Run KAMUSORA with Termux

Install Python in Termux (`pkg install python`), enter the folder containing `index.html` and `web/`, then run:

```bash
python -m web . --port 8080
```

Open `http://127.0.0.1:8080` on the same phone. To allow other devices on a trusted LAN, use `python -m web . --host 0.0.0.0 --port 8080` and browse to the phone's LAN IP from the other device. Stop with `Ctrl+C`. This launcher serves static files; it is not an application backend.
