from pathlib import Path
import subprocess
from app.domain_manager import load_domains

HOSTS = Path("/etc/hosts")
BEGIN = "# >>> BLOCKER BEGIN >>>"
END   = "# <<< BLOCKER END <<<"

def _run_with_admin(cmd: str):
    """
    用 AppleScript 弹系统密码框，以管理员权限执行 shell 命令。
    """
    # 先把命令里的反斜杠和双引号安全转义
    safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
    osa = [
        "osascript", "-e",
        f'do shell script "{safe_cmd}" with administrator privileges'
    ]
    subprocess.run(osa, check=True)


def _build_block_lines():
    """
    读取 blocked=True 的域名，生成 /etc/hosts 规则：
    - 对裸域（youtube.com）或带 www 的域名（www.youtube.com）：
      生成两条：youtube.com、www.youtube.com
    - 对非 www 的明确子域（如 m.youtube.com）：
      只生成该子域本身，不额外加 www.m.youtube.com
    """
    domains = load_domains()
    lines = []
    seen = set()

    for item in domains:
        if not item.get("blocked"):
            continue

        d = (item.get("domain") or "").strip().lstrip(".").lower()
        if not d:
            continue

        # 归一化：移除前导 www.
        if d.startswith("www."):
            base = d[4:]
        else:
            base = d

        # 判断是否是“非 www 的明确子域”（例如 m.youtube.com）
        is_subdomain = base.count(".") >= 2 and not d.startswith("www.")

        if is_subdomain:
            candidates = [base]  # 只拦这个子域
        else:
            candidates = [base, f"www.{base}"]  # 裸域 + www

        for host in candidates:
            rule = f"0.0.0.0 {host}"
            if host and rule not in seen:
                lines.append(rule)
                seen.add(rule)

    return lines


def _merge_hosts(text: str, block_lines):
    """
    用 BEGIN/END 包装的“屏蔽块”覆盖旧块，返回新文本。
    """
    out, in_block = [], False
    for line in text.splitlines():
        s = line.strip()
        if s == BEGIN: in_block = True;  continue
        if s == END:   in_block = False; continue
        if not in_block: out.append(line)
    out.append(BEGIN)
    out += block_lines
    out.append(END)
    return "\n".join(out).rstrip() + "\n"

def rebuild_hosts_blocking():
    """
    读取当前被标记为 blocked 的域名 -> 写入 /etc/hosts 屏蔽块 -> 刷新 DNS。
    失败会抛异常，UI 会捕获并弹窗。
    """
    orig = HOSTS.read_text(encoding="utf-8")
    new  = _merge_hosts(orig, _build_block_lines())
    if new == orig:
        return  # 没变化就不动

    tmp = Path("/tmp/hosts.blocker.tmp")
    bak = Path("/tmp/hosts.blocker.bak")
    bak.write_text(orig, encoding="utf-8")
    tmp.write_text(new,  encoding="utf-8")

    # 覆盖 hosts 并刷新 DNS（两步）
    cmd = (
        f"/bin/cp {tmp} {HOSTS} && "
        "/usr/bin/dscacheutil -flushcache && "
        "/usr/bin/killall -HUP mDNSResponder || true"
    )
    _run_with_admin(cmd)
    tmp.unlink(missing_ok=True)
