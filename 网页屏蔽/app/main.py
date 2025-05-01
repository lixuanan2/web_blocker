from app.hosts_manager import backup_hosts, block_sites, unblock_sites

def main():
    backup_hosts()
    while True:
        print("\n=== Blocker App ===")
        print("1. 屏蔽网站")
        print("2. 解锁网站")
        print("3. 退出")
        choice = input("请输入操作编号：")
        if choice == "1":
            block_sites()
        elif choice == "2":
            unblock_sites()
        elif choice == "3":
            print("Bye～")
            break
        else:
            print("输入无效，请重新选择。")

if __name__ == "__main__":
    main()
