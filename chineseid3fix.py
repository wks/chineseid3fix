# Copyright 2016 Kunshan Wang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mutagen
import mutagen.mp3
import mutagen.id3

import argparse

def fix_file(filename, source_charset, dry_run):
    print("Opening file: {}".format(filename))
    try:
        m = mutagen.mp3.Open(filename)
    except mutagen.mp3.HeaderNotFoundError as e:
        print("Error opening file {}: {}".format(filename, e))
        return

    t = m.tags
    if t is None:
        print("File {} does not contain ID3 tags.".format(filename))
        return

    t.update_to_v24()
    for k,v in t.items():
#        print(k)
        if isinstance(v, mutagen.id3.TextFrame) and not isinstance(v, mutagen.id3.TimeStampTextFrame):
            enc = v.encoding
            old_ts = "".join(v.text)
            if v.encoding == mutagen.id3.Encoding.LATIN1:
                bs = old_ts.encode("latin1")
                ts = bs.decode(source_charset, errors="ignore")
                v.encoding = mutagen.id3.Encoding.UTF16
                v.text = [ts]
                fixed = True
            else:
                ts = old_ts
                fixed = False
            print("  {} Was {}: {} {}".format("*" if fixed else " ", enc, k, ts))
    if dry_run:
        print("Dry run. File not saved!")
    else:
        t.save(filename)
        print("File {} saved".format(filename))

parser = argparse.ArgumentParser(
        description="""
        Fix MP3 files that contain ID3 tags with wrong character encodings.
        """)

parser.add_argument('filenames', nargs='+', metavar="FILE",
                    help='the path to the MP3 file')
parser.add_argument('-s', '--source-charset', metavar="CHARSET",
                    default="gb18030",
                    help="""
                    the charset to assume if the tag encoding is LATIN1
                    (default: gb18030)
                    """)
parser.add_argument('-n', '--dry-run', action="store_true",
                    help="""
                    Don't actually change the tags, just print the updated
                    tags with fixed character encoding.
                    """)

def main():
    args = parser.parse_args()
    for filename in args.filenames:
        fix_file(
                filename=filename,
                source_charset=args.source_charset,
                dry_run=args.dry_run,
                )

if __name__ == '__main__':
    main()
