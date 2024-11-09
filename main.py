from ImageGenerator import ImageGenerator
from BibleVerseService import BibleVerseService
def main():
    verse_ref = input("Please enter a bible verse reference: ")

    service = BibleVerseService()
    ref, text = service.get_verse(verse_ref)

    if (ref != None):
        generator = ImageGenerator()
        generator.generate_image(ref, text)
    else:
        print(text)

if __name__ == '__main__':
    main()
