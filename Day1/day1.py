# Advent of code day 1 -- A: 219
from joblib import Parallel, delayed
from distutils import util
import multiprocessing, time, argparse

def durationSince(sTime):
    return time.time() - sTime

def search(needle, haystack):
    return needle in haystack

def parallelSearchJobLib(needle, haystack, cc, s):
    return Parallel(n_jobs = cc)(delayed(search)(needle, haystack[i if i == 0 else len(haystack) / i: i + s]) for i in range(cc))

def parallelSearchMultiprocessing(pool, needle, haystack, cc ,s):
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
    freqs = []
    executionStart = time.time()
    previousExecutionTime = 0.0
    while True:
        for i in calibration:
            freqs.append(freq)
            freq += int(i)

            searchStart = time.time()
            if (not util.strtobool(args.runParallel)) or (util.strtobool(args.runParallel) and previousExecutionTime < 0.00075):
                if search(freq, freqs): 
                    print("Dupe: %d \nExecution Time: %s seconds" % (freq, durationSince(searchStart)))
                    break
            else:
                if(True in parallelSearchMultiprocessing(pool, freq, freqs, cc, len(freqs) / cc)):
                    print("Dupe: %d \nExecution Time: %s seconds" % (freq, durationSince(executionStart)))
                    break
        else:
            previousExecutionTime = durationSince(searchStart) if previousExecutionTime < 0.00075 else 0.00075
            print("Frequency: %d \nExecution Time: %s seconds" % (freq, durationSince(searchStart)))
            continue
        break
                    
if __name__ == "__main__":
    main()