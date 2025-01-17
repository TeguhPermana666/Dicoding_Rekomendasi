# Report Sistem Rekomendasi Content Based 
- Nama : I Gede Teguh Permana

## Project Overview
Perkembangan teknologi informasi dan telekomunikasi terus mengalami peningkatan yang signifikan. Saat ini, hampir semua aspek kehidupan manusia memanfaatkan teknologi informasi dan komunikasi, termasuk dalam bidang musik dan perfilman. Film, sebagai media audio-visual, menawarkan beragam genre, seperti komedi, drama, horor, action, dan lainnya, yang membuatnya menjadi salah satu bentuk hiburan yang sangat populer di masyarakat.

Sejak tahun 1874 hingga 2015, tercatat sebanyak 3.361.741 judul film telah dirilis oleh industri perfilman. Jumlah judul yang begitu banyak sering kali menimbulkan kendala bagi penikmat film dalam menentukan film berikutnya yang akan ditonton. Informasi tentang film yang tersedia di berbagai situs web dapat diolah dan dimanfaatkan untuk memberikan rekomendasi film kepada pengguna lain. Masalah ini dapat diatasi dengan menyajikan daftar film yang direkomendasikan berdasarkan preferensi masing-masing pengguna. Oleh sebab itu, diperlukan sebuah sistem yang mampu memberikan rekomendasi film secara personal kepada pengguna.

Sistem rekomendasi adalah mekanisme yang mampu menyediakan informasi atau saran yang sesuai dengan minat pengguna berdasarkan data yang diperoleh dari pengguna tersebut. Oleh karena itu, dibutuhkan model rekomendasi yang efektif agar saran yang diberikan sistem sesuai dengan selera pengguna, sekaligus memudahkan pengguna dalam membuat keputusan terkait film yang akan ditonton. Salah satu metode yang banyak digunakan dalam sistem rekomendasi adalah Collaborative Filtering. Metode ini menghubungkan pengguna yang memiliki kesamaan preferensi terhadap suatu item (film) berdasarkan penilaian atau rating yang mereka berikan.

## Business Understanding
### 1. Problem Statements
Berdasarkan latar belakang yang telah dijelaskan, permasalahan dapat dirumuskan sebagai berikut:
- Bagaimana meningkatkan pengalaman pengguna dalam menemukan film yang diinginkan?
- Bagaimana cara mengimplementasikan pendekatan *collaborative filtering* dalam membangun sistem rekomendasi film?

### 2. Goals
Proyek ini bertujuan untuk:
- Meningkatkan pengalaman pengguna dalam mencari film yang sesuai dengan preferensi mereka.
- Mengaplikasikan metode collaborative filtering untuk merancang sistem rekomendasi film yang efektif.

### 3. Solusi
Berdasarkan rumusan masalah dan tujuan yang telah ditetapkan, solusi yang diusulkan adalah sebagai berikut:
- Mengimplementasikan pendekatan collaborative filtering dalam membangun sistem rekomendasi film. Metode ini dipilih karena data yang digunakan dalam proyek ini mencakup penilaian pengguna terhadap film-film yang telah mereka tonton. Pada pendekatan collaborative filtering, atribut utama yang dimanfaatkan adalah perilaku pengguna, seperti memberikan rekomendasi film berdasarkan riwayat penilaian dari pengguna tersebut maupun pengguna lainnya.

## Data Understanding
Dataset yang digunakan dalam proyek ini diambil dari website kaggle.com dan dapat diakses melalui tautan berikut: Movie Lens Dataset https://www.kaggle.com/datasets/suryadeepti/movie-lens-dataset. Dataset ini memiliki format .csv yang terdiri dari dua file, yaitu movies.csv dan ratings.csv. Berikut adalah deskripsi dari masing-masing file tersebut:
1. movies.csv
- File ini berisi 9742 baris dengan 3 kolom, yaitu:
    - movieId, merupakan *unique Id* untuk masing-masing film
    - title: Nama atau judul film, termasuk tahun rilis yang dicantumkan dalam tanda kurung.
    - genre: Genre atau kategori film
2. ratings.csv
- File ini berisi 10.1000 baris dengan 4 kolom, yaitu:
    - userId: *unique Id* untuk masing-masing *user*
    - movieId: *unique Id* untuk masing-masing film
    - rating: Penilaian berupa skor oleh user terhadap suatu film
    - timestamp: Waktu penilaian oleh user terhadap suatu film
### Overview Dataset
Dataset ini telah diubah menjadi dua dataframe, yaitu movie_df dan rating_df, dengan penjelasan sebagai berikut:

