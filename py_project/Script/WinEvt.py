#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import pywintypes
import win32evtlog
import datetime
import itertools
import pytz
import Constant

INFINITE = 0xFFFFFFFF
EVTLOG_READ_BUF_LEN_MAX = 0x7FFFF

LOGON_QUERY = "*[System[(EventID=4624)]] and *[EventData[Data[@Name='LogonType'] and (Data='2' or Data='7'or Data='11')]]"
SYSTEM_OFF_QUERY = "*[System[(EventID=1074)]]"

def get_events_xmls(channel_name="Security",query = LOGON_QUERY, events_batch_num=100, backwards=True):
    ret = []
    flags = win32evtlog.EvtQueryChannelPath
    if backwards:
        flags |= win32evtlog.EvtQueryReverseDirection
    try:
        query_results = win32evtlog.EvtQuery(channel_name, flags, query, None)
    except pywintypes.error as e:
        print(e)
        return ret
    events = win32evtlog.EvtNext(query_results, events_batch_num, INFINITE, 0)
    while events:
        for event in events:
            ret.append(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
        events = win32evtlog.EvtNext(query_results, events_batch_num, INFINITE, 0)
    return ret


def GetEvent(channel_name="Security",query = LOGON_QUERY,backwards=True):
    CREATE_TIME_TAG = "{http://schemas.microsoft.com/win/2004/08/events/event}TimeCreated"

    xmls = get_events_xmls(channel_name, query)
    
    DATE_FORMAT = "%Y-%m-%d"

    # now = datetime.datetime.now().strftime(TIME_FORMAT)
    # print(now)
    # print(datetime.datetime.strptime(now,TIME_FORMAT))
    # print()
    logonTime:list[datetime.datetime] = []
    for xml in xmls:
        tree = ET.fromstring(xml)[0].findall(CREATE_TIME_TAG)
        for child in tree:
            time_str = child.get("SystemTime").split(".")[0]
            time = datetime.datetime.strptime(time_str,Constant.TIME_READ_FORMAT).replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(Constant.TIME_ZONE))
            logonTime.append(time)
    logonDate = itertools.groupby(logonTime, lambda x:x.strftime(DATE_FORMAT))        

    logonResult:dict[str,datetime.datetime] = dict()

    for name,group in logonDate:
        sort = list(group)
        sort.sort()
        logonResult[name] = sort[0]
    
    return logonResult
            
if __name__ == "__main__":
    print(f'{datetime.datetime.now(pytz.UTC)} | {datetime.datetime.now()}')
    print(
        "Python {:s} {:03d}bit on {:s}\n".format(
            " ".join(elem.strip() for elem in sys.version.split("\n")),
            64 if sys.maxsize > 0x100000000 else 32,
            sys.platform,
        )
    )

    logonResult = GetEvent()
    for ret in logonResult:
        print(f'##{ret}| {logonResult[ret].strftime(Constant.TIME_OUTPUT_FORMAT)}')
    
    print("\nDone.\n")