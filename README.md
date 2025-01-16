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
| movieId | title	                                   | genres                                      |
|---------|------------------------------------------|---------------------------------------------|
| 1       | Toy Story (1995)                         | Adventure-Animation-Children-Comedy-Fantasy |
| 2       | Jumanji (1995)                           | Adventure-Children-Fantasy                  |
| 3       | Grumpier Old Men (1995)	                 | Comedy-Romance                              |
| 4       | Waiting to Exhale (1995)                 | Comedy-Drama-Romance                        |
| 5       | Father of the Bride Part II (1995)       | Comedy                                      |
| ......  | ........................................ | ........................................... |
| 193581  | Black Butler: Book of the Atlantic (2017)| Action-Animation-Comedy-Fantasy             |
| 193583	| No Game No Life: Zero (2017)	           | Animation-Comedy-Fantasy                    |
| 193585  | Flint (2017)                             | Drama                                       |
| 193587  | Bungo Stray Dogs: Dead Apple (2018)      | Action-Animation                            |
| 193609  | Andrew Dice Clay: Dice Rules (1991)		   | Comedy                                      |

2. rating_df
Dataframe ini memuat sebuah data dari file ratings.csv. Pada tahap ini kolom timestamp telah dihapus karena tidak diperlukan. Dataframe rating ditunjukkan dalam tabel di bawah ini:
| userId | movieId | rating |
|--------|---------|--------|
| 1	     | 1	     | 4.0    |
| 1	     | 3	     | 4.0    |
| 1	     | 6	     | 4.0    |
| 1	     | 47	     | 5.0    |
| 1	     | 50	     | 5.0    |
| ...... | ....... | ...... |
| 610    | 166534  | 4.0    |
| 610    | 168248  | 5.0    |
| 610    | 168250  | 5.0    |
| 610    | 168252  | 5.0    |
| 610    | 170875  | 3.0    |