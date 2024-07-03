from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior

from others import dbinterface, appregister, logger
from folder_paths import GUI_folder, graphics_folder

Builder.load_file(GUI_folder + 'post_screen_GUI.kv')

# 지금까지 찾아다닌 게시글들의 id들의 이력들을 저장하는 클래스
class SearchLog:
    logs = ['']
    ptr = 0
    def add(self, log):
        if self.ptr < len(self.logs) - 1:
            del self.logs[self.ptr + 1:]
        self.logs.append(log)
        self.ptr += 1
        logger.info("Search log is : " + str(self.logs))
    def prev(self):
        if self.ptr > 0:
            self.ptr -= 1
            return self.logs[self.ptr]
        else:
            return
    def next(self):
        if self.ptr < len(self.logs) - 1:
            self.ptr += 1
            return self.logs[self.ptr]
        else:
            return
searchlog = SearchLog()

# 게시글 유닛 클래스
class PostUnit(ButtonBehavior, BoxLayout):
    # 게시글에 게시글id, 작성자id, 작성날짜, 내용을 입력해 게시글 유닛을 생성한다
    def __init__(self, id, writer, writedate, content, **kwargs):
        super(PostUnit, self).__init__(**kwargs)
        self.id = id
        username = dbinterface.selectByUsernum(writer)
        if username == None:
            username = 'Not Twitter Official'
        else:
            username = username[0]
        self.ids.writer.text += username
        self.ids.writedate.text += writedate
        self.ids.content.text = content
    # 게시글을 클릭하면 해당 게시글과 그것의 자식 게시글들을 소환한다. 다만 공지사항을 클릭하면 작동하지 않는다
    def updateposts(self, *args):
        # 공지사항 게시글 유닛인 경우...
        if self.id != '':
            searchlog.add(self.id)
            postscreen.updateposts(self.id, *args)

# 게시글 스크린 클래스
class PostScreen(Screen):
    bg_path = graphics_folder + 'post_background.jpg'
    # 게시글 스크린으로 들어가기 직전의 행동이다
    def on_pre_enter(self, *args):
        username = dbinterface.selectByUsernum(appregister.usernum())[0]
        self.ids.welcome_message.text = 'Welcome, ' + username + '!'
        self.updateposts(appregister.curparent())
    # 부모가 되는 게시글과 그것의 자식 게시글들을 소환한다
    def updateposts(self, parent='', *args):
        if self.ids.body.children != []:
            self.ids.body.clear_widgets()
        # parent가 ''이면 공지사항 게시글을 맨 위에 추가한다
        if (parent == ''):
            self.ids.body.add_widget(PostUnit('', 0, '2000-01-01', 
"""Welcome to this app!
This is copycat of Twitter(current day X),
but this app cannot edit or delete your post,
except the administator can delete post content.
Post carefully!"""))
        appregister.curparent(parent)
        postlists = dbinterface.selectPosts(parent)
        if postlists == None:
            return
        for p in postlists:
            self.ids.body.add_widget(PostUnit(p[0], p[1], p[2], p[3]))
    # 이전에 방문한 게시글 및 그의 자식들을 불러온다
    def go_prev(self, *args):
        log = searchlog.prev()
        if log == None:
            return
        else:
            self.updateposts(log)
    # 이후에 방문한 게시글 및 그의 자식들을 불러온다
    def go_next(self, *args):
        log = searchlog.next()
        if log == None:
            return
        else:
            self.updateposts(log)
    # 게시글 작성 스크린으로 들어간다
    def goto_edit_screen(self):
        self.manager.current = 'Edit Screen'
    # 환경설정 스크린으로 들어간다
    def goto_setting_screen(self):
        self.manager.current = 'Setting Screen'
postscreen = PostScreen(name='Post Screen')
