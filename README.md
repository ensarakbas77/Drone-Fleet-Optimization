# 🚁 Drone Filo Optimizasyonu <br>

Bu proje, Yazılım Geliştirme Lab II dersi kapsamında geliştirilmiştir. Amaç, çoklu drone filosunun kısıtlı ortamlarda optimum teslimat rotası oluşturmasını sağlayan algoritmalar geliştirmektir. <br> <br>

## 🚀 Proje Özellikleri <br>

- 📦 Teslimat noktalarını ve drone özelliklerini baz alan dinamik rota planlaması <br>
- ❌ Uçuşa yasak bölgeleri tanıma ve zaman pencerelerine göre değerlendirme <br>
- 📈 A* algoritması ile rota bulma <br>
- 🔒 CSP (Constraint Satisfaction Problem) ile kısıt yönetimi <br>
- 🧬 Genetik algoritma ile çoklu drone optimizasyonu <br>
- 📊 Matplotlib ile rota görselleştirmesi <br> 
- 🧪 2 sabit senaryo + rastgele senaryo üretici <br> <br>

## 📁 Proje Yapısı <br>
├── data/ --> Senaryo veri dosyaları (.txt) <br>
├── project/ --> Algoritmalar (A*, GA, CSP, graf yapısı) <br>
├── tools/ --> Senaryo üretici ve demo çalıştırıcı <br>
├── utils/ --> Yardımcı fonksiyonlar (veri yükleme, görselleştirme) <br>
├── main.py --> Projeyi çalıştıran ana dosya  <br>
├── .gitignore <br>
└── README.md <br> <br>


## ⚙️ Kurulum <br>

1. Depoyu klonlayın: <br>
`git clone https://github.com/ensarakbas77/Drone-Fleet-Optimization.git` <br>
`cd Drone-Fleet-Optimization`

2. Gerekli Python kütüphanelerini yükleyin: <br>
`pip install matplotlib` <br>

3. Çalıştırma <br>
`python main.py`
