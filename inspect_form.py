import requests
from bs4 import BeautifulSoup

url = "https://www.pacificcouncil.org/junior-fellowship-application"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

for i, form in enumerate(soup.find_all("form")):
    form_id = form.get("id")
    action = form.get("action")
    print(f"\n================ FORM {i+1}: ID={form_id}, ACTION={action} ================")
    for el in form.find_all(["input", "select", "textarea"]):
        tag = el.name
        eid = el.get("id")
        name = el.get("name")
        etype = el.get("type", "")
        eclass = " ".join(el.get("class", []))
        req = el.get("required")
        val = el.get("value", "")
        lbl = ""
        if eid:
            label_el = soup.find("label", {"for": eid})
            if label_el:
                lbl = label_el.get_text(strip=True)
        print(f"[{tag}] id='{eid}' name='{name}' type='{etype}' required={req} label='{lbl}'")
