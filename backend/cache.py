from time import sleep

def main():
    while True:
        try:
            import cache2
            cache2.main()
            sleep(60)
        except:
            sleep(60)


if __name__ == "__main__":
    main()