1. movie_df
Dataframe ini memuat data dari file movies.csv, yang mencakup informasi tentang film, seperti yang ditunjukkan dalam table di bawah ini:

| movieId | title                                    | genres                                      |
|---------|------------------------------------------|---------------------------------------------|
| 1       | Toy Story (1995)                         | Adventure-Animation-Children-Comedy-Fantasy |
| 2       | Jumanji (1995)                           | Adventure-Children-Fantasy                  |
| 3       | Grumpier Old Men (1995)                  | Comedy-Romance                              |
| 4       | Waiting to Exhale (1995)                 | Comedy-Drama-Romance                        |
| 5       | Father of the Bride Part II (1995)       | Comedy                                      |
| ......  | ........................................ | ........................................... |
| 193581  | Black Butler: Book of the Atlantic (2017)| Action-Animation-Comedy-Fantasy             |
| 193583  | No Game No Life: Zero (2017)             | Animation-Comedy-Fantasy                    |
| 193585  | Flint (2017)                             | Drama                                       |
| 193587  | Bungo Stray Dogs: Dead Apple (2018)      | Action-Animation                            |
| 193609  | Andrew Dice Clay: Dice Rules (1991)      | Comedy                                      |

2. rating_df
Dataframe ini memuat sebuah data dari file ratings.csv. Pada tahap ini kolom timestamp telah dihapus karena tidak diperlukan. Dataframe rating ditunjukkan dalam tabel di bawah ini:

| userId | movieId | rating |
|--------|---------|--------|
| 1      | 1       | 4.0    |
| 1      | 3       | 4.0    |
| 1      | 6       | 4.0    |
| 1      | 47      | 5.0    |
| 1      | 50      | 5.0    |
| ...... | ....... | ...... |
| 610    | 166534  | 4.0    |
| 610    | 168248  | 5.0    |
| 610    | 168250  | 5.0    |
| 610    | 168252  | 5.0    |
| 610    | 170875  | 3.0    |


