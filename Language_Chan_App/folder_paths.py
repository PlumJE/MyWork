#폴더 경로 상수들입니다.
from os import makedirs
from os.path import dirname, isdir, realpath

app_dir = dirname(realpath(__file__))
db_folder = app_dir + '/databases/'
graphics_folder = app_dir + '/graphics/'
bg_folder = graphics_folder + '/background/'
charas_folder = graphics_folder + '/charas/'
enemies_folder = graphics_folder + '/enemies/'
GUI_folder = app_dir + '/GUIfiles/'

if not isdir(db_folder):
    makedirs(db_folder)