#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
def path2abolutepath(path, base_dir=os.path.dirname(__file__)):
	if path[0] != '/':
		return os.path.join(base_dir, path)
	else:
		return path
