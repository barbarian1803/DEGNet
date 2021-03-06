#!/usr/bin/env python2
"""
A very simple and not 100% compliant parser for the OBO file format

This parser is supplied "as is"; it is not an official parser, it
might puke on perfectly valid OBO files, it might parse perfectly
invalid OBO files, it might steal your kitten or set your garden shed
on fire. Apart from that, it should be working, or at least
it should be in a suitable condition to parse the Gene Ontology,
which is my only test case anyway.

Usage example::

    import gene_ontology.obo as obo
    parser = obo.Parser(open("gene_ontology.1_2.obo"))
    gene_ontology = {}
    for stanza in parser:
        gene_ontology[stanza.tags["id"][0]] = stanza.tags
"""

__author__  = "Tamas Nepusz"
__email__   = "tamas@cs.rhul.ac.uk"
__copyright__ = "Copyright (c) 2009, Tamas Nepusz"
__license__ = "MIT"
__version__ = "0.1"


__all__ = ["ParseError", "Stanza", "Parser"]


from cStringIO import StringIO
import re
import tokenize


class ParseError(Exception):
    """Exception thrown when a parsing error occurred"""

    def __init__(self, msg, lineno = 1):
        Exception.__init__("%s near line %d" % (msg, lineno))
        self.lineno = lineno


class Stanza(object):
    """Class representing an OBO stanza.

    An OBO stanza looks like this::

      [name]
      tag: value
      tag: value
      tag: value

    Values may optionally have modifiers, see the OBO specification
    for more details. This class stores the stanza name in the
    `name` member variable and the tags and values in a Python
    dict called `tags`. Given a valid stanza, you can do stuff like
    this:

      stanza.name
      "Term"
      stanza.tags["id"]
      ['GO:0015036']
      stanza.tags["name"]
      ['disulfide oxidoreductase activity']

    Note that the `tags` dict contains lists associated to each
    tag name. This is because theoretically there could be more than
    a single value associated to a tag in the OBO file format.
    """

    __slots__ = ["name", "tags"]

    def __init__(self, name, tags=None):
        """Creates a new stanza with the given name and the given
        tags (which must be a dict)"""
        self.name = name
        if tags:
            self.tags = dict(tags)
        else:
            self.tags = dict()

    def __repr__(self):
        """Returns a Python representation of this object"""
        return "%s(%r, %r)" % (self.__class__.__name__,self.name, self.tags)


class Parser(object):
    """The main attraction, the OBO parser."""

    def __init__(self, fp):
        """Creates an OBO parser that reads the given file-like object.
        If you want to create a parser that reads an OBO file, do this:

          import obo
          parser = obo.Parser(file("gene_ontology.1_2.obo"))

        Only the headers are read when creating the parser. You can
        access these right after construction as follows:

        parser.headers["format-version"]
          ['1.2']

        To read the stanzas in the file, you must iterate over the
        parser as if it were a list. The iterator yields `Stanza`
        objects.
        """
        if isinstance(fp, (str, unicode)):
            fp = open(fp)
        self.fp = fp
        self.line_re = re.compile(r"\s*(?P<tag>[^:]+):\s*(?P<value>.*)")
        self.lineno = 0
        self._read_headers()

    def _lines(self):
        """Iterates over the lines of the file, removing
        comments and trailing newlines and merging multi-line
        tag-value pairs into a single line"""
        while True:
            self.lineno += 1
            line = self.fp.readline()
            if not line: break

            line = line.strip()
            if not line:
                yield line
                continue

            if line[0] == '!': continue
            if line[-1] == '\\':
                # This line is continued in the next line
                lines = [line[:-1]]
                finished = False
                while not finished:
                    self.lineno += 1
                    line = self.fp.readline()
                    if line[0] == '!': continue
                    line = line.strip()
                    if line[-1] == '\\':
                        lines.append(line[:-1])
                    else:
                        lines.append(line)
                        finished = True
                line = " ".join(lines)
            else:
                try:
                    # Search for a trailing comment
                    comment_char = line.rindex("!")
                    line = line[0:comment_char].strip()
                except ValueError:
                    # No comment, fine
                    pass

            yield line

    def _parse_line(self, line):
        """Parses a single line consisting of a tag-value pair
        and optional modifiers. Returns the tag name and the
        value as a `Value` object."""
        match = self.line_re.match(line)
        if not match: return False
        tag, value_and_mod = match.group("tag"), match.group("value")

        # If the value starts with a quotation mark, we parse it as a
        # Python string -- luckily this is the same as an OBO string
        if value_and_mod and value_and_mod[0] == '"':
            g = tokenize.generate_tokens(StringIO(value_and_mod).readline)
            for toknum, tokval, _, (erow, ecol), _ in g:
                if toknum == tokenize.STRING:
                    value = eval(tokval)
                    mod = (value_and_mod[ecol:].strip(), )
                    break
                raise ParseError("cannot parse string literal", self.lineno)
        else:
            value = value_and_mod
            mod = None

#        value = Value(value, mod)
        return tag, value

    def _read_headers(self):
        """Reads the headers from the OBO file"""
        self.headers = {}
        for line in self._lines():
            if not line or line[0] == '[':
                # We have reached the end of headers
                self._extra_line = line
                return
            key, value = self._parse_line(line)
            try:
#                self.headers[key].append(value.value)
                self.headers[key].append(value)
            except KeyError:
#                self.headers[key] = [value.value]
                self.headers[key] = [value]

    def stanzas(self):
        """Iterates over the stanzas in this OBO file,
        yielding a `Stanza` object for each stanza."""
        stanza = None
        if self._extra_line and self._extra_line[0] == '[':
            stanza = Stanza(self._extra_line[1:-1])
        for line in self._lines():
            if not line: continue
            if line[0] == '[':
                if stanza: yield stanza
                stanza = Stanza(line[1:-1])
                continue
            tag, value = self._parse_line(line)
            try:
                stanza.tags[tag].append(value)
            except KeyError:
                stanza.tags[tag] = [value]

        yield stanza

    def __iter__(self): return self.stanzas()

    @staticmethod
    def get_all_ontology(fname):
        print "parsing file "+fname+"..."
        fp = open(fname)
        parser = Parser(fp)
        count = 0
        stanzas = {}
        for stanza in parser:
            stanzas[stanza.tags["id"][0]]=stanza

        print "Parsing successful, %d stanzas" % len(stanzas)
        return stanzas

if __name__ == "__main__":
    Parser.get_all_ontology("../data/go-basic.obo")