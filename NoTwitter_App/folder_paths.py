# 폴더 경로 상수
from os import makedirs
from os.path import dirname, isdir, realpath

login_posting_dir = dirname(realpath(__file__))
db_folder = login_posting_dir + '/databases/'
graphics_folder = login_posting_dir + '/graphics/'
GUI_folder = login_posting_dir + '/GUIfiles/'

if not isdir(db_folder):
    makedirs(db_folder)