import fileinput

def main():
	traces = []

	for line in fileinput.input():
		trace = line.rstrip().split(' ')
		traces.append(trace)

	print(traces)
main()
