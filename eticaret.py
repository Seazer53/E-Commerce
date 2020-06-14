from flask import Flask, redirect, url_for, request, render_template, session
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = "Çok gizli"
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-5L8Q4TP;'
                      'Database=ETicaret;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

noCount = """
SET NOCOUNT ON;
"""


@app.route('/', methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route('/kayit', methods=["GET", "POST"])
def kayit():
    return render_template("kayit.html")


@app.route('/hesapolustur', methods=["GET", "POST"])
def hesapolustur():
    adi = request.form["ad"]
    soyadi = request.form["soyad"]
    adresi = request.form["adres"]
    dogumtarihi = request.form["dogumtarihi"]
    telefon = request.form["telefon"]
    email = request.form["email"]
    email2 = request.form["email2"]
    sifre = request.form["sifre"]
    sifre2 = request.form["sifre2"]
    hata_var = False

    if email != email2:
        hata_var = True
        hata = "Email adresleriniz uyuşmuyor!"
        return render_template("kayit.html", hata_var=hata_var, hata=hata)

    elif sifre != sifre2:
        hata_var = True
        hata = "Şifreleriniz uyuşmuyor!"
        return render_template("kayit.html", hata_var=hata_var, hata=hata)

    else:
        sqlExecSP = "{call SP_KullaniciEkle (?, ?, ?, ?, ?, ?, ?)}"
        cursor.execute(sqlExecSP, adi, soyadi, adresi, dogumtarihi, telefon, email, sifre)
        conn.commit()
        hata_var = False
        mesaj = "Hesabınız başarıyla oluşturuldu! Lütfen giriş yapın!"

        return render_template("login.html", hata_var=hata_var, mesaj=mesaj)


@app.route('/kontrol', methods=["GET", "POST"])
def kontrol():
    email = request.form["email"]
    sifre = request.form["sifre"]
    basarili = False

    kullanicilar = cursor.execute("Select * From Kullanicilar")

    for x in kullanicilar:
        if x[-2] == email and x[-1] == sifre:
            basarili = True

        session['isim'] = x[1] + " " + x[2]

    if basarili is False:
        hatamesaji = "Kullanıcı adı ya da şifre hatalı!"

        return render_template("login.html", hatamesaji=hatamesaji, basarili=basarili)

    else:
        return redirect(url_for('anasayfa'))


@app.route('/anasayfa', methods=["GET", "POST"])
def anasayfa():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    return render_template("anasayfa.html", giris_yapildi=giris_yapildi)


@app.route('/cikisyap', methods=["GET", "POST"])
def cikisyap():
    cikis_yapildi = True
    kullanici = session['isim']
    veda = kullanici + " başarıyla çıkış yaptınız!"

    if 'isim' in session:
        session.pop('isim', None)

    return render_template("login.html", cikis_yapildi=cikis_yapildi, veda=veda)


@app.route('/sepetim', methods=["GET", "POST"])
def sepet():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    if giris_yapildi is False:
        return redirect(url_for("login"))

    else:
        urunler = []
        toplam = 0

        sepet = cursor.execute("Select * From Sepettekiler")

        for x in sepet:
            urunler.append(x[-1])

        if request.method == 'POST':
            urunidstr = request.form["urunid"]
            urunid = int(urunidstr)

            kullanicilar = cursor.execute("Select * From Kullanicilar")

            for x in kullanicilar:
                if session["isim"] == x[1] + " " + x[2]:
                    kullaniciid = x[0]

            sqlExecSP = "{call SP_SepeteEkle (?, ?)}"
            cursor.execute(sqlExecSP, kullaniciid, urunidstr)
            conn.commit()

            urunler.append(urunid)

        urunlistesi = cursor.execute("Select * From Urunler")

        for y in urunlistesi:
            for a in urunler:
                if y[0] == a:
                    toplam += y[-2]

        return render_template("sepet.html", urunler=urunler, toplam=toplam)


@app.route('/sepetguncelle', methods=["GET", "POST"])
def sepetguncelle():
    urunid = request.form["urunid"]
    kullanicilar = cursor.execute("Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            kullaniciid = x[0]

    sepet = cursor.execute("Select * From Sepettekiler")

    for y in sepet:
        if int(urunid) == y[2] and int(kullaniciid) == y[1]:
            id = y[0]

    cursor.execute("""Delete From Sepettekiler Where Id = ?""", id)
    conn.commit()

    return redirect(url_for('anasayfa'))


@app.route('/bilgisayar', methods=["GET", "POST"])
def bilgisayarlistele():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    return render_template("bilgisayar.html", giris_yapildi=giris_yapildi)


@app.route('/kitap', methods=["GET", "POST"])
def kitaplistele():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    return render_template("kitap.html", giris_yapildi=giris_yapildi)


@app.route('/akillitelefon', methods=["GET", "POST"])
def telefonlistele():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    return render_template("akillitelefon.html", giris_yapildi=giris_yapildi)


@app.route('/arama', methods=["GET", "POST"])
def arama():
    if 'isim' in session:
        giris_yapildi = True
    else:
        giris_yapildi = False

    aranan = request.form["arama"]
    bulunanlar = {}
    urunlistesi = cursor.execute("Select * From Urunler")

    for x in urunlistesi:
        if aranan in x[2]:
            bulunanlar[x[0]] = [x[2], x[-2]]

    return render_template("aramasonucu.html", bulunanlar=bulunanlar, giris_yapildi=giris_yapildi)


@app.route('/satinal', methods=["GET", "POST"])
def satinal():
    sepettekiler = []
    fiyat = 0
    sepet = cursor.execute("Select * From Sepettekiler")

    for x in sepet:
        sepettekiler.append(x[-1])

    urunler = cursor.execute("Select * From Urunler")

    for urun in urunler:
        for x in sepettekiler:
            if x == urun[0]:
                fiyat += urun[-2]

    return render_template("satinal.html", fiyat=fiyat)


@app.route('/odeme', methods=["GET", "POST"])
def odeme():
    mesaj = ""
    fiyat = 0

    sepettekiler = cursor.execute(noCount + " Select * From Sepettekiler")
    urunler = cursor.execute(noCount + " Select * From Urunler")

    for urun in urunler:
        for x in sepettekiler:
            if x[-1] == urun[0]:
                adet = urun[-1] - 1

                cursor.execute(noCount + """ Update Urunler Set UrunTipId = ?, Adi = ?, Fiyati = ?, StokMiktari = ? Where Id = ?""",
                urun[1], urun[2], urun[-2], adet, urun[0])
                conn.commit()

    sepet = cursor.execute("Select * From Sepettekiler")
    alisveris_sepeti = []

    for x in sepet:
        alisveris_sepeti.append(x[-1])

    dburunler = cursor.execute("Select * From Urunler")

    for urun in dburunler:
        for x in alisveris_sepeti:
            if x == urun[0]:
                fiyat += urun[-2]

    kullanicilar = cursor.execute(noCount + " Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]

    for i in alisveris_sepeti:
        cursor.execute(noCount + " Insert Into AlinanUrunler(KullaniciId, UrunId) Values (?, ?)", id, i)
        conn.commit()

    cursor.execute(noCount + " Insert Into Siparisler(KullaniciId, Tutar) Values (?, ?)", id, fiyat)
    conn.commit()

    mesaj += "Siparişiniz başarıyla alındı!"

    cursor.execute(noCount + """ Delete From Sepettekiler""")
    conn.commit()

    return render_template("siparis.html", mesaj=mesaj)


@app.route('/hesabim', methods=["GET", "POST"])
def hesabim():
    kullanicilar = cursor.execute(noCount + " Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            adsoyad = x[1] + " " + x[2]
            adres = x[3]
            dogumtarihi = x[4]
            telefon = x[5]
            email = x[6]

    return render_template("hesap.html", adsoyad=adsoyad, adres=adres, dogumtarihi=dogumtarihi, telefon=telefon, email=email)


@app.route('/hesapgoruntule', methods=["GET", "POST"])
def hesapgoruntule():
    kullanicilar = cursor.execute(noCount + " Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]
            ad = x[1]
            soyad = x[2]
            adres = x[3]
            dogumtarihi = x[4]
            telefon = x[5]
            email = x[6]

    return render_template("hesapgoruntule.html", ad=ad, soyad=soyad, adres=adres, dogumtarihi=dogumtarihi, telefon=telefon, email=email)


@app.route('/hesapguncelle', methods=["GET", "POST"])
def hesapguncelle():
    hesapguncellendi = True
    adi = request.form["ad"]
    soyadi = request.form["soyad"]
    adresi = request.form["adres"]
    dogumtarihi = request.form["dogumtarihi"]
    telefon = request.form["telefon"]
    email = request.form["email"]

    kullanicilar = cursor.execute(noCount + " Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]
            sifre = x[-1]

    cursor.execute(noCount + """ Update Kullanicilar Set Adi = ?, Soyadi = ?, Adresi = ?, DogumTarihi = ?, Telefon = ?, Email = ?, 
    Sifre = ? Where Id = ?""", adi, soyadi, adresi, dogumtarihi, telefon, email, sifre, id)
    conn.commit()

    bilgi = "Hesap bilgileriniz başarıyla güncellendi. Lütfen tekrar giriş yapın!"

    if 'isim' in session:
        session.pop('isim', None)

    return render_template("login.html", bilgi=bilgi, hesapguncellendi=hesapguncellendi)


@app.route('/sifredegistir', methods=["GET", "POST"])
def sifredegistir():
    hata_var = False
    hata = ""

    return render_template("sifre.html", hata_var=hata_var, hata=hata)


@app.route('/sifreguncelle', methods=["GET", "POST"])
def sifreguncelle():
    hesapguncellendi = True
    hata_var = False
    hata = ""
    mevcut_sifre = request.form["mevcutsifre"]
    yeni_sifre = request.form["yenisifre"]
    yeni_sifre2 = request.form["yenisifre2"]

    kullanicilar = cursor.execute(noCount + " Select * From Kullanicilar")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]
            adi = x[1]
            soyadi = x[2]
            adresi = x[3]
            dogumtarihi = x[4]
            telefon = x[5]
            email = x[6]
            sifre = x[-1]

    if mevcut_sifre != sifre:
        hata_var = True
        hata = "Mevcut şifrenizi yanlış girdiniz!"

        return render_template("sifre.html", hata_var=hata_var, hata=hata)

    elif yeni_sifre != yeni_sifre2:
        hata_var = True
        hata = "Yeni şifreler eşleşmiyor!"

        return render_template("sifre.html", hata_var=hata_var, hata=hata)

    elif mevcut_sifre == yeni_sifre:
        hata_var = True
        hata = "Yeni şifre mevut şifre ile aynı!"

        return render_template("sifre.html", hata_var=hata_var, hata=hata)

    cursor.execute(noCount + """ Update Kullanicilar Set Adi = ?, Soyadi = ?, Adresi = ?, DogumTarihi = ?, 
    Telefon = ?, Email = ?, Sifre = ? Where Id = ?""", adi, soyadi, adresi, dogumtarihi, telefon, email, yeni_sifre, id)
    conn.commit()

    bilgi = "Şifreniz başarıyla güncellendi! Lütfen tekrar giriş yapın!"

    if 'isim' in session:
        session.pop('isim', None)

    return render_template("login.html", bilgi=bilgi, hesapguncellendi=hesapguncellendi)


@app.route('/siparislerim', methods=["GET", "POST"])
def siparisgoruntule():
    siparis_var = False
    kullanicilar = cursor.execute(noCount + """ Select * From Kullanicilar""")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]

    alinanurunler = cursor.execute(noCount + """ Select * From AlinanUrunler""")
    urunidleri = []

    for i in alinanurunler:
        if i[1] == id:
            urunidleri.append(i[-1])

    urunler = cursor.execute(noCount + """ Select * From Urunler""")
    bulunanlar = {}

    for y in urunler:
        for x in urunidleri:
            if x == y[0]:
                bulunanlar[y[0]] = [y[2], y[-2]]

    if len(bulunanlar) > 0:
        siparis_var = True

    return render_template("siparisgoruntule.html", bulunanlar=bulunanlar, siparis_var=siparis_var)


@app.route('/siparisiptal', methods=["GET", "POST"])
def siparisiptal():
    urunid = request.form["urunid"]

    kullanicilar = cursor.execute(noCount + """ Select * From Kullanicilar""")

    for x in kullanicilar:
        if session["isim"] == x[1] + " " + x[2]:
            id = x[0]

    cursor.execute(noCount + """ Delete From AlinanUrunler Where KullaniciId = ? AND UrunId = ?""", id, urunid)
    conn.commit()

    alinanurunler = cursor.execute(noCount + """ Select * From AlinanUrunler""")
    urunidleri = []

    for i in alinanurunler:
        if i[1] == id:
            urunidleri.append(i[-1])

    urunler = cursor.execute(noCount + """ Select * From Urunler""")
    fiyat = 0

    for y in urunler:
        for x in urunidleri:
            if x == y[0]:
                fiyat += y[-2]

    cursor.execute(noCount + """ Update Siparisler Set KullaniciId = ?, Tutar = ? Where KullaniciId = ?""", id, fiyat, id)
    conn.commit()

    return redirect(url_for("siparisgoruntule"))


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
