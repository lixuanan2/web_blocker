import json
from pathlib import Path

# 绝对路径：…/项目根/data/domain_list.json
DATA_FILE = (Path(__file__).resolve().parent.parent / "data" / "domain_list.json")

def _ensure_data_file():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

# 读取网站列表
def load_domains():
    try:
        _ensure_data_file()
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # 文件损坏时回退为空数组
        return []

# 保存网站列表
def save_domains(domains):
    _ensure_data_file()
    DATA_FILE.write_text(json.dumps(domains, indent=4, ensure_ascii=False), encoding="utf-8")

# 添加新网站
def add_domain(new_domain: str) -> bool:
    new_domain = (new_domain or "").strip()
    if not new_domain:
        return False
    domains = load_domains()
    if any(d.get("domain") == new_domain for d in domains):
        return False
    domains.append({"domain": new_domain, "blocked": False})
    save_domains(domains)
    return True

# 删除网站
def delete_domain(target_domain: str):
    domains = load_domains()
    domains = [d for d in domains if d.get("domain") != target_domain]
    save_domains(domains)

# 更新网站屏蔽状态
def update_domain_status(target_domain: str, blocked: bool):
    domains = load_domains()
    for d in domains:
        if d.get("domain") == target_domain:
            d["blocked"] = bool(blocked)
    save_domains(domains)
