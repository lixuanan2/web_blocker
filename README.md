# Blocker App

## 简介

Blocker App 是一个小巧简洁的自制应用，诞生于课余时间娱乐开发，  
主要用于屏蔽一些特定的网站域名，帮助我提升自律和专注力。  
目前是第一个公开版本，功能基础，但足够实用！

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
├── dist/
│   └── BlockerApp.exe         # 打包后的可执行程序
├── build/                     # 打包临时文件（可忽略）
├── main.py                    # 控制台版本（命令行界面）
├── README.md                  # 项目说明文件
```

---

## 运行方式

- 推荐直接运行 `dist/BlockerApp.exe`。
- 无需安装任何环境，双击即可使用。
- 程序会在启动时**自动请求管理员权限**，因为需要修改系统的 `hosts` 文件。
- 第一次运行时，会自动备份原始的 hosts 文件到 `data/hosts_backup.txt`，保障安全。

---

## 工作原理

- 本程序通过修改系统 `hosts` 文件，将特定网站的域名重定向到 `127.0.0.1` 本地地址，  
  从而达到在本机屏蔽访问指定网站的效果。
- 需要管理员权限写入 `hosts` 文件，这是操作系统安全要求。

---

## 当前版本

- **版本号**：v0
- **特性**：
  - 简单的域名添加、删除、屏蔽、解锁功能。
  - 直观的图形界面，方便操作。
  - 自动备份原有 hosts 文件，保障系统安全。

---

## 后续计划

- 持续完善功能，比如：
  - 添加时间段自动屏蔽
  - 批量导入/导出域名
  - 更丰富的界面体验
- 优化打包，增加程序图标和版本描述信息。
- 发布正式版 v1.0。

---

## 特别感谢

感谢大家使用与支持！  
本项目主要是为了自用，也希望能给有同样需要的朋友带来一点帮助。🎯

---

## 其他说明

如果需要，可以为 `dist/BlockerApp.exe` 创建一个快捷方式，  
方便将程序固定到桌面或任务栏，一键启动。

【快捷方式创建方法】：
- 找到 `dist/BlockerApp.exe`
- 右键 → 发送到 → 桌面快捷方式
- 也可以拖动到任务栏固定

---

## 打包方法

如果需要重新打包 Blocker App，可按照以下步骤进行：

1. 确保已安装 PyInstaller。

```bash
pip install pyinstaller
```

2. 清理旧的打包文件（可选，但推荐）。

```bash
rmdir /s /q build dist
del *.spec
```

3. 在项目根目录下，运行打包命令：

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "BlockerApp" app/ui_main.py
```

- `--onefile`：生成单个 `.exe` 文件。
- `--windowed`：不弹出命令行黑窗口（适合 GUI 应用）。
- `--noconfirm`：覆盖旧的打包结果无需确认。
- `--name "BlockerApp"`：指定打包生成的 exe 文件名。

4. 打包完成后，生成的可执行文件位于 `dist/BlockerApp.exe`。

5. （可选）为 `BlockerApp.exe` 创建桌面快捷方式，方便启动。

---
