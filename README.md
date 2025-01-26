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
- File ini berisi 100836 baris dengan 4 kolom, yaitu:
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
1. Drop Kolom
Pada tahap ini, kolom timestamp pada file ratings.csv dihapus karena tidak diperlukan dan tidak memiliki relasi yang cukup signifikan untuk proses rekomendasi.
2. Merge Data
Pada tahap ini, dilakukan proses menggabungkan dua set data (data_ratings dan data_movie) berdasarkan kolom movieId yang mereka miliki bersama. Metode merge digunakan dengan parameter how='inner' untuk melakukan 'inner join', yang berarti hanya baris-baris dengan movieId yang cocok pada kedua data akan dimasukkan dalam hasil gabungan.
3. Normalisasi
Tahapan normalisasi bertujuan untuk mengubah nilai pada kolom numerik ke dalam skala yang seragam tanpa menghilangkan perbedaan dalam rentang nilai. Dalam proyek ini, kolom rating pada file ratings.csv dinormalisasi menggunakan metode `Min-Max Scaling`. Metode ini bekerja dengan menggunakan nilai minimum dan setiap nilai pada fitur, kemudian membaginya dengan selisih antara nilai maksimum dan nilai minimum pada fitur tersebut.
4. Encoding
Pada tahap ini dilakukan proses encoding  untuk mengodekan ID pengguna (userId) dan ID film (movieId) menjadi representasi numerik yang lebih mudah digunakan dalam model pembelajaran mesin dengan semua nilai unik pada kolom userId diubah menjadi daftar dan dibuat dua kamus: 

- encoderUser yang memetakan userId ke indeks numeriknya;
- encodertoUser yang memetakan sebaliknya, dari indeks numerik ke userId. 

Kolom baru user di dalam dataset kemudian diisi dengan nilai yang dipetakan berdasarkan encoderUser. Jumlah total pengguna unik disimpan dalam n_user. Proses serupa dilakukan untuk movieId, dimana semua nilai unik pada kolom ini diubah menjadi daftar dan dua kamus serupa dibuat: 

- encoderMovie yang memetakan movieId ke indeks numeriknya;
- encodertoMovie yang memetakan sebaliknya, dari indeks numerik ke movieId.

Kolom baru movie kemudian diisi dengan nilai yang dipetakan berdasarkan encoderMovie, dan jumlah total film unik disimpan dalam n_movie. Proses ini sangat penting untuk persiapan data dalam model pembelajaran mesin, agar ID yang lebih deskriptif menjadi angka sederhana.

5. Splitting:
Proses split data dilakukan dengan membabi data menjadi data train dan test, yang mana pembagian data dirujuk pada variabel X (user, movie) yang digunakan untuk representasi fitur data dan y (rating) yang digunakan untuk representasi label data.
- Adapun ukuran pembagian data di dasari pada ukuran test data yakni 200000, sedangkan pada ukuran train data menyesuaikan yang di impelementasikan dengan metode indeks slicing.
- Sehingga diperoleh bahwa train data sebesar 1672:  dan test data sebesar : 99164


## Modeling & Result
Dalam proyek ini digunakan model dengan teknik embedding, yaitu Neural Collaborative Filtering (NCF). NCF adalah sebuah jaringan saraf tiruan yang menerapkan metode collaborative filtering berdasarkan umpan balik implisit, yang mampu merekomendasikan produk berdasarkan interaksi antara pengguna dan item. Sebagai contoh, model ini dapat merekomendasikan film berdasarkan skor rating yang diberikan oleh pengguna. Proses modeling dilakukan dengan menggunakan model deep learning dengan model arsitektur sebagai berikut: 
- Input layer
- Embedding layer
- Dot product layer
- Flatten layer
- Dense layer
- Output layer

Dari setiap model yang disusun berdasarkan arsitektur tersebut dilakukan inisialisasi model berdasarkan input user dan movie yang digunakan sebagai representasi fitur data, X di output layer sebagai representasi label data. setiap model di compile dengan loss function, metrics, dan optimizer. Adapun susunan arsitektur model yang digunakan sebagai berikut:

