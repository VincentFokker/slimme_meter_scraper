from src.slimmemeterdata.slimmemeterlezer import SlimmeMeterLezer


def main():
    """Main function to run."""
    lezer = SlimmeMeterLezer()
    lezer.run()
    print("Files downloaded.")


if __name__ == "__main__":
    main()
