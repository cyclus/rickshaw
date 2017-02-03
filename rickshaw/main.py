"""Main entry point for rickshaw"""
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint


from rickshaw import generate


def main():
    input_file = generate.generate()
    pprint(input_file)


if __name__ == '__main__':
    main()