## Data Preparation
Berikut adalah teknik *data preparation* yang diterapkan dalam proyek ini
1. Menghapus missing value:
Langkah ini dilakukan untuk memeriksa dan menangani missing value dalam dataet, keberadaan missing value dapat mempengaruhi performa model, sehingga data tanpa missing value akan meningkatkan kualitas hasil model. Proses ini dilakukan menggunakan fungsi dataframe.dropna(), yang akan menghapus baris yang mengandung nilai null pada dataset.
2. Normalisasi:
Tahapan normalisasi bertujuan untuk mengubah nilai pada kolom numerik ke dalam skala yang seragam tanpa menghilangkan perbedaan dalam rentang nilai. Dalam proyek ini, kolom rating pada file ratings.csv dinormalisasi menggunakan metode `Min-Max Scaling`. Metode ini bekerja dengan menggunakan nilai minimum dan setiap nilai pada fitur, kemudian membaginya dengan selisih antara nilai maksimum dan nilai minimum pada fitur tersebut.
3. Splitting:
Pada tahap ini, dataset akan dipisahkan menjadi dua bagian, yaitu data train dan data test. Data train digunakan untuk melatih model, sementara data test berfungsi untuk memvalidasi model. Dalam proyek ini, pembagian dataset mengikuti proporsi umum, yaitu 80% sebagai data train dan 20% sebagai data test. Proses pembagian diawali dengan mengacak sampel data sebelum membagi dataset tersebut. Pada proses splitting ini, terdapat parameter test_size yang menentukan ukuran data test, yaitu test_size=200000 untuk proyek ini. Selanjutnya, data akan dipisahkan untuk keperluan pemodelan menggunakan teknik slicing dengan format [baris, kolom], seperti [X_train[:, 0], X_train[:, 1], yang berarti mencakup semua baris, kolom pertama, dan kolom kedua.


## Model
Dalam proyek ini digunakan model dengan teknik embedding, yaitu Neural Collaborative Filtering (NCF). NCF adalah sebuah jaringan saraf tiruan yang menerapkan metode collaborative filtering berdasarkan umpan balik implisit, yang mampu merekomendasikan produk berdasarkan interaksi antara pengguna dan item. Sebagai contoh, model ini dapat merekomendasikan film berdasarkan skor rating yang diberikan oleh pengguna. Berikut adalah tahapan untuk mendapatkan daftar rekomendasi film berdasarkan perilaku pengguna, yang dalam hal ini mencakup pemberian rating terhadap film yang telah ditonton:

1. Mengidentifikasi daftar film yang telah ditonton oleh pengguna, kemudian data tersebut dimasukkan ke dalam dataframe baru dengan parameter userId, plot diatur ke False, dan temp diatur bernilai 1.
2. Menentukan film dengan rating terendah dari data yang sesuai, menggunakan parameter rating_df.userId dengan nilai yang sama seperti userId.
3. Membuat referensi film terbaik (top_movie_reference) berdasarkan urutan rating dengan parameter sort_values pada kolom "rating" dan pengaturan ascending bernilai False.
4. Membentuk dataframe baru, user_pref_df, dari dataframe utama movie_df, yang kemudian difilter agar hanya berisi data film yang masuk dalam top_movie_reference. Dalam tahap ini, parameter movie_df difokuskan pada movieId dan menggunakan isin dari top_movie_reference.
5. Menghitung rata-rata rating dari film yang telah dinilai oleh pengguna, menggunakan parameter rating_df.userId dengan nilai yang sama seperti userId.

Hasil dari sistem rekomendasi ini menunjukkan daftar 10 film teratas, dengan rata-rata rating tertinggi mencapai 5.0/5.0.

| movieId | title                                        | genres                            |
|---------|----------------------------------------------|-----------------------------------|
| 25      | Fugitive, The (1993)                        | Thriller                          |
| 62      | Reservoir Dogs (1992)                       | Crime\|Mystery\|Thriller          |
| 70      | Raiders of the Lost Ark (Indiana Jones and the...) | Action\|Adventure                |
| 71      | Clockwork Orange, A (1971)                  | Crime\|Drama\|Sci-Fi\|Thriller    |
| 89      | Indiana Jones and the Last Crusade (1989)   | Action\|Adventure                 |
| 147     | American History X (1998)                   | Crime\|Drama                      |
| 166     | Matrix, The (1999)                          | Action\|Sci-Fi\|Thriller          |
| 192     | Fight Club (1999)                           | Action\|Crime\|Drama\|Thriller    |
| 197     | Being John Malkovich (1999)                 | Comedy\|Drama\|Fantasy            |
| 228     | X-Men (2000)                                | Action\|Adventure\|Sci-Fi         |

## Evaluation

1. Mean Squared Error (MSE)

    Metode Mean Squared Error (MSE) digunakan untuk mengukur sejauh mana kesalahan dalam prediksi. Semakin kecil nilai MSE, mendekati nol, semakin baik hasil prediksi tersebut, karena menunjukkan bahwa prediksi sangat mendekati data asli. Hal ini menjadikan metode ini relevan untuk digunakan dalam evaluasi prediksi di masa mendatang. MSE juga berfungsi sebagai alat evaluasi untuk berbagai model seperti regression, moving average, weighted moving average, dan analisis trendline. Perhitungan MSE dilakukan dengan mengurangi nilai aktual dengan nilai prediksi, mengkuadratkan selisihnya, menjumlahkan seluruh hasil, lalu membaginya dengan jumlah data yang ada. Dalam proyek ini, nilai MSE yang diperoleh adalah 0.06 untuk data testing dan 0.01 untuk data train. Grafik berikut menunjukkan hasil MSE, di mana MSE pada Train mengalami penurunan, sedangkan MSE pada Test cenderung stabil dengan sedikit penurunan yang tidak signifikan

    <img src="Hasil\MSE.png" style="zoom:70%;" />

2. Precision

    Precision mengukur ketepatan informasi yang dihasilkan oleh sistem dibandingkan dengan informasi yang dicari oleh pengguna. Dalam proyek ini, nilai precision yang dicapai adalah 1.0000 untuk data training dan 0.0986 untuk data test. Grafik di bawah ini menunjukkan hasil precision, di mana precision pada Train cenderung meningkat, sementara precision pada Test tetap stabil sepanjang pengujian.

    <img src="Hasil\Precision.png" style="zoom:70%;" />

3. Recall 

    Recall menggambarkan kemampuan sistem untuk menemukan kembali informasi yang relevan. Proyek ini menghasilkan nilai recall sebesar 1.00 untuk data train dan 0.89 untuk data test. Grafik berikut menunjukkan hasil recall, dengan recall pada Train yang terus meningkat, sementara recall pada Test menunjukkan pola menurun dengan sedikit fluktuasi.

    <img src="Hasil\Recall.png" style="zoom:70%;" />

## Conclusions

Berdasarkan hasil proyek sistem rekomendasi, diperoleh kesimpulan sebagai berikut:

- Nilai Mean Squared Error (MSE) sebesar 0.0.06 untuk data testing dan 0.01 untuk data train.
- Nilai Precision sebesar 1.0000 untuk data training dan 0.0986
- Nilai Recall sebesar 1.00 untuk data train dan 0.89 untuk data test

