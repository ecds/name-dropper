#!/usr/bin/env python

import argparse

import spotlight


def list_names(sc, filename):

    # preliminary: plain text file handling
    with open(filename) as txtfile:
        results = sc.annotate(txtfile.read())

    if not 'Resources' in results:
        print 'No resources identified'
        return

    # NOTE: dbpedia annotate result is per offset within the text, so
    # may include duplicates - e.g., different "surfaceForm" text variants
    # for the same URI, or same exact text and URI

    # TODO: consider uniquifying & alphabetizing this list
    # (or possibly use candidates instead of annotate for list output...)

    for resource in results['Resources']:
        print '%s  %s' % (resource['surfaceForm'].ljust(40), resource['URI'])


def main():
    parser = argparse.ArgumentParser(description='Look up named entities in a file.')
    parser.add_argument('filename', metavar='INPUT_FILE', type=str,
        help='name of the file to be processed')
    # dbpedia-specific options
    spotlight_opts = parser.add_argument_group('DBpedia Spotlight options')
    spotlight_opts.add_argument('--confidence', '-c', metavar='N', type=float, default=0.4,
        help='minimum confidence score (default: %(default)s)')
    spotlight_opts.add_argument('--support', '-s', metavar='N', type=int, default=20,
        help='minimum support score (default: %(default)s)')
    spotlight_opts.add_argument('--types', '-t', metavar='TYPES', type=str, default='Person,Place,Organisation',
        help='restrict to specific types of resources (default: %(default)s)')
    args = parser.parse_args()

    spotlight_args = {'confidence': args.confidence, 'support': args.support,
        'types': args.types}

    sc = spotlight.SpotlightClient(**spotlight_args)

    # for now, script only has a single mode: output a list of recognized names and URIs
    list_names(sc, args.filename)

    # Brief summary of API call activity
    print '\nMade %d API call%s in %s' % (sc.total_api_calls, 's' if sc.total_api_calls != 1 else '',
        sc.total_api_duration)


if __name__ == '__main__':
    main()

