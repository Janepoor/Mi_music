#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from db_util import db_instance
import xlsxwriter


def getstats():

    ret = db_instance.execute("select list.list_id,list.list_name, relation.song_id, song.song_name,song.artist_id, song.artist_name \
                              from t_radio_list_songs as relation, t_radio_list as list ,t_song as song \
                              where list.state=1 and relation.list_id=list.list_id and relation.song_id=song.song_id order by list.list_id,relation.rate desc ")

    book = xlsxwriter.Workbook('stats.xlsx')
    worksheet = book.add_worksheet()

    switcher = {
        0: "list_id",
        1: "list_name",
        2: "song_id",
        3: "song_name",
        4: "artist_id",
        5:"artist_name"
    }

    for i in range(0,5):
        worksheet.write(0,i,switcher[i])


    row = 1
    for i in range(len(ret)):
        data = ret[i]
        for item, value in data.iteritems():
            for number,name in switcher.iteritems():
                if item == name:
                    worksheet.write(row, number, value)
        row += 1
    book.close()


    db_instance.close()

if __name__ == '__main__':
    getstats()
