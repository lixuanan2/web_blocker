import json

DOMAIN_LIST_FILE = "../data/domain_list.json"

# 读取网站列表
def load_domains():
    try:
        with open(DOMAIN_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 保存网站列表
def save_domains(domains):
    with open(DOMAIN_LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(domains, f, indent=4)

# 添加新网站
def add_domain(new_domain):
    domains = load_domains()
    if not any(d["domain"] == new_domain for d in domains):
        domains.append({"domain": new_domain, "blocked": False})
        save_domains(domains)
        return True
    else:
        return False  # 已存在

# 删除网站
def delete_domain(target_domain):
    domains = load_domains()
    domains = [d for d in domains if d["domain"] != target_domain]
    save_domains(domains)

# 更新网站屏蔽状态
def update_domain_status(target_domain, blocked):
    domains = load_domains()
    for d in domains:
        if d["domain"] == target_domain:
            d["blocked"] = blocked
    save_domains(domains)
