# Advent of code day 1 -- A: 219
from distutils import util
import multiprocessing, time, argparse

def durationSince(sTime):
    return time.time() - sTime

def search(needle, haystack):
    return needle in haystack

def binarySearch(needle, haystack):
    if len(haystack) == 0:
        return False
    else:
        midstack = len(haystack)//2
        if haystack[midstack] == needle:
            return True
        else:
            if needle < haystack[midstack]:
                return binarySearch(needle, haystack[:midstack])
            else:
                return binarySearch(needle, haystack[midstack+1:])

def parallelSearch(pool, needle, haystack, cc ,s):
    results = [pool.apply_async(search, args = (needle, haystack[i if i == 0 else len(haystack) / i: i + s])) for i in range(cc)]
    results = [p.get() for p in results]
    return results

def main():
    cc = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cc)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputFile', help = 'Puzzle Input', required = True)
    parser.add_argument('-p', '--runParallel', help = 'Try running chunk/parallel', required = True)
    args = parser.parse_args()

    calibration = []
    with open(args.inputFile) as ifile:
        calibration = ifile.read().split('\n')
        ifile.close()

    freq = 0
    freqs = set()
    executionStart = time.time()
    previousExecutionTime = 0.0
    while True:
        for i in calibration:
            freqs.add(freq)
            freq += int(i)

            searchStart = time.time()
            if not util.strtobool(args.runParallel):
                if search(freq, freqs): 
                    print("Dupe: %d \nExecution Time: %s seconds" % (freq, durationSince(executionStart)))
                    break
            else:
                if True in parallelSearch(pool, freq, freqs, cc, len(freqs) / cc):
                    print("Dupe: %d \nExecution Time: %s seconds" % (freq, durationSince(executionStart)))
                    break
        else:
            previousExecutionTime = durationSince(searchStart) if previousExecutionTime < 0.00075 else 0.00075
            print("Frequency: %d \nExecution Time: %s seconds" % (freq, durationSince(searchStart)))
            continue
        break
                    
if __name__ == "__main__":
    main()