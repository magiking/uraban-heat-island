import csv
import numpy as np

station_data = '2018-11-01-to-2019-11-01-met-noheader.csv'
pcd_list = [
    61101, # Wind speed - Scalar
    61102, # wind direction - Scalar
    61103, # Wind Speed - Resultant
    61104, # Peak Wind Gust
    61106, # Std Dev wind Direction
    62101, # Outdoor Temperature
    62103, # Dew point
    62106, # Temperature difference
    62201, # Relative Humidity (%RH)
    63301, # solar Radiattion
    63302, # ultraviolet radiation
    63305, # Net Radiation
    64101, # Barometric Pressure
    65102, # Rain/Melt Precipitation
    65301, # Volume (Precip)
    ]

data = {}
with open(station_data, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    line_count = 0
    for row in csv_reader:
        sid = row[4]
        pcd = row[5]
        d = row[10]
        t = row[11]
        v = row[12]

        # make sure that I can actually hash into the
        # right dictionaries
        # data = { sid: {date : {time: {pcd : val }}}}
        if sid not in data.keys():
            data[sid] = {}
        if d not in data[sid].keys():
            data[sid][d] = {}
        if t not in data[sid][d].keys():
            data[sid][d][t] = {}

        data[sid][d][t][pcd] = v


# How do I turn these into arrays?

dlist = []
for sid in data.keys():
    # print(sid)
    for date in data[sid].keys():
        # print("  " + date)
        for time in data[sid][date].keys():
            # print("    " + time)
            entry = [sid, date, time]
            for pcd in pcd_list:
                # print(pcd)
                # print(data[sid][date][time].keys())
                if pcd in data[sid][date][time].keys():
                    entry.append(data[sid][date][time][pcd])
                else:
                    entry.append(None) 
            dlist.append(entry)
                
dlist = np.array(dlist)
np.save('flat-tceq.npy', dlist)
