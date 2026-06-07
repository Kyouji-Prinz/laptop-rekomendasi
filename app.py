import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from recom_system import rekomendasi_laptop

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil_rekomendasi = None
    sudah_submit = False
    
    if request.method == 'POST':
        sudah_submit = True
        budget_min_raw = request.form.get('budget_min')
        budget_max_raw = request.form.get('budget_max')
        kebutuhan = request.form.get('kebutuhan')
        merek = request.form.get('merek')
        
        budget_minimal = int(budget_min_raw.replace('.', '')) if budget_min_raw else 0
        budget_maksimal = int(budget_max_raw.replace('.', '')) if budget_max_raw else 999000000
            
        if merek == 'Semua':
            merek = None
            
        df_hasil = rekomendasi_laptop(
            budget_minimal=budget_minimal,
            budget_maksimal=budget_maksimal,
            tipe_kebutuhan=kebutuhan,
            preferensi_merek=merek
        )
        
        if 'Pesan' in df_hasil.columns:
            hasil_rekomendasi = "tidak_ditemukan"
        else:
            hasil_rekomendasi = df_hasil.to_dict(orient='records')
            
    return render_template('index.html', hasil=hasil_rekomendasi, submit=sudah_submit)


# =========================================================
# RUTE BARU: MENANGKAP & MENYIMPAN FEEDBACK KE CSV
# =========================================================
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    nama = request.form.get('nama_user')
    pesan = request.form.get('pesan_feedback')
    
    # Menangani jika temanmu membiarkan nama kosong
    if not nama or nama.strip() == "":
        nama = "Anonim"
        
    if pesan:
        # Cek apakah file feedback.csv sudah ada sebelumnya
        file_exists = os.path.isfile('feedback.csv')
        
        # Membuka (atau membuat) file CSV dengan mode 'a' (append)
        with open('feedback.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Jika ini adalah feedback pertama, buat header kolomnya terlebih dahulu
            if not file_exists:
                writer.writerow(['Waktu', 'Nama', 'Pesan_Feedback'])
                
            # Mencatat waktu saat ini dan menuliskannya ke baris baru
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([waktu_sekarang, nama, pesan])
            
    # Mengembalikan pengguna ke halaman utama
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)