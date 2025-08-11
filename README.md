# Blocker App

## 简介

Blocker App 是一个小巧简洁的自制应用，诞生于课余时间娱乐开发，  
主要用于屏蔽一些特定的网站域名，帮助提升自律和专注力。  

目前已支持 **macOS** 和 **Windows** 两个版本，  
功能基础但足够实用，并支持在 GitHub 分支中进行版本控制。  

---

## 项目结构

```plaintext
web_blocker/
├── app/
│   ├── __init__.py
│   ├── ui_main.py            # 主界面程序（GUI）
│   ├── hosts_manager.py      # hosts 文件管理
│   ├── domain_manager.py     # 域名清单管理
├── data/
│   ├── domain_list.json       # 网站清单数据
│   ├── hosts_backup.txt       # hosts 文件备份（首次运行自动生成）
├── dist/                      # 打包后的可执行程序（按平台区分）
├── build/                     # 打包临时文件（可忽略）
├── main.py                    # 控制台版本（命令行界面）
├── README.md                  # 项目说明文件
```

---

## 分支说明（版本控制）

- **main** 分支：公共代码与文档，不依赖具体平台。  
- **windows** 分支：Windows 平台适配版（.exe 可执行程序）  
- **macos** 分支：macOS 平台适配版（.app 应用程序）  

这样可以在不同分支独立维护平台差异代码，而不影响主分支。  

切换方法：
```bash
# 切换到 macOS 版本
git checkout macos

# 切换到 Windows 版本
git checkout windows
```

---

## 运行方式

### 直接运行打包版本（推荐）

#### Windows
- 运行 `dist/BlockerApp.exe`
- 双击即可使用，无需安装 Python 环境。

#### macOS
- 运行 `dist/BlockerApp.app`
- 第一次运行需通过系统安全验证（右键 → 打开）。
- 自动请求管理员权限以修改 `/etc/hosts`。

> ⚠️ **注意**：程序启动时会自动备份原始 hosts 文件到 `data/hosts_backup.txt`。

---

### 从源码运行

1. 克隆项目
```bash
git clone https://github.com/yourname/web_blocker.git
cd web_blocker
```

2. 创建虚拟环境并安装依赖
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. 启动
```bash
python -m app.ui_main
```

---

## 工作原理

- 程序通过修改系统 `hosts` 文件，将目标域名指向 `0.0.0.0`（黑洞地址）  
  从而在本机屏蔽这些网站。
- 修改 `hosts` 文件需要管理员权限，这是操作系统的安全要求。
- 首次运行会自动备份原始 `hosts` 文件，确保可以恢复。

---

## 当前版本

- **版本号**：v0
- **特性**：
  - 支持 macOS 与 Windows。
  - 域名添加、删除、屏蔽、解锁。
  - 自动备份 hosts 文件，防止误操作。

---

## 后续计划

- 添加时间段自动屏蔽。
- 批量导入/导出域名列表。
- 增加应用图标与版本信息。
- 发布 v1.0 正式版。

---

## 打包方法

### macOS
```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --windowed --name "BlockerApp" app/ui_main.py
```
生成的 `.app` 文件位于 `dist/BlockerApp.app`。

### Windows
```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name "BlockerApp" app/ui_main.py
```
生成的 `.exe` 文件位于 `dist/BlockerApp.exe`。

---

## 特别感谢

感谢大家使用与支持！  
本项目主要是自用，也希望能帮到同样需要的朋友。🎯
