import datetime as dt

def melt(header, data):
    
    r_data = []

    format = "%m/%d/%Y %I:%M %p"

    for i in range(0,len(data)):
        for j in range(1, len(data[i])):
        
           # Create List Representation
            datetime_str = data[i][0] + " " + header[j]
            datetimes = dt.datetime.strptime(datetime_str, format)
            r_data.append([datetimes.strftime(format), data[i][j]])

    return r_data


