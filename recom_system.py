import pandas as pd

df_laptop = pd.read_csv('laptops_ready.csv')

def rekomendasi_laptop(budget_minimal, budget_maksimal, tipe_kebutuhan, preferensi_merek=None):
    # Logika filter diperluas untuk menangkap rentang harga minimal dan maksimal
    kondisi = (df_laptop['price_idr'] >= budget_minimal) & \
              (df_laptop['price_idr'] <= budget_maksimal) & \
              (df_laptop['laptop_type'] == tipe_kebutuhan)
    
    if preferensi_merek:
        kondisi = kondisi & (df_laptop['brand'].str.lower() == preferensi_merek.lower())
        
    hasil_filter = df_laptop[kondisi]
    
    if hasil_filter.empty:
        return pd.DataFrame({"Pesan": ["Maaf, tidak ada laptop yang sesuai dengan kriteria Anda."]})
    
    # Mengurutkan dari harga termurah ke termahal di dalam rentang, tanpa batasan .head()
    rekomendasi_semua = hasil_filter.sort_values(by='price_idr', ascending=True)
    
    kolom_tampil = ['brand', 'model', 'cpu', 'ram_gb', 'gpu', 'screen_specs', 'price_idr']
    return rekomendasi_semua[kolom_tampil]