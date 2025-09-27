#!/usr/bin/env python3
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXCLUDES = {'.git', '.github', '.gitignore', 'Technical', 'Output'}

technical_dir = os.path.join(ROOT, 'Technical')
output_dir = os.path.join(ROOT, 'Output')
os.makedirs(technical_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

for entry in os.listdir(ROOT):
	if entry in EXCLUDES:
		continue
	src = os.path.join(ROOT, entry)
	dst = os.path.join(technical_dir, entry)
	try:
		shutil.move(src, dst)
	except Exception as e:
		print(f"Skip {entry}: {e}")

# Ensure Output contains PDFs if any were previously created
prev_output = os.path.join(technical_dir, 'Output')
if os.path.isdir(prev_output):
	for root, dirs, files in os.walk(prev_output):
		rel = os.path.relpath(root, prev_output)
		target = os.path.join(output_dir, rel)
		os.makedirs(target, exist_ok=True)
		for f in files:
			srcf = os.path.join(root, f)
			dstf = os.path.join(target, f)
			if not os.path.exists(dstf):
				shutil.copy2(srcf, dstf)
