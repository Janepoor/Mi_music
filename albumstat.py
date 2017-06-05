#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
from db_util import db_instance
import logging
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def split_tag(input_tag):
    language_tagset = ['华语', '欧美', '粤语', '日语', '闽南语', '韩语', '小语种']
    genre_tagset = ['流行', '摇滚', '民谣', '电子', '说唱', '轻音乐', '爵士', '乡村', 'R&B/Soul', '后摇', '舞曲',
                    '英伦', '金属', '朋克', '蓝调', '雷鬼', '拉丁', '另类/独立', '古典', '民族', '古风', '中国风']
    emotion_tagset = ['怀旧', '清新', '伤感', '治愈', '放松', '安静', '浪漫', '性感', '孤独', '感动', '兴奋', '快乐', '思念', '励志', '回忆', '幸福',
                      '忧郁']
    scene_tagset = ['驾车', '运动', '旅行', '逛街', '起床', 'KTV', '在路上', '咖啡馆', '广场舞', '地铁', '散步', '酒吧',
                    '校园', '休闲', '婚礼', '洗澡', '瑜伽', '胎教', '学习', '工作']
    theme_tagset = ['影视原声', '游戏', '儿歌', '网络歌曲', '铃声', '经典', '榜单', '新歌', '节日', '天气', '其他']
    decade_tagset = ['70后', '80后', '90后', '60后', '00后', '10后']
    instrument_tagset = ['钢琴', '吉他', '器乐', '小提琴', '大提琴', '萨克斯', '古筝', '二胡']

    tag_list = input_tag.split('|')   #(data_file['tag_xiaomi'])

    lang=[]
    for i in tag_list:
        if i in language_tagset:
            lang.append(i)
        else:
            lang.append('')

    genre=[]
    for i in tag_list:
        if i in genre_tagset:
            genre.append(i)
        else:
            genre.append('')

    emotion=[]
    for i in tag_list:
        if i in emotion_tagset:
            emotion.append(i)
        else:
            emotion.append('')
    scene=[]
    for i in tag_list:
        if i in scene_tagset:
            scene.append(i)
        else:
            scene.append('')

    theme=[]
    for i in tag_list:
        if i in theme_tagset:
            theme.append(i)
        else:
            theme.append('')

    decade=[]
    for i in tag_list:
        if i in decade_tagset:
            decade.append(i)
        else:
            decade.append('')

    instrument = []
    for i in tag_list:
        if i in instrument_tagset:
            instrument.append(i)
        else:
            instrument.append('')

    return lang,genre,emotion,scene,theme,decade,instrument


def get_album_stats(input_txt='album.txt'):
    logging.info('Retrieving album info...')
    data_line=[]    # data row
    same_line=[]    # data that with multiple times
    original_album_set=[]
    get_album_set=[]
    name_set=set([])
    with open(input_txt, 'r') as w:
        lines=w.readlines()
        for line in lines:
            al_array=line.split('\t')
            album_name=str(al_array[0])
            play_times=al_array[1].strip()

            original_album_set.append(album_name)

            if not play_times.isdigit() :
                logging.warning('Warnning: play time not number')
            ret = db_instance.execute("select al.list_id,al.list_name, al.artist_id, so.artist_name, so.song_id, so.song_name,al.tag_xiaomi from t_list as al, t_song as so \
                                        where  al.list_type ='album' and al.list_name = '{name}'  and al.list_id = so.album_id".format(name=album_name) )


            logging.info('SQL executed ready')


            #### use set to mark the multiple
            for i in range(len(ret)):
                data_file=ret[i]
                samename=False
                for i in range(len(ret)):
                    name_set.add(data_file['list_name'])
                if data_file['list_name'] in name_set:
                    samename=True

                # split tag
                insert_tag=split_tag(data_file['tag_xiaomi'])

                if samename:
                    same_line.append([data_file['list_id'],data_file['list_name'],str(play_times), data_file['artist_id'],data_file['artist_name'],
                                 data_file['song_id'],data_file['song_name']]+insert_tag[0]+insert_tag[1])
                else:
                    data_line.append([data_file['list_id'],data_file['list_name'],str(play_times), data_file['artist_id'],data_file['artist_name'],
                                 data_file['song_id'],data_file['song_name']]+insert_tag[0]+insert_tag[1])

                if data_file['list_name'] not in get_album_set:
                    get_album_set.append(data_file['list_name'])

    checkmissing(original_album_set,get_album_set)
    db_instance.close()

    return same_line,data_line


def writecsv(input_file,outfile='album_stats.csv'):


    header=['album_id', 'album_name','playtimes_online','artist_id','artist_name','song_id','song_name','album_tag1_language','album_tag2_genre']
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for line in input_file:
            writer.writerow(line)

def checkmissing(original,get):
    for n in original:
        if n not in get:
            logging.warning('Cannot find album: %s' % (n))




if __name__ == '__main__':

    same_file,input_file=get_album_stats('album_test.txt')
    writecsv(same_file,'samename_album.csv')
    writecsv(input_file, 'album_stats.csv')

'''
for i in range(len(ret)):
    samename=False
    data_file = ret[i]
    for j in range(len(ret)):
        if data_file['list_id'] != (ret[j])['list_id']:
            samename=True
'''