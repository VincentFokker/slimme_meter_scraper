from src.slimmemeterdata.slimmemeterlezer import SlimmeMeterLezer


def main():
    """Main function to run."""
    print("Initializing reading..")
    lezer = SlimmeMeterLezer()
    print("Run Reader..")
    lezer.run()
    print("Files downloaded. ")


if __name__ == "__main__":
    main()
