# 폴더 경로 상수
from os import makedirs
from os.path import dirname, isdir, realpath

this_app_dir = dirname(realpath(__file__))
db_folder = this_app_dir + '/databases/'
graphics_folder = this_app_dir + '/graphics/'
GUI_folder = this_app_dir + '/GUIfiles/'

if not isdir(db_folder):
    makedirs(db_folder)