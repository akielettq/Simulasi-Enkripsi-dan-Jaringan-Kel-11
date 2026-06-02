from menu.menu_utama import jalankan_aplikasi

def main():
    try:
        jalankan_aplikasi()
    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan oleh user. Dadah!")

if __name__ == "__main__":
    main()