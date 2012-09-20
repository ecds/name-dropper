#!/usr/bin/env python

import argparse
from eulxml.xmlmap import load_xmlobject_from_file
from eulxml.xmlmap.eadmap import EncodedArchivalDescription as EAD

import spotlight


# TODO: may want to set up a local mirror of dbpedia spotlight,
# to avoid hitting production server for development work....

def list_names(sc, text):

    results = sc.annotate(text)

    if not 'Resources' in results:
        print 'No resources identified'
        return

    # NOTE: dbpedia annotate result is per offset within the text, so
    # may include duplicates - e.g., different "surfaceForm" text variants
    # for the same URI, or same exact text and URI

    # TODO: consider uniquifying & alphabetizing this list
    # (or possibly use candidates instead of annotate for list output...)

    # TODO: in list mode, maybe return a list of tuples (or similar), to
    # allow the results of multiple calls to be aggregated
    for resource in results['Resources']:
        print '%s  %s' % (resource['surfaceForm'].ljust(40), resource['URI'])


def main():
    parser = argparse.ArgumentParser(description='Look up named entities in a file.')
    parser.add_argument('filename', metavar='INPUT_FILE', type=str,
        help='name of the file to be processed')
    # FIXME: could we reliably auto-detect TEI/EAD/text file?
    parser.add_argument('--input', metavar='INPUT_TYPE', type=str, required=True,
        help='type of file to be processed', choices=['EAD', 'text'])
    # dbpedia-specific options
    spotlight_opts = parser.add_argument_group('DBpedia Spotlight options')
    spotlight_opts.add_argument('--confidence', '-c', metavar='N', type=float, default=0.4,
        help='minimum confidence score (default: %(default)s)')
    spotlight_opts.add_argument('--support', '-s', metavar='N', type=int, default=20,
        help='minimum support score (default: %(default)s)')
    spotlight_opts.add_argument('--types', '-t', metavar='TYPES', type=str, default='',  # Person,Place,Organisation',
        help='restrict to specific types of resources (default: %(default)s)')

    # NOTE! restricting to person/place/org leaves out literary prizes, which are otherwise being
    # recognized; check if these be tagged/identified in EAD for inclusion
    # - probably do want to exclude dates (don't seem to be recognized in a useful way...)
    args = parser.parse_args()

    spotlight_args = {'confidence': args.confidence, 'support': args.support,
        'types': args.types}

    sc = spotlight.SpotlightClient(**spotlight_args)

    if args.input == 'EAD':
        try:
            ead = load_xmlobject_from_file(args.filename, EAD)
        except Exception as err:
            print 'Error loading %s as EAD: %s' % (args.filename, err)
            return -1

        # run name lookup on targeted sections of EAD
        # - biographical statement
        for para in ead.archdesc.biography_history.content:
            list_names(sc, unicode(para))  # note: unicode normalizes whitespace

        # test first series
        series1 = ead.dsc.c[0]
        # series scope & content note
        for para in series1.scope_content.content:
            list_names(sc, unicode(para))
        for c in series1.c:
            # NOTE: if we do want to annotate file-level unit titles,
            # may want to do some pre-screening (date-only titles?),
            # or at least keep track to avoid looking up duplicates
            list_names(sc, unicode(c.did.unittitle))

    elif args.input == 'text':
        # NOTE: would probably need to be read / processed in chunks
        # if we want to handle text files of any significant size
        with open(args.filename) as txtfile:
            text = txtfile.read()
        list_names(sc, text)

    # for now, script only has a single mode: output a list of recognized names and URIs

    # Brief summary of API call activity
    print '\nMade %d API call%s in %s' % (sc.total_api_calls, 's' if sc.total_api_calls != 1 else '',
        sc.total_api_duration)


if __name__ == '__main__':
    main()

