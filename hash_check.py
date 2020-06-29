import os
os.system('sha384sum dictionary.tar.gz > dictionary.sha')
os.system('sha384sum ligand.tar.gz > ligand.sha')
os.system('sha384sum protein.tar.gz > protein.sha')
state=True
try:
	with open('/app/data/dictionary.sha', 'r') as sha_file1:
		with open('dictionary.sha', 'r') as sha_file2:
			if sha_file1.readlines() != sha_file2.readlines():
				state = False
	with open('/app/data/ligand.sha', 'r') as sha_file1:
		with open('ligand.sha', 'r') as sha_file2:
			if sha_file1.readlines() != sha_file2.readlines():
				state = False
	with open('/app/data/protein.sha', 'r') as sha_file1:
		with open('protein.sha', 'r') as sha_file2:
			if sha_file1.readlines() != sha_file2.readlines():
				state = False
except:
	state = False
if state:
	print('true')
else:
	print('false')
