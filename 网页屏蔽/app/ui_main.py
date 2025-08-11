import tkinter as tk
from tkinter import messagebox
from app.domain_manager import (
    load_domains, save_domains, add_domain, delete_domain, update_domain_status
)
from app.hosts_manager import rebuild_hosts_blocking

import sys

# —— 提示：macOS 上不要在这里强制提权，交给 hosts_manager 内部处理 ——


def refresh_listboxes():
    all_domains = load_domains()

    listbox_blocked.delete(0, tk.END)
    listbox_all.delete(0, tk.END)

    for d in all_domains:
        if d.get("blocked"):
            listbox_blocked.insert(tk.END, d["domain"])

        status_text = "[屏蔽中]" if d.get("blocked") else "[未屏蔽]"
        listbox_all.insert(tk.END, f'{d["domain"]} {status_text}')


def _apply_hosts_and_refresh(success_msg: str):
    try:
        rebuild_hosts_blocking()
        refresh_listboxes()
        status_label.config(text=f"状态：{success_msg}")
    except Exception as e:
        messagebox.showerror("操作失败", f"修改 hosts 失败：\n{e}")


def add_new_domain():
    new_domain = entry_domain.get().strip()
    if not new_domain:
        messagebox.showwarning("警告", "请输入有效的域名！")
        return

    if add_domain(new_domain):
        entry_domain.delete(0, tk.END)
        _apply_hosts_and_refresh(f"添加成功：{new_domain}")
    else:
        messagebox.showinfo("提示", "该域名已存在。")


def block_selected():
    sel = listbox_all.curselection()
    if not sel:
        messagebox.showwarning("警告", "请选择要屏蔽的域名！")
        return

    for idx in sel:
        domain_line = listbox_all.get(idx)
        domain_name = domain_line.split(" ")[0]
        update_domain_status(domain_name, True)

    _apply_hosts_and_refresh("屏蔽成功！")


def unblock_selected():
    sel = listbox_all.curselection()
    if not sel:
        messagebox.showwarning("警告", "请选择要解锁的域名！")
        return

    for idx in sel:
        domain_line = listbox_all.get(idx)
        domain_name = domain_line.split(" ")[0]
        update_domain_status(domain_name, False)

    _apply_hosts_and_refresh("解锁成功！")


def delete_selected():
    sel = listbox_all.curselection()
    if not sel:
        messagebox.showwarning("警告", "请选择要删除的域名！")
        return

    domains_to_delete = []
    for idx in sel:
        domain_line = listbox_all.get(idx)
        domain_name = domain_line.split(" ")[0]
        domains_to_delete.append(domain_name)

    if messagebox.askyesno("确认", f"确定要删除选中的 {len(domains_to_delete)} 个网站吗？"):
        for domain in domains_to_delete:
            delete_domain(domain)
        _apply_hosts_and_refresh("删除成功！")


# ===== GUI =====
root = tk.Tk()
root.title("网站屏蔽器 Blocker App (macOS)")
root.geometry("650x600")

title_label = tk.Label(root, text="网站屏蔽器 Blocker App", font=("Arial", 16))
title_label.pack(pady=10)

frame_listboxes = tk.Frame(root)
frame_listboxes.pack(pady=5)

# 左：已屏蔽
frame_blocked = tk.Frame(frame_listboxes, bg="#a3c6f1")
frame_blocked.pack(side=tk.LEFT, padx=10)

blocked_label = tk.Label(frame_blocked, text="已屏蔽网站列表", bg="#a3c6f1", font=("Arial", 12))
blocked_label.pack()

listbox_blocked = tk.Listbox(frame_blocked, selectmode=tk.BROWSE, width=35, height=15, bg="#d8e6f8")
listbox_blocked.pack()

# 右：全部
frame_all = tk.Frame(frame_listboxes, bg="#fff4c2")
frame_all.pack(side=tk.LEFT, padx=10)

all_label = tk.Label(frame_all, text="全部网站列表", bg="#fff4c2", font=("Arial", 12))
all_label.pack()

listbox_all = tk.Listbox(frame_all, selectmode=tk.MULTIPLE, width=35, height=15, bg="#fffbd7")
listbox_all.pack()

# 输入 + 按钮
entry_domain = tk.Entry(root, width=30)
entry_domain.pack(pady=5)

add_button = tk.Button(root, text="添加网站", command=add_new_domain)
add_button.pack(pady=5)

# 操作按钮
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

block_button = tk.Button(frame_buttons, text="屏蔽选中", width=12, command=block_selected)
block_button.pack(side=tk.LEFT, padx=5)

unblock_button = tk.Button(frame_buttons, text="解锁选中", width=12, command=unblock_selected)
unblock_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(frame_buttons, text="删除选中", width=12, command=delete_selected)
delete_button.pack(side=tk.LEFT, padx=5)

# 状态栏
status_label = tk.Label(root, text="状态：等待操作...", font=("Arial", 10))
status_label.pack(side=tk.BOTTOM, pady=10)

# 初始化
refresh_listboxes()
root.mainloop()
