#!/usr/bin/env python

import os
import fnmatch


def find_by_extension(ext, search_path=None, verbose=False):
    if search_path is None:
        search_path = os.path.expanduser("~")

    matches = []
    for root, dir_names, file_names in os.walk(search_path):
        for filename in fnmatch.filter(file_names, '*.{}'.format(ext)):
            matches.append(os.path.join(root, filename))

    if verbose:
        print(matches)
    print("Found {} matching files.".format(len(matches)))

    return matches


if __name__ == '__main__':
    find_by_extension("ma", verbose=True)
