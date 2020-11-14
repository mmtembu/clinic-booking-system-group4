import difflib

lines1 = '''
cat
dog
bird
buffalo
gopher
horse
mouse
'''.strip().splitlines()

lines2 = '''
dog
cat
bird
buffalo
gopher
horse
mouse
'''.strip().splitlines()

# Changes:
# swapped positions of cat and dog
# changed gophers to gopher
# removed hound
# added mouse

#print("show me result", list(difflib.unified_diff(lines1, lines2, fromfile='file1',tofile='file2', lineterm='')))
for line in difflib.unified_diff(lines1, lines2, fromfile='file1',tofile='file2', lineterm=''):
    print (line)
