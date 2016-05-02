import pycommons
import time

for i in range(1, 1001):
	if i % 2 == 0:
		pycommons.print_progress(i, 1000, colors=True)
		time.sleep(0.01)

