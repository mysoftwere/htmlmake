# 🌐 HTML Make Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-informational?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Excel](https://img.shields.io/badge/Excel-Input%20Support-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

**Excel থেকে স্বয়ংক্রিয়ভাবে সুন্দর HTML ফাইল তৈরি করার সফটওয়্যার**

</div>

---

## 📖 বিবরণ (Description)

**HTML Make Generator** একটি Python-ভিত্তিক Desktop সফটওয়্যার যা Excel ফাইল থেকে ডেটা পড়ে স্বয়ংক্রিয়ভাবে একাধিক HTML ফাইল তৈরি করে। প্রতিটি HTML ফাইলে Title, Meta Tags, Script Link এবং Custom Image সঠিকভাবে ইনজেক্ট হয়।

> **HTML Make Generator** is a Python-based Desktop GUI software that reads data from an Excel file and automatically generates multiple customized HTML files — each with injected titles, meta tags, script links, and images.

---

## ✨ বৈশিষ্ট্যসমূহ (Features)

- 📊 **Excel Input** — `.xlsx` ফাইল থেকে সরাসরি ডেটা পড়ে
- 🏷️ **Auto Title Injection** — Title, Meta Tags, JSON-LD Schema সব জায়গায় স্বয়ংক্রিয়ভাবে আপডেট হয়
- 🔗 **Script Link Support** — Column C তে কাস্টম Script URL দেওয়া যায়
- 🖼️ **Image Support** — URL বা Local Image ফাইল সাপোর্ট করে (Base64 Embed)
- 📁 **Slug Filename** — Title থেকে SEO-friendly ফাইলনাম তৈরি হয়
- 📅 **Auto Date Update** — আজকের তারিখ সব জায়গায় স্বয়ংক্রিয়ভাবে বসে
- 🖥️ **Dark UI Log Console** — Real-time Colored Log দেখা যায়
- ⏸️ **Start / Stop Control** — প্রক্রিয়া যেকোনো সময় বন্ধ করা যায়
- ⚡ **Multi-threaded** — UI ফ্রিজ হয় না, Background-এ কাজ করে

---

## 📂 Excel ফাইল স্ট্রাকচার

| Column A | Column B | Column C | Column D |
|----------|----------|----------|----------|
| **Title** (Required) | Body/Content | Script Link (Optional) | Image URL/Path (Optional) |

> **Column A** অবশ্যই পূরণ করতে হবে। Column C খালি থাকলে Default Script Link ব্যবহার হয়।

---

## 🚀 ইনস্টলেশন ও চালানো (Installation & Usage)

### Prerequisites

```bash
pip install openpyxl
```

> Python 3.8 বা তার উপরের ভার্সন প্রয়োজন।

### চালানোর পদ্ধতি

**Option 1: Double-click (সহজ পদ্ধতি)**
```
Run HTML Make.bat  ← এটি Double-click করুন
```

**Option 2: Terminal দিয়ে**
```bash
python "HTML Make.py"
```

---

## 🖥️ Software ব্যবহার পদ্ধতি

1. সফটওয়্যার চালু করুন
2. **Excel File** সিলেক্ট করুন (`.xlsx` ফরম্যাট)
3. **Output Folder** সিলেক্ট করুন যেখানে HTML ফাইল সেভ হবে
4. **"Start HTML Make"** বাটনে ক্লিক করুন
5. নিচের Log Console-এ Real-time অগ্রগতি দেখুন
6. সম্পন্ন হলে Output ফোল্ডারে HTML ফাইলগুলো পাবেন

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
HTML Make/
│
├── HTML Make.py           # মূল সফটওয়্যার (Main Application)
├── template.html          # HTML Template ফাইল
├── HTML MAKE.xlsx         # Excel Input ফাইল (নমুনা)
├── Run HTML Make.bat      # Windows-এ চালানোর Shortcut
├── config.json            # সেটিংস সংরক্ষণ ফাইল (Auto-generated)
│
├── Output/                # Generated HTML ফাইলগুলো এখানে আসে
│
├── inspect_form.py        # ডেভেলপমেন্ট টুল
├── test_junior.py         # টেস্ট স্ক্রিপ্ট
└── test_pacific.py        # টেস্ট স্ক্রিপ্ট
```

---

## ⚙️ Configuration

সফটওয়্যার স্বয়ংক্রিয়ভাবে `config.json` ফাইলে পাথ সংরক্ষণ করে:

```json
{
  "excel_path": "path/to/HTML MAKE.xlsx",
  "output_dir": "path/to/Output"
}
```

---

## 🛠️ টেকনোলজি (Tech Stack)

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core Language |
| Tkinter | Desktop GUI |
| openpyxl | Excel File Reading |
| re (regex) | HTML Template Manipulation |
| base64 | Local Image Embedding |
| threading | Background Processing |

---

## 📋 Requirements

```
python >= 3.8
openpyxl >= 3.0.0
tkinter (built-in with Python)
```

---

## 🤝 কন্ট্রিবিউশন (Contributing)

1. এই repo-টি Fork করুন
2. নতুন Feature Branch তৈরি করুন (`git checkout -b feature/AmazingFeature`)
3. আপনার পরিবর্তন Commit করুন (`git commit -m 'Add some AmazingFeature'`)
4. Branch-এ Push করুন (`git push origin feature/AmazingFeature`)
5. Pull Request খুলুন

---

## 📄 লাইসেন্স (License)

এই প্রজেক্টটি [MIT License](LICENSE) এর অধীনে প্রকাশিত।

---

## 👨‍💻 ডেভেলপার (Developer)

**Mizan YT**

<div align="center">

⭐ যদি এই সফটওয়্যার আপনার কাজে লাগে, তাহলে একটি Star দিতে ভুলবেন না!

</div>
