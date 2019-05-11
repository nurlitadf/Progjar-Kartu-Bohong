if __name__ == "__main__":
    def _creator():        
        screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)
        hello = HelloWorld(screen2)
        hello.run()
    MENU_ITEMS = ("Welcome", "Exit")
    SCREEN = pygame.display.set_mode((800, 600), 0, 32)
    FUNCS = {"Welcome": _creator, "Exit": sys.exit}
    GM = Main(SCREEN, FUNCS.keys(), FUNCS)
    GM.run()