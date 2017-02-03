import pprint

from rickshaw import generate


def main():
    input_file = generate.generate()
    pprint.pprint(input_file)


if __name__ == '__main__':
    main()
