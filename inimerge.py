#!/usr/bin/python
import argparse
import ConfigParser
import sys
import os.path
import re, shutil, tempfile

from os import path

def sed_inplace(filename, pattern, repl):
	'''
	Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
	`sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
	credit: https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python
	'''
	# For efficiency, precompile the passed regular expression.
	pattern_compiled = re.compile(pattern)
	
	# For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
	# writing with updating). This is usually a good thing. In this case,
	# however, binary writing imposes non-trivial encoding constraints trivially
	# resolved by switching to text writing. Let's do that.
	with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
		with open(filename) as src_file:
			for line in src_file:
				tmp_file.write(pattern_compiled.sub(repl, line))
	# Overwrite the original file with the munged temporary file in a
	# manner preserving file attributes (e.g., permissions).
	shutil.copystat(filename, tmp_file.name)
	shutil.move(tmp_file.name, filename)

parser = argparse.ArgumentParser(description='a simple program to output the product of two ini config files, with later files overriding earlier values')
# If we'd wanted argparse to try and actually open the files (and thus confirm their presence) then we could use "type=argparse.FileType('r')" However we dont,
# just check if it exists and dont include it if it does not.

#parser.add_argument('files', type=argparse.FileType('r'), nargs='+')
parser.add_argument('files', nargs='+')
parser.add_argument('-o', '--output', dest="outputfile" , required=True, help="name of ini file to output to. Anything existing will be overwritten")
parser.add_argument('-s', '--spaces', dest="spaces" , action='store_true', help="Whether to surround the equal sign with spaces when outputting the resulting file. KDE Plasma needs no spaces")
parser.add_argument('-a', '--fail-on-no-exist', dest="failnoexist" , action='store_true', help="Whether or not to fail if any of the specified files in -f dont exist")
args = parser.parse_args()

if args.failnoexist:
	for f in args.files:
		if not path.exists(f):
			sys.stderr.write(f + ' Does not exist\n')
			sys.exit(1)

config = ConfigParser.ConfigParser()
# If you dont include this ConfigParser will cheerfully convert all keys to lower case, even better, this is to maintain compatibility with Windows!!!! (Insert expletive here)
# https://stackoverflow.com/questions/1611799/preserve-case-in-configparser/23836686
config.optionxform = lambda option: option

config.read(args.files)
with open(args.outputfile, 'wb') as configfile:
	config.write(configfile)
	configfile.close()

if not args.spaces:
	sed_inplace(args.outputfile, r' = ', '=')

sys.exit(0)
