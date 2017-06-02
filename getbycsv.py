#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from db_util import db_instance
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getstats():

    ret = db_instance.execute("select list.list_id,list.list_name, relation.song_id, song.song_name,song.artist_id, song.artist_name,song.state,list.tag_xiaomi\
                              from t_radio_list_songs as relation, t_radio_list as list ,t_song as song \
                              where list.state=1 and relation.list_id=list.list_id and relation.song_id=song.song_id order by list.list_id,relation.rate desc ")

    #csvfile = file('csv_stat.csv', 'wb')
    header=['list_id', 'list_name', 'song_id','song_name','artist_id','artist_name','state']
    with open('csv_stat.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header+['language','category','other'])
        for i in range(len(ret)):
            data=ret[i]
            tag=data['tag_xiaomi'].split('|')
            writer.writerow(     [data[headname] for headname in header]      )



    db_instance.close()
if __name__ == '__main__':
    getstats()
