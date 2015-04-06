import os
import fnmatch
import shutil
import json

def recursive_copy(base_dir, src, dest):
	cwd = os.getcwd()
	os.chdir(base_dir)
	try:
		shutil.copytree(src, dest)
	except OSError as exc:
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dest)
		else:
			raise
	os.chdir(cwd)

def recursive_list(src, regex):
	files = []
	for root, dirnames, filenames in os.walk(src):
		for filename in fnmatch.filter(filenames, regex):
			files.append(os.path.abspath(os.path.join(root, filename)))
		for dirname in dirnames:
			path = os.path.join(root, dirname)
			for entry in recursive_list(path, regex):
				files.append(entry)
	files = list(set(files))
	files.sort()
	return files

'''
Only applies regex to files
'''
def ls(src, regex):
	files = []
	dirs  = []
	if not os.path.isdir(src):
		return files, dirs
	entries = os.listdir(src)
	for entry in entries:
		path = os.path.join(src, entry)
		if os.path.isfile(path) and fnmatch.fnmatch(entry, regex):
			files.append(entry)
		if os.path.isdir(path):
			dirs.append(entry)

	files.sort()
	dirs.sort()
	return files, dirs

