import sqlite3  # Modul untuk berinteraksi dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Modul untuk membuat GUI

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuat atau membuka database 'nilai_siswa.db'
    cursor = conn.cursor()  # Membuat kursor untuk menjalankan perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        )
    ''')  # Membuat tabel jika belum ada
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat kursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan hasil query ke dalam variabel
    conn.close()  # Menutup koneksi database
    return rows  # Mengembalikan data

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat kursor
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  # Menambahkan data ke tabel
    ''', (nama, biologi, fisika, inggris, prediksi))  # Mengisi parameter dengan data
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk memperbarui data yang sudah ada
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat kursor
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  # Memperbarui data berdasarkan ID
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghapus data berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat kursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Jika Biologi tertinggi, prediksi fakultas adalah Kedokteran
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Jika Fisika tertinggi, prediksi fakultas adalah Teknik
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Jika Inggris tertinggi, prediksi fakultas adalah Bahasa
    else:
        return "Tidak Diketahui"  # Jika nilai sama, prediksi tidak diketahui

# Fungsi untuk menyimpan data baru melalui GUI
def submit():
    try:
        nama = nama_var.get()  # Mengambil nama dari input
        biologi = int(biologi_var.get())  # Mengambil nilai Biologi
        fisika = int(fisika_var.get())  # Mengambil nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil nilai Inggris
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan ke database
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk membersihkan input
def clear_inputs():
    nama_var.set("")  # Membersihkan input nama
    biologi_var.set("")  # Membersihkan input nilai Biologi
    fisika_var.set("")  # Membersihkan input nilai Fisika
    inggris_var.set("")  # Membersihkan input nilai Inggris
    selected_record_id.set("")  # Membersihkan ID yang dipilih

# Fungsi untuk memperbarui isi tabel GUI
def populate_table():
    for row in tree.get_children():  # Menghapus data di tabel
        tree.delete(row)
    for row in fetch_data():  # Menambahkan data baru ke tabel
        tree.insert('', 'end', values=row)
# Fungsi untuk mengisi input berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan item yang dipilih di tabel
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari item yang dipilih

        selected_record_id.set(selected_row[0])  # Mengisi ID record ke variabel
        nama_var.set(selected_row[1])  # Mengisi nama siswa ke input
        biologi_var.set(selected_row[2])  # Mengisi nilai Biologi ke input
        fisika_var.set(selected_row[3])  # Mengisi nilai Fisika ke input
        inggris_var.set(selected_row[4])  # Mengisi nilai Inggris ke input
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menampilkan pesan error jika tidak ada data yang dipilih

# Fungsi untuk memperbarui data melalui GUI
def update():
    try:
        if not selected_record_id.get():  # Mengecek apakah ID record sudah dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID record
        nama = nama_var.get()  # Mengambil nama siswa dari input
        biologi = int(biologi_var.get())  # Mengambil nilai Biologi
        fisika = int(fisika_var.get())  # Mengambil nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil nilai Inggris

        if not nama:  # Mengecek apakah nama siswa kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan input

# Fungsi untuk menghapus data melalui GUI
def delete():
    try:
        if not selected_record_id.get():  # Mengecek apakah ID record sudah dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID record
        delete_database(record_id)  # Menghapus data di database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan

# Inisialisasi database
create_database()  # Membuat database dan tabel jika belum ada

# Membuat GUI dengan tkinter
root = Tk()  # Membuat jendela utama
root.title("Prediksi Fakultas Siswa")  # Memberikan judul pada jendela

# Variabel tkinter
nama_var = StringVar()  # Variabel untuk input nama siswa
biologi_var = StringVar()  # Variabel untuk input nilai Biologi
fisika_var = StringVar()  # Variabel untuk input nilai Fisika
inggris_var = StringVar()  # Variabel untuk input nilai Inggris
selected_record_id = StringVar()  # Variabel untuk menyimpan ID record yang dipilih

# Membuat label dan input untuk nama siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # Label nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # Input nama siswa

# Membuat label dan input untuk nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # Label nilai Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # Input nilai Biologi

# Membuat label dan input untuk nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # Label nilai Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # Input nilai Fisika

# Membuat label dan input untuk nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # Label nilai Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # Input nilai Inggris

# Membuat tombol Add, Update, dan Delete
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # Tombol untuk menambahkan data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol untuk memperbarui data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol untuk menghapus data

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # Kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel

# Mengatur posisi dan lebar kolom di tabel
for col in columns:
    tree.heading(col, text=col.capitalize())  # Memberikan nama pada kolom
    tree.column(col, anchor='center')  # Mengatur posisi isi kolom di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di GUI

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Menghubungkan tabel dengan fungsi untuk mengisi input

populate_table()  # Memperbarui tabel dengan data dari database

root.mainloop()  # Menjalankan loop utama GUI
