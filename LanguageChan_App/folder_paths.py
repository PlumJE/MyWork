#폴더 경로 상수들
from os.path import dirname, realpath

app_dir = dirname(realpath(__file__))

graphics_folder = app_dir + '/graphics'
bg_folder = graphics_folder + '/background'
charas_folder = graphics_folder + '/charas'
enemies_folder = graphics_folder + '/enemies'

GUI_folder = app_dir + '/GUIfiles'
