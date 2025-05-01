import os
import shutil
from app.domain_manager import load_domains

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
# BACKUP_FILE = "hosts_backup.txt" 改成下面👇
BACKUP_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'hosts_backup.txt'))
START_MARK = "# --- Blocker App Start ---\n"
END_MARK = "# --- Blocker App End ---\n"

# 备份 hosts 文件（第一次执行）
def backup_hosts():
    if not os.path.exists(BACKUP_FILE):
        shutil.copy(HOSTS_PATH, BACKUP_FILE)
        print("[√] Hosts 文件已备份。")

# 读取 hosts 文件
def read_hosts():
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        return f.readlines()

# 写入 hosts 文件
def write_hosts(lines):
    with open(HOSTS_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 根据当前 blocked 状态重新生成标记区
def rebuild_hosts_blocking():
    lines = read_hosts()

    # 先移除原有的标记区
    new_lines = []
    inside_mark = False
    for line in lines:
        if line == START_MARK:
            inside_mark = True
        if not inside_mark:
            new_lines.append(line)
        if line == END_MARK:
            inside_mark = False

    # 加上新的标记区（根据 blocked:true 的域名）
    domains = load_domains()
    blocked_domains = [d["domain"] for d in domains if d["blocked"]]

    if blocked_domains:
        new_lines.append(START_MARK)
        for domain in blocked_domains:
            new_lines.append(f"127.0.0.1 {domain}\n")
        new_lines.append(END_MARK)

    # 写回 hosts 文件
    write_hosts(new_lines)
    print("[√] hosts 文件已同步。")