| Layer (type)          | Output Shape    | Param #      | Connected to      |
|-----------------------|-----------------|--------------|-------------------|
| user (InputLayer)     | (None, 1)       | 0            | -                 |
| movie (InputLayer)    | (None, 1)       | 0            | -                 |
| user_embedding        | (None, 1, 128)  | 78,080       | user[0][0]        |
| (Embedding)           |                 |              |                   |
| movie_embedding       | (None, 1, 128)  | 1,244,672    | movie[0][0]       |
| (Embedding)           |                 |              |                   |
| dot_product (Dot)     | (None, 1, 1)    | 0            | user_embedding[0…|
|                       |                 |              | movie_embedding[…|
| flatten (Flatten)     | (None, 1)       | 0            | dot_product[0][0] |
| dense (Dense)         | (None, 1)       | 2            | flatten[0][0]     |
| activation            | (None, 1)       | 0            | dense[0][0]       |
| (Activation)          |                 |              |                   |

Arsitektur model dilakukan tahapan inisialisasi dan dilakukan  proses training  dengan  melakukan training model dengan data train untuk training dan data test untuk validasi model di setiap epoch, serta memanggil beberapa callback, yaitu Early Stopping, Model Checkpoin.
Pada proses training dilakukan dengan menyimpan bobot model pada file tertentu dan menambahkan beberapa callback penting selama proses pelatihan model dengan TensorFlow atau Keras. 
- ModelCheckpoint digunakan untuk menyimpan bobot model terbaik ke dalam file ./weight.weights.h5, hanya menyimpan bobot (tanpa arsitektur model), dan memantau nilai val_loss untuk memastikan model hanya menyimpan bobot ketika val_loss mencapai angka terendah selama pelatihan. 
- EarlyStopping adalah callback lain yang digunakan untuk menghentikan pelatihan lebih awal jika tidak ada perbaikan pada metrik yang dipantau (mse dalam hal ini) berdasarkan mode 'min', yang juga mengembalikan bobot terbaik yang dihasilkan selama pelatihan. 

Kedua callback ini dimasukkan ke dalam list my_callbacks dan diteruskan ke fungsi fit untuk memulai pelatihan model. 
- Fungsi fit ini melatih model dengan data pelatihan (X_train, y_train) dan memvalidasi dengan data uji (X_test, y_test) selama 30 epoch dengan ukuran batch sebesar 32, menggunakan semua callback yang telah ditentukan.

Hasil yang diperoleh dalam proses training dapat berupa  weight_model yang bertujuan untuk mengambil bobot dari lapisan model tertentu (dalam hal ini, melalui parameter name dan model). Pertama, fungsi mengambil bobot dari lapisan yang ditentukan menggunakan metode get_layer() pada model. Bobot ini kemudian dinormalisasi dengan membagi setiap vektor bobot dengan normanya, yang dihitung menggunakan np.linalg.norm(). Normalisasi ini dilakukan untuk memastikan bahwa bobot memiliki panjang jednot, yang penting untuk berbagai operasi pembelajaran mesin seperti kesamaan kosinus. Hasil dari fungsi ini adalah bobot yang telah dinormalisasi dan fungsi weight_model digunakan untuk mengekstrak bobot dari lapisan pengukuran movie_embedding dan user_embedding dalam model yang sama.

Adapun `Hasil` yang dapat diperoleh dari implementasi dari `get_similar_users` yang bertujuan untuk mengidentifikasi pengguna yang mirip berdasarkan parameter tertentu. Fungsi ini membutuhkan tempId (identifikasi sementara pengguna) dan n (jumlah pengguna mirip yang ingin ditemukan, dengan default 10). Dalam fungsi ini, index diatur ke tempId dan weights diinisialisasi dengan user_weight, yang mungkin merupakan matriks bobot pengguna. Fungsi kemudian menghitung jarak (atau kesamaan) antara pengguna yang dicari dan seluruh pengguna lainnya menggunakan np.dot. Hasil dari perhitungan jarak diurutkan dengan np.argsort dan mengambil n pengguna dengan jarak terdekat menggunakan indeks terurut. Setelah pengguna dengan jarak terdekat ditemukan, fungsi akan mencetak ID pengguna yang mirip dan menyimpan pasangan pengguna dengan tingkat kemiripannya dalam SimilarArr. Setelah iterasi selesai, output disimpan dalam bentuk DataFrame Frame dan dikembalikan sebagai hasil akhir. Adapun hasilnya sebagai berikut:

| Rank | User ID |
|------|---------|
| 0    | 459     |
| 1    | 186     |
| 2    | 450     |
| 3    | 568     |
| 4    | 1       |
| 5    | 406     |
| 6    | 602     |
| 7    | 323     |
| 8    | 264     |
| 9    | 81      |
| 10   | 393     |

Untuk mengimplementasikan movie yang akan direkomendasikan ke pengguna, Anda dapat menggunakan metode top-n recommendation berdasarkan similar user  yang dapat digunakan untuk mendapatkan daftar film yang telah ditonton oleh pengguna. Berikut adalah tahapan untuk mendapatkan daftar rekomendasi film berdasarkan perilaku pengguna, yang dalam hal ini mencakup pemberian rating terhadap film yang telah ditonton:
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

    Metode Mean Squared Error (MSE) digunakan untuk mengukur sejauh mana kesalahan dalam prediksi. Semakin kecil nilai MSE, mendekati nol, semakin baik hasil prediksi tersebut, karena menunjukkan bahwa prediksi sangat mendekati data asli. Hal ini menjadikan metode ini relevan untuk digunakan dalam evaluasi prediksi di masa mendatang. MSE juga berfungsi sebagai alat evaluasi untuk berbagai model seperti regression, moving average, weighted moving average, dan analisis trendline. Perhitungan MSE dilakukan dengan mengurangi nilai aktual dengan nilai prediksi, mengkuadratkan selisihnya, menjumlahkan seluruh hasil, lalu membaginya dengan jumlah data yang ada. Dalam proyek ini, nilai MSE yang diperoleh adalah 0.01 untuk data train dan 0.06 untuk data testing. Grafik berikut menunjukkan hasil MSE, di mana MSE pada Train mengalami penurunan, sedangkan MSE pada Test cenderung stabil dengan sedikit penurunan yang tidak signifikan

    <img src="Hasil\MSE.png" style="zoom:70%;" />

2. Precision

    Precision mengukur ketepatan informasi yang dihasilkan oleh sistem dibandingkan dengan informasi yang dicari oleh pengguna. Dalam proyek ini, nilai precision yang dicapai adalah 1.0000 untuk data training dan 0.986 untuk data test. Grafik di bawah ini menunjukkan hasil precision, di mana precision pada Train cenderung meningkat, sementara precision pada Test tetap stabil sepanjang pengujian.

    <img src="Hasil\Precision.png" style="zoom:70%;" />

3. Recall 

    Recall menggambarkan kemampuan sistem untuk menemukan kembali informasi yang relevan. Proyek ini menghasilkan nilai recall sebesar 0.89 untuk data train dan 1.00 untuk data test. Grafik berikut menunjukkan hasil recall, dengan recall pada Test yang terus meningkat, sementara recall pada Train menunjukkan pola menurun dengan sedikit fluktuasi.

    <img src="Hasil\Recall.png" style="zoom:70%;" />

## Conclusions

Pada bagian kesimpulan ini berisikan sebuah jawaban dari problem statment berdasarkan result dan evaluasi yang di peroleh
1. Meningkatkan pengalaman pengguna dapat dilakukan dengan implementasi sebuah sistem rekomendasi berdasarkan perilaku pengguna, hal ini dapat dilakukan dengan mendapatkan sebuah similar user yang memiliki perilaku yang mirip dengan perilaku pengguna tersebut, dapat dilihat bahwa paada user 393. Memperoleh sebuah similar user sebagai berikut:
#### User that similar to user #393

| Rank | User ID |
|------|---------|
| 0    | 459     |
| 1    | 186     |
| 2    | 450     |
| 3    | 568     |
| 4    | 1       |
| 5    | 406     |
| 6    | 602     |
| 7    | 323     |
| 8    | 264     |
| 9    | 81      |
| 10   | 393     |

Untuk mengetahui sebuah performa model dalam memetakan similar user berdasarkan perilaku nya, dapat dilihat dari evaluasi model yang di lakukan selama proses training yang mana pada tahap ini terdapat evaluasi pada model MSE, recall, dan precision.
- Nilai Mean Squared Error (MSE) sebesar 0.01 untuk data train dan 0.06 untuk data testing.
- Nilai Precision sebesar 1.0000 untuk data training dan 0.0986 untuk data test
- Nilai Recall sebesar 0.89 untuk data train dan 1.00 untuk data test
Jika dilihat dari performa model bahwa model dapat memetakan similar user dengan baik, dengan nilai pada MSE pada data train dan test sebesar 0.01 dan 0.06. Dan nilai precision dan recall sebesar 1.0000 dan 0.89 untuk data training serta 0.986 dan 1.00 untuk data test. Dengan demikian dapat dikatakan bahwa model dapat memetakan similar user dengan baik. Jika dilihat bahwa loss MSE yang diperoleh 0.01 dan 0.06 yang cukup similar yang mana menandakan bahwa model good fit, sedangkan hasil pada precision dan recal pada data test cukup baik dengan nilai sebesar 0.986 dan 1.00 pada data test yang menandakan bahwa model dapat memetakan similar user dengan baik yang mana false 1 dan false 2 di estimasikan minim terjadi.



2. Cara mengimplementasikan pendekatan collaborative filtering dilakukan berdasarkan kedekatan user nya dengan top-n recommendatin method, berikut tahapan yang dapat dilakukan untuk mengimplementasikan pendekatan collaborative filtering:
    1. Mengidentifikasi daftar film yang telah ditonton oleh pengguna, kemudian data tersebut dimasukkan ke dalam dataframe baru dengan parameter userId, plot diatur ke False, dan temp diatur bernilai 1.
    2. Menentukan film dengan rating terendah dari data yang sesuai, menggunakan parameter rating_df.userId dengan nilai yang sama seperti userId.
    3. Membuat referensi film terbaik (top_movie_reference) berdasarkan urutan rating dengan parameter sort_values pada kolom "rating" dan pengaturan ascending bernilai False.
    4. Membentuk dataframe baru, user_pref_df, dari dataframe utama movie_df, yang kemudian difilter agar hanya berisi data film yang masuk dalam top_movie_reference. Dalam tahap ini, parameter movie_df difokuskan pada movieId dan menggunakan isin dari top_movie_reference.
    5. Menghitung rata-rata rating dari film yang telah dinilai oleh pengguna, menggunakan parameter rating_df.userId dengan nilai yang sama seperti userId.

### Rekomendasi Film untuk User ID #393

Berikut ini adalah hasil implementasi dengan pendekatan collaborative filtering berdasarkan kedekatan user nya dengan top-n recommendatin method, daftar rekomendasi film  dari user dengan ID #393 yang telah mereview 68 film dengan rata-rata ratingnya adalah 5.0/5.0 yang mana dapat dilihat pada tabel berikut:

| Rank | Movie ID | Title                                                 | Genres                           |
|------|----------|-------------------------------------------------------|----------------------------------|
| 1    | 457.0    | Fugitive, The (1993)                                  | Thriller                         |
| 2    | 1089.0   | Reservoir Dogs (1992)                                 | Crime|Mystery|Thriller           |
| 3    | 1198.0   | Raiders of the Lost Ark (Indiana Jones and the...)    | Action|Adventure                 |
| 4    | 1206.0   | Clockwork Orange, A (1971)                            | Crime|Drama|Sci-Fi|Thriller      |
| 5    | 1291.0   | Indiana Jones and the Last Crusade (1989)             | Action|Adventure                 |
| 6    | 2329.0   | American History X (1998)                             | Crime|Drama                      |
| 7    | 2571.0   | Matrix, The (1999)                                    | Action|Sci-Fi|Thriller           |
| 8    | 2959.0   | Fight Club (1999)                                     | Action|Crime|Drama|Thriller      |
| 9    | 2997.0   | Being John Malkovich (1999)                           | Comedy|Drama|Fantasy             |
| 10   | 3793.0   | X-Men (2000)                                          | Action|Adventure|Sci-Fi          |

