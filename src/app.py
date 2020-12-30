#!/usr/bin/env python
import sys

from age import get_data

if __name__ == '__main__':
    data = get_data(sys.argv[1:][0])

    print("")
    print(f"{data['title']} ({data['year']})")
    print("")
    print(f"{data['female']['name']} - {data['female']['age']} years old ({data['female']['year']})")
    print(f"{data['male']['name']} - {data['male']['age']} years old ({data['male']['year']})")
    print(f"Years of difference: {data['diff']}")
    print("")
