# inimerger

Simple python program to merge two ini files with files specified later in the parameter list overriding matched values in earlier files.

# Example

Given:
```
#inifile1.ini
[shared]
prop_uniue1 = 1
prop_shared = 10

[unique1]
test_unique = 101
```

```
# inifile2.ini
[shared]
prop_uniue2 = 2
prop_shared = 14

[unique2]
test_unique = 102
```

and running:
```
$ ./inimerger.py -o merged.ini inifile1.ini initfile2.ini
```
The result will be:
```
#merged.ini

[shared]
prop_uniue1 = 1
prop_uniue2 = 2
prop_shared = 14

[unique1]
test_unique = 101

[unique2]
test_unique = 102
`
```
