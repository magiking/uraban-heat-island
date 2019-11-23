import numpy as np
import re
import os
from pyhdf.SD import SD, SDC

def infoFromFilename(fname):
    feature = re.split('\.', fname)
    # print(feature)
    # 1 -> AYYYYDDD
    # 2 -> HHMM
    date = (feature[1])
    time = (feature[2])
    year = int(date[1:5])
    day = int(date[5:])
    hour = int(time[:2])
    minute = int(time[2:])
    if minute > 30:
        year, day, hour = julianRoundUp(year, day, hour)
    return year, day, hour
    
def julianRoundUp(year, day, hour):
    hour = hour + 1 % 24
    if hour == 0:
        if isLeapYear(year):
            day = (day + 1) % 366
        else:
            day = (day + 1) % 355
        if day == 0:
            year = year + 1
    return year, day, hour

def isLeapYear(year):
    ''' Cheating, because we are only going back to 2009. '''
    return year == 2012 or year == 2016 or year == 2020
        


if __name__ == "__main__":
    ### shape
    # print(f.info())

    ### for checking the keys
    # datasets_dic = f.datasets()
    # for idx,key in enumerate(datasets_dic.keys()):
    #     print(idx)
    #     print(key)

    station = {
        481410029:{ 'name': 'Ivanhoe',              'lat': 31.7857687, 'lon': -106.3235781 },
        481410037:{ 'name': 'El Paso UTEP',         'lat': 31.7682914, 'lon': -106.5012595 },
        481410038:{ 'name': 'Riverside',            'lat': 31.7338000, 'lon': -106.3721000 },
        481410044:{ 'name': 'El Paso Chamizal',     'lat': 31.7656854, 'lon': -106.4552272 },
        481410047:{ 'name': 'Womble',               'lat': 31.7759422, 'lon': -106.4131769 },
        481410054:{ 'name': 'El Paso Lower Valley', 'lat': 31.703846 , 'lon': -106.3560220 },
        481410055:{ 'name': 'Ascarate Park SE',     'lat': 31.7467753, 'lon': -106.4028059 },
        481410057:{ 'name': 'Socorro Hueco',        'lat': 31.6675000, 'lon': -106.2880000 },
        481410058:{ 'name': 'Skyline Park',         'lat': 31.8939133, 'lon': -106.4258270 },
        481410693:{ 'name': 'VanBuren',             'lat': 31.8133700, 'lon': -106.4645200 },
        481411011:{ 'name': 'El Paso Delta',        'lat': 31.7584760, 'lon': -106.4073460 },
        481411021:{ 'name': 'Ojo De Agua',          'lat': 31.8624700, 'lon': -106.5473000 },
        }

    base_dir = './hdf/20180101-20191101/'
    flist = sorted(os.listdir(base_dir))
    features = []
    # do this for each file
    for fname in flist:

        f = SD(base_dir + fname, SDC.READ)
        ### select sds obj
        lat_obj = f.select('Latitude')
        lon_obj = f.select('Longitude')
        lst_obj = f.select('LST')
        vt_obj  = f.select('View_time')

        ### get sds data
        lat_data = lat_obj.get()
        lon_data = lon_obj.get()
        lst_data = lst_obj.get()
        vt_data  = vt_obj.get()

        # filter hdf points by loacation bound
        inbound = []
        year, day, hour = infoFromFilename(fname)
        for i in range(np.shape(lat_data)[0]):
            for j in range(np.shape(lat_data)[1]):
                if lat_data[i][j] > 31.5 and lat_data[i][j] < 31.9:
                    if lon_data[i][j] > -106.5 and lon_data[i][j] < -106.3:
                        inbound.append([
                            0, # station
                            year,
                            day,
                            hour,
                            lat_data[i][j],
                            lon_data[i][j],
                            lst_data[i][j],
                            vt_data[i][j],
                        ])

        # make sure that there were points that are inbound
        if len(inbound) == 0:
            continue

        # compare stations to inbound points and find closest one to each station
        for sid in station.keys():
            location = np.array([station[sid]['lat'], station[sid]['lon']])
            distance = []
            for ex in inbound:
                point = np.array([ex[4], ex[5]])
                # euclidean distance
                distance.append(np.sqrt(np.sum((location-point)*(location-point))))
            t = inbound[np.argmin(distance)]
            t[0] = sid
            features.append(t)

    features = np.array(features)
    np.save('station-lst.npy', features)


