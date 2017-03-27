"""Main entry point for rickshaw"""
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint
import json

from rickshaw import generate


def main():
    input_file = generate.generate()
    pprint(input_file)
    i = 0
    while i < 100:
        input_file = generate.generate()
        jsonfile = str(i)+'.json'
        with open(jsonfile, 'w') as jf:
            json.dump(input_file, jf, indent=4)
        i+=1


if __name__ == '__main__':
    main()
