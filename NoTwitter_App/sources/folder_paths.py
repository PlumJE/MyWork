# 폴더 경로 상수
from os import makedirs
from os.path import dirname, isdir, realpath

app_dir = dirname(dirname(realpath(__file__)))
db_folder = app_dir + '/databases/'
graphics_folder = app_dir + '/graphics/'
GUI_folder = app_dir + '/GUIfiles/'

if not isdir(db_folder):
    makedirs(db_folder)