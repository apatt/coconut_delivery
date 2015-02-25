# this sure looks like a variation of the traveling salesmen problem to me..  I found this while researching
# http://xkcd.com/399/
# The king should consider using amazon.. If he orders enough coconuts, he will get free shipping ;)

# i left in my debug print statemens so you can see what i did while developing

import sys

from pprint import pformat

# python has a limit of 1000, but that is not high enough for this sample set
# 1996 is the minimum needed for the large sample set, but setting it much higher in case of different sets
# it might need to be set even higher for larger or different sets.
sys.setrecursionlimit(10000)

def load_jetstreams(filename):
    f = open(filename)
    base = int(next(f)[:-1])
    path_end = 0
    js = []
    for line in f:
        # skip blank lines in case they get in
        if not line.strip():
            continue
        start, end, cost = [int(x) for x in line[:-1].split(' ')]
        if end > path_end:
            path_end = end
        #print start, end, cost
        js.append([start, end, cost])
    js.sort()
    print len(js)
    return base, path_end, js

# calculation cache to keep the number of loops sane 
# this turned the program from not returning after minutes to returning in about a second
CACHE = {}
# i used this to verify it did what was expected on the smaller data set
LOOPS = 0

# I do assume jetstream is always faster that "normal" space
def travel(current_cost, current_pos, js, base_cost, path_end, path, depth=1):
    global LOOPS
    ddepth = '%02d' % depth
    #print ddepth, '  ' * depth, 'init:', current_cost, current_pos, js, path
    results = []
    for index, j in enumerate(js):
        start, end, cost = j
        #print ddepth, '  ' * depth, 'loop:', start, end, cost
        cache_hit = CACHE.get((start, end))
        if cache_hit:
            #print ddepth, '  ' * depth, 'hit!'
            return cache_hit

        LOOPS += 1
        cost += current_cost   
        # can't use this jetstream, we are already past it (might be able to break)
        if current_pos > start:
            continue
        # js doesn't start for a while, so need to travel in normal space until then
        if current_pos < start:
            cost += (start - current_pos) * base_cost
        total_cost, final_path = travel(cost, end, js[index+1:], base_cost, path_end, path + ((start, end),), depth + 1 )
        CACHE[(start,end)] = [total_cost, final_path]
        results.append([total_cost, final_path])
#        if depth == 1:
#            print '.'
#            sys.stdout.flush()
    results.sort()
    if results:
        # return fastest path
        #print ddepth, '  ' * depth, 'all results:', results
        #print ddepth, '  ' * depth, 'return1:', results[0]
        return results[0]
    else:
        # could not travel on a js, so travel normal space until the end
        cost = current_cost + (path_end - current_pos) * base_cost
        #print ddepth, '  ' * depth, 'return2:', [cost, path]
        return [cost, path]
    
    
if __name__ == '__main__':
    #base, path_end, js = load_jetstreams('sample_paths.txt')
    base, path_end, js = load_jetstreams('flight_paths.txt')
    cost, path = travel(0, 0, js, base, path_end, ())
    
    print 'energy cost:', cost
    print 'path:', path
    
                