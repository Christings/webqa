#python2
from __future__ import print_function
import math,sys,codecs,re,time,datetime,os,traceback
import Queue

'''
function to calc percentile
using box for some size.
'''

def usage(error_code = 1):
    extend_msg = ''
    if(error_code == 1):
        extend_msg = "no enough parameter. check: log_filename, percent, interval, box size."
    elif(error_code == 2):
        extend_msg = "precent should between from 0.00 to 1.00."
    elif(error_code == 3):
        extend_msg = "cannot fild logfile :" + input_datafile
    elif(error_code == 4):
        extend_msg = "cannot find box size. consider it 500 as default in OP online monitor."
    print ("Usage: \npython percentile.py logfile.log percentile interval\nexample: python calc_tp.py webcached_test.log 0.99 60, parm 2 should in 0.00-1.00. \n" + extend_msg)
    
time_se_style_1 = r'\d{8} \d{2}:\d{2}:\d{2}'
    
def get_pxx(data, percentile):
    data_to_sort = list(data)
    data_to_sort.sort(key=float)
    return data_to_sort[int(len(data_to_sort) * percentile)]
    
def get_readable_timestr(ts):
    ts = int(ts)
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    input_datafile = sys.argv[1] #which logfile to read?
    data_precent = float(sys.argv[2]) #percentile
    my_output_timestamp_interval = int(sys.argv[3])
    box_size = int(sys.argv[4])

    #check input good.
    if(data_precent > 1 or data_precent < 0):
        usage(2)
        sys.exit(1)

    if(not os.path.isfile(input_datafile)):
        usage(3)
        sys.exit(1)

    if(box_size < 1):
        usage(4)
        sys.exit(1)



    #box_size = 500 #in the box.
    #my_output_timestamp_interval = 15 #get every 15s
    box = []

    timestamp_key = 0

    show_percent = data_precent * 100

    wfp = open(input_datafile + "_p" + str(show_percent) + ".log", 'w+')
    wfp.write("timestamp,p" + str(show_percent))
    #outstr=''
    datestr=''
    datastr=''
    with open (input_datafile, 'r') as fp:
        for line in fp:
            try:
                if(not "Sogou-Observer" in line):
                    continue
                cost_str = line.split("cost=")[1].split(",")[0]
                mat = re.search(time_se_style_1, line)
                if(not mat is None):
                    my_timestamp = (time.mktime(datetime.datetime.strptime(mat.group(0), "%Y%m%d %H:%M:%S").timetuple()))
                if(len(box) < box_size):
                    box.append(cost_str)
                else:
                    #process when box is full. calc pxx, then remove [0] and append it
                    #print only when timestamp > 15s
                    if(my_timestamp - timestamp_key > my_output_timestamp_interval):
                        timestamp_key = my_timestamp
                        mypxx = get_pxx(box, data_precent)
                        #print (str(my_timestamp) + "," + mypxx + ", box size:" + str(len(box)) + ", max:" + str(max(box, key=float)) + ", min:" + str(min(box, key=float)))
                        wfp.write("".join([str(get_readable_timestr(my_timestamp)), str(mypxx)]))
                        #outstr+=('[%d' % (int(my_timestamp)*1000)+','+str(mypxx)+'],')
                        #print ("in:" + str(cost_str) + ", out:" + str(box[0]))
                        datestr+=(str(int(my_timestamp)*1000)+',')
                        datastr+=(str(mypxx)+',')
                    #update box.
                    del box[0]
                    box.append(cost_str)
            except Exception as e:
                traceback.print_exc()

    wfp.close()
    #print(outstr)
    print(datestr)
    print(datastr)
