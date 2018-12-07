#python2
from __future__ import print_function
import math,sys,codecs,re,time,datetime,os

def usage(error_code = 1):
    extend_msg = ''
    if(error_code == 1):
        extend_msg = "no enough parameter. check: log_filename, percent, interval."
    elif(error_code == 2):
        extend_msg = "precent should between from 0.00 to 1.00."
    elif(error_code == 3):
        extend_msg = "cannot fild logfile :" + input_datafile
    print ("Usage: \npython percentile.py logfile.log percentile interval\nexample: python calc_tp.py webcached_test.log 0.99 60, parm 2 should in 0.00-1.00. \n" + extend_msg)


def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n) # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        #raise ValueError('variance requires at least two data points')
        return 0
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

if (len(sys.argv) != 4):
    usage(1)
    sys.exit(1)
    
input_datafile = sys.argv[1]
data_precent = float(sys.argv[2])
data_interval = int(sys.argv[3])

print ("Processing " + input_datafile + " ...")

#check input good.
if(data_precent > 1 or data_precent < 0):
    usage(2)
    sys.exit(1)
    
if(not os.path.isfile(input_datafile)):
    usage(3)
    sys.exit(1)
    
#output_filename
output_filename = 'stat_output_' + str(data_precent * 100) + ".csv"
summary_filename = 'stat_output_summary.txt'
    
date_re = re.compile(r'\d{8} \d{2}:\d{2}:\d{2}') #compile for timestamp like '20181203 15:40:04'

def get_readable_timestr(ts):
    ts = int(ts)
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

line_count = 0
item_count = 0 #calc total number
error_count = 0

data_frame_num = 500 #data frame mode
#data_percent = 0.99 #Pxx cent
data_percent = float(sys.argv[2])
cost_list = []
final_data = []
time_se_style_1 = r'\d{8} \d{2}:\d{2}:\d{2}'

sec_log_box = {} #a box contains data, key is timestamp, value is a list, and put all costs num in this list.
sec_log_box_keys = [] #to save keys(timestamp) for sec_log_box

def do_analy_timebox(in_str, time_se_style_1):
    #time_se_style_1 = r'\d{8} \d{2}:\d{2}:\d{2}'
    #time_se_style_2 = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    try:
        mat1 = re.search(time_se_style_1, in_str)
        if(not mat1 is None and len(mat1.groups()) > 0):
            return time.mktime(datetime.datetime.strptime(mat1.group(0), "%Y%M%D %H:%M:%S").timetuple())
        '''
        mat2 = re.search(time_se_style_2, in_str)
        if(not mat2 is None and len(mat2.groups()) > 0):
            return time.mktime(datetime.datetime.strptime(mat2.group(0), "%Y-%M-%D %H:%M:%S").timetuple())
        '''
        return None
    
    except Exception as e:
        print (e)
        return None


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

#with open (input_datafile, 'r', errors='ignore') as fp:
fp = codecs.open(input_datafile, 'r', errors = 'ignore')
for line in fp:
    if("Sogou-Observer" in line):
        try:
            timestamp_key = 0
            mat = re.search(time_se_style_1, line)
            if(not mat is None):
                timestamp_key = (time.mktime(datetime.datetime.strptime(mat.group(0), "%Y%m%d %H:%M:%S").timetuple()))
            else:
                mat = re.search(time_se_style_2, line)
                if(not mat is None):
                    timestamp_key = (time.mktime(datetime.datetime.strptime(mat.group(0), "%Y%m%d %H:%M:%S").timetuple()))
            #got timestamp_key, try to get cost...
            if(timestamp_key > 0):
                m_cost = line.split("cost=")[1].split(",")[0] #prase cost in this line.
                if(not timestamp_key in sec_log_box):
                    sec_log_box[timestamp_key] = [m_cost]
                    sec_log_box_keys.append(timestamp_key)
                else:
                    sec_log_box[timestamp_key].append(m_cost)
            
            #add to total box.
            cost_list.append(line.split("cost=")[1].split(",")[0])
            item_count = item_count + 1
        except Exception as e:
            print (e)
            error_count = error_count + 1
    line_count = line_count + 1
fp.close()

print ("Item count:" + str(item_count))
#print (sec_log_box)

sec_log_box_keys.sort(key=float)

#get data task done, start to analy...
new_data_key_list = []
new_data_list = []
new_data_small_box = []
slbk_sign = 0

#print (sec_log_box_keys)
#print (sec_log_box)

last_slbk = 0
for slbk in sec_log_box_keys: #read keys every seconds.
    if(slbk - slbk_sign >= data_interval):
        new_data_list.append(new_data_small_box)
        new_data_key_list.append(slbk)
        new_data_small_box = sec_log_box[slbk] #clear small_box && put current data into it
        #set sign to new key.
        slbk_sign = slbk
    else:
        for zk in sec_log_box[slbk]:
            new_data_small_box.append(zk) #merge lists into small box
    last_slbk = slbk
if(len(new_data_small_box) > 0): #add last small_box stay here.
    new_data_list.append(new_data_small_box)
    new_data_key_list.append(last_slbk + data_interval)

#check & output from final data.
pxx_list = []
first_line = True
wfp = open(output_filename, 'w+')
new_data_list_index = 0
for new_data_key in new_data_key_list:
    if(len(new_data_list[new_data_list_index]) > 0):
        new_data_list[new_data_list_index].sort(key=float)
        n_to_list = new_data_list[new_data_list_index]
        wfp.write (str(get_readable_timestr(new_data_key)) + "," + str(n_to_list[int(len(n_to_list) * data_percent)]) + "\n")
        pxx_list.append(float(n_to_list[int(len(n_to_list) * data_percent)]))
    else:
        if(first_line):
            first_line = False
        else:
            wfp.write (str(get_readable_timestr(new_data_key)) + ",0\n")
            if(not first_line):
                pxx_list.append(0)
    new_data_list_index = new_data_list_index + 1
wfp.close()

#write to summary result.
wfp = open(summary_filename, 'w+')
wfp.write ("".join(["====== parameter ======" , "\n"]))
wfp.write ("".join(["percent:", str(data_percent) ,"\n"]))
wfp.write ("".join(["interval:", str(data_interval) ," second(s)\n"]))
wfp.write ("".join(["====== statistics ======" , "\n"]))
wfp.write ("".join(["item count:", str(item_count) ,"\n"]))
wfp.write ("".join(["P", str(data_percent*100), " nodes count:", str(len(pxx_list)), "\n"]))
wfp.write ("".join(["max:", str(max(pxx_list)), "\n"]))
wfp.write ("".join(["min:", str(min(pxx_list)), "\n"]))
wfp.write ("".join(["max - min:", str(max(pxx_list) - min(pxx_list)), "\n"]))
wfp.write ("".join(["standard deviation:", str(stddev(pxx_list, 1)), "\n"]))
pxx_list.sort(key=float)
wfp.write ("".join(["P95 for all P", str(data_percent*100) , " data:", str(pxx_list[int(len(pxx_list) * 0.95)]), "\n"]))

wfp.close()

print ("task done. check output file:" + output_filename)
'''
ch_list = chunks(cost_list, data_frame_num) #split into chunks
for chunk in ch_list:
    final_data.append(np.percentile(chunk, data_percent))
print (final_data)
'''

