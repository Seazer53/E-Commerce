Create Database ETicaret
Go
Use ETicaret
Go
Create Table Kullanicilar
(
	Id int identity,
	Adi varchar(50) not null,
	Soyadi varchar(50) not null,
	Adresi varchar(150) not null,
	DogumTarihi date,
	Telefon varchar(11) not null,
	Email varchar(75) not null,
	Sifre varchar(30) not null,
	Constraint PK_Kullanicilar_Id Primary Key (Id),
	Constraint CK_Kullanicilar_Telefon
	Check (Telefon Like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
)
Go
Create Table UrunTipleri
(
	Id int identity,
	Adi varchar(75) not null,
	Constraint PK_UrunTipleri_Id Primary Key (Id)
)
Go
Create Table Urunler
(
	Id int identity,
	UrunTipId int,
	Adi varchar(100) not null,
	Fiyati decimal,
	StokMiktari int,
	Constraint PK_Urunler_Id Primary Key (Id),
	Constraint FK_Urunler_UrunTipId Foreign Key (UrunTipId)
	References UrunTipleri(Id)
)
Go
Create Table Sepettekiler
(
	Id int identity,
	KullaniciId int,
	UrunId int,
	Constraint PK_Sepettekiler_Id Primary Key (Id),
	Constraint FK_Sepettekiler_KullaniciId Foreign Key (KullaniciId)
	References Kullanicilar(Id),
	Constraint FK_Sepettekiler_UrunTipId Foreign Key (UrunId)
	References Urunler(Id)
)
Go
Create Table AlinanUrunler
(
	Id int identity,
	KullaniciId int,
	UrunId int,
	Constraint PK_AlinanUrunler_Id Primary Key (Id),
	Constraint FK_AlinanUrunler_KullaniciId Foreign Key (KullaniciId)
	References Kullanicilar(Id),
	Constraint FK_AlinanUrunler_UrunId Foreign Key (UrunId)
	References Urunler(Id)
)
Go
Create Table Siparisler
(
	Id int identity,
	KullaniciId int,
	Tutar decimal,
	Constraint PK_Siparisler_Id Primary Key (Id),
	Constraint FK_Siparisler_KullaniciId Foreign Key (KullaniciId)
	References Kullanicilar(Id)
)
Go
Create Proc SP_KullaniciEkle
	@adi varchar(50),
	@soyadi varchar(50),
	@adresi varchar(150),
	@dogumtarihi date,
	@telefon varchar(11),
	@email varchar(75),
	@sifre varchar(30)
As
Begin
	Insert Into Kullanicilar(Adi, Soyadi, Adresi, DogumTarihi, Telefon, Email, Sifre)
	Values (@adi, @soyadi, @adresi, @dogumtarihi, @telefon, @email, @sifre)
End
Go
Create Proc SP_UrunTipiEkle
	@adi varchar(75)
As
Begin
	Insert Into UrunTipleri(Adi)
	Values (@adi)
End
Go
Create Proc SP_UrunEkle
	@uruntipid int,
	@adi varchar(100),
	@fiyati decimal,
	@stokmiktari int
As
Begin
	Insert Into Urunler(UrunTipId, Adi, Fiyati, StokMiktari)
	Values (@uruntipid, @adi, @fiyati, @stokmiktari)
End
Go
Create Proc SP_SepeteEkle
	@kullaniciid int,
	@urunid int

As
Begin
	Insert Into Sepettekiler(KullaniciId,UrunId)
	Values (@kullaniciid,@urunid)
End
Go
Create Proc SP_SiparisEkle
	@kullaniciid int,
	@tutar decimal
As
Begin
	Insert Into Siparisler(KullaniciId, Tutar)
	Values (@kullaniciid, @tutar)
End
Go
Create Proc SP_KullaniciGuncelle
	@id int,
	@adi varchar(50),
	@soyadi varchar(50),
	@adresi varchar(150),
	@dogumtarihi date,
	@telefon varchar(11),
	@email varchar(75),
	@sifre varchar(30)
As
Begin
	Update Kullanicilar
	Set Adi = @adi,
		Soyadi = @soyadi,
		Adresi = @adresi,
		DogumTarihi = @dogumtarihi,
		Telefon = @telefon,
		Email = @email,
		Sifre = @sifre
		Where Id = @id
End
Go
Create Proc SP_SiparisGuncelle
	@id int,
	@kullaniciid int,
	@tutar decimal
As
Begin
	Update Siparisler
	Set KullaniciId = @kullaniciid,
		Tutar = @tutar
		Where Id = @id
End
Go
Create Proc SP_UrunGuncelle
	@id int,
	@uruntipid int,
	@adi varchar(100),
	@fiyati decimal,
	@stokmiktari int
As
Begin
	Update Urunler
	Set UrunTipId = @uruntipid,
		Adi = @adi,
		Fiyati = @fiyati,
		StokMiktari = @stokmiktari
		Where Id = @id
End
Go
Create Proc SP_SepetGuncelle
	@id int,
	@kullaniciid int,
	@urunid int
As
Begin
	Update Sepettekiler
	Set KullaniciId = @kullaniciid,
		UrunId = @urunid
		Where Id = @id
End
Go
Create Proc SP_UrunTipiGuncelle
	@id int,
	@adi varchar(75)
As
Begin
	Update UrunTipleri
	Set Adi = @adi
		Where Id = @id
End
Go
Create Proc SP_KullaniciSil
	@id int
As
Begin
Delete From Kullanicilar Where Id = @id
End
Go
Create Proc SP_SiparisSil
	@id int
As
Begin
Delete From Siparisler Where Id = @id
End
Go
Create Proc SP_UrunSil
	@id int
As
Begin
Delete From Urunler Where Id = @id
End
Go
Create Proc SP_SepetSil
	@id int
As
Begin
Delete From Sepettekiler Where Id = @id
End
Go
Create Proc SP_UrunTipiSil
	@id int
As
Begin
Delete From UrunTipleri Where Id = @id
End
Go