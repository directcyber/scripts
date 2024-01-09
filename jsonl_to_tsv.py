#!/usr/bin/env python3
import json
import csv
import sys


if len(sys.argv) < 3:
	print("usage: %s <field1,field2,...> <file>" % sys.argv[0]) 
	exit(1)
fields_csv = sys.argv[1]
fields = fields_csv.split(',')

SEP='\t'

file = sys.argv[2]

def get_field_recur(d, key):
	if '.' not in key:
		if d == None:
			return d
		elif '[' in key and key.endswith(']'):
			index = int(key.split('[')[1].split(']')[0])
			actual_key = key.split('[')[0]
			if actual_key in d:
				try:
					return d[actual_key][index]
				except Exception as e:
					print("error in get_field_recur:", e)
					return None
			else:
				return None
		return d.get(key)

	ks = key.split('.')

	if '[' in ks[0] and ']' in ks[0]:
		index = int(ks[0].split('[')[1].split(']')[0])
		actual_ks = ks[0].split('[')[0]
		try:
			return get_field_recur(d.get(actual_ks)[index], '.'.join(ks[1:]))
		except Exception as e:
			print("error in get_field_recur:", e)
			return None
	else:
		try:
			return get_field_recur(d.get(ks[0]), '.'.join(ks[1:]))
		except Exception as e:
			print("error in get_field_recur:", e)
			return None


with open(file, 'r') as f:
	for line in f:
		# print(line)
		d = json.loads(line.strip())
		# for l in d:
		for field in fields:
			if '[' in field:
				fieldindex = int(field.split('[')[1].split(']')[0])
				fieldname = field.split('[')[0]
				if d.get(fieldname):
					# print(get_field_recur(d, fieldname)[fieldindex], end=SEP)
					try:
						print(d[fieldname][fieldindex], end=SEP)
					except IndexError:
						print(None, end=SEP)
				else:
					print(None, end=SEP)
			else:
				print(get_field_recur(d, field), end=SEP)

		print()
