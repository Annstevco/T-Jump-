<h2>T-Jump  (Tubes PBO RC-06) </h2>

<h4>T-Jump Team : </h4>

1. Denny Prayoga Setiawan Halim         (120140012)

2. Annike Stella Cova                   (120140041)

3. Sultan Ahmad Alfath                  (120140046)

4. Reza Chairul Manam                   (120140086)

5. Mohammad Al Muktabar                 (120140222)

6. Yudha Kurnia Pratama                 (120140241)

<h2> Deskripsi Program : </h2>
  Program yang dibuat adalah sebuah game bernama T-Jump.
Pembuatan game ini menggunakan bahasa pemograman python dengan memanfaatkan library pygame. 
Program ini menerapkan konsep-konsep yang ada pada PBO(pemrograman berorientasi objek)/OOP(object oriented programming).
  
<h4>Cara Bermain : </h4>
  Player cukup menekan tombol keyboard anak panah ke kanan dan kiri (left arrow & right arrow) untuk menentukan arah pergerakan jumper. Ketika menekan panah ke kanan maka jumper bergerak ke kanan, dan jika menekan panah ke kiri maka jumper akan bergerak ke kiri. Player memiliki target untuk mencetak skor sebanyak-banyaknya. Setiap pijakan yang dilewati dan coin yang terambil, akan menambah skor player. Ketika jumper terjatuh (terjun bebas) atau menginjak pijakan jebakan, maka game akan berakhir.
  
<h2>Cara Menjalankan Kontainer : </h2>
  Untuk menjalankan kontainer, pertama clone repositori ini pada folder yang diinginkan. <br />
  Kemudian, pada file Makefile dapat diubah kode berikut sesuai direktori di mana file diclone <br />

  ```
  -v ~/Desktop/T-Jump-:/home/docker \
  ```

  Kode `~/Desktop/T-Jump-` dapat diubah menjadi file direktori yang diinginkan seperi `~/Documents:/home/docker \` <br />
  Setelah itu dapat dibuild images docker dengan menggunakan <br />
  ```
  make build-tjump
  ```
  Setelah build images selesai , images yang telah dibuild dapat dicek dengan menggunakan `docker images` dan setelah itu dapat dijalankan perintah <br />
  ```
  make run-test
  ```
  Dan apabila tidak terdapat error, maka pygame dapat dijalankan dengan perintah <br />
  ```
  python3 doodle.py
  ```
  
  <h4>Video Demo Kontainer</h4>
  [![Hands On 4](https://img.youtube.com/vi/54_COzEhGWM/0.jpg)](https://www.youtube.com/watch?v=54_COzEhGWM)
