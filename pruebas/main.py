from scraper import PostScraping
from controller import Menu

def main():
    ps = PostScraping()
    objeto_menu = Menu(ps)
    objeto_menu.mostrar_menu()

if __name__ == '__main__':
    main()
