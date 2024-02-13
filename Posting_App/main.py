"""
작성자 : 외기러기
작성일 : 2023-03-02
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from datetime import datetime
import sqlite3


Builder.load_file('main_GUI.kv')

#SQLite3 DB와 연동하는 클래스
class DBInterface:
    conn = sqlite3.connect("PostingApp.db", isolation_level=None)
    cur = conn.cursor()
    def __init__(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS PostInfo(number int, writer text, content text, first_write date, latest_write date);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS CommentInfo(master int, writer text, content text);")
    def __del__(self):
        self.conn.close()
    def execute(self, cmd_str):
        print("Execute :", cmd_str)
        try:
            self.cur.execute(cmd_str)
            if cmd_str.upper().startswith("SELECT"):
                return self.cur.fetchall()
        except Exception:
            print("Error :", cmd_str, "문장에 이상이 있습니다!")
            return Exception()
db = DBInterface()


#게시글 목록의 단위가 되는 클래스
class PostListUnit(RecycleDataViewBehavior, BoxLayout):
    num = 0
    def refresh_view_attrs(self, rv, index, data):
        self.num = data['number']
        self.ids.writer.text = data['writer']
        self.ids.content.text = data['content']
        self.ids.first_date.text = data['first_date']
        self.ids.latest_date.text = data['latest_date']
        return super().refresh_view_attrs(rv, index, data)
    def goto_post_screen(self):
        posting_app.goto_post_screen(self.num)

#댓글 목록의 단위가 되는 클래스
class ReplyListUnit(RecycleDataViewBehavior, BoxLayout):
    def refresh_view_attrs(self, rv, index, data):
        return super().refresh_view_attrs(rv, index, data)

#작성자 이름을 입력받는 팝업창
class InputWriterPopup(Popup):
    def close(self):
        writer = self.ids.writer.text
        if writer.isspace() or writer == '':
            return
        pes.get_writer(self.ids.writer.text)
        self.dismiss()
    def refuse(self):
        pes.goback()
        self.dismiss()


#게시글 목록 화면을 나타내는 클래스
class PostListScreen(Screen):
    def __init__(self, **kwargs):
        super(PostListScreen, self).__init__(**kwargs)
        self.update()
    def update(self):
        queryresult = db.execute("SELECT * FROM PostInfo;")
        datas = []
        for qr in queryresult:
            datas.append({'number':int(qr[0]), 'writer':str(qr[1]), 'content':str(qr[2]), 'first_date':str(qr[3]), 'latest_date':str(qr[4])})
        self.ids.postlist.data = datas
    def goto_postedit_screen(self):
        posting_app.goto_postedit_screen()
pls = PostListScreen(name='Post list screen')

#게시글 화면을 나타내는 클래스
class PostScreen(Screen):
    num = None
    def intent(self, number):
        self.num = number
        qr = db.execute('SELECT writer, content, first_write, latest_write FROM PostInfo WHERE number=%s' % number)[0]
        self.ids.writer.text = 'writer :\n' + str(qr[0])
        self.ids.content.text = str(qr[1])
        self.ids.first_date.text = 'first write date :\n' + str(qr[2])
        self.ids.latest_date.text = 'latest write date :\n' + str(qr[3])
    def goto_postlist_screen(self):
        posting_app.goto_postlist_screen()
    def goto_postedit_screen(self):
        posting_app.goto_postedit_screen(self.num)
ps = PostScreen(name='Post screen')

#게시글 작성 화면을 나타내는 클래스
class PostEditScreen(Screen):
    num = None
    def intent(self, number=None):
        self.num = number
        if number == None:
            self.ids.writer.text = 'writer :\n'
            self.ids.content.text = ''
            self.ids.first_date.text = 'first write date :\n' + datetime.today().strftime('%Y-%m-%d')
            InputWriterPopup().open()
        else:
            self.new_writer = ''
            qr = db.execute('SELECT writer, content, first_write, latest_write FROM PostInfo WHERE number=%s' % number)[0]
            self.ids.writer.text = 'writer :\n' + str(qr[0])
            self.ids.content.text = str(qr[1])
            self.ids.first_date.text = 'first write date :\n' + str(qr[2])
        self.ids.latest_date.text = 'latest write date :\n' + datetime.today().strftime('%Y-%m-%d')
    def get_writer(self, writer):
        self.ids.writer.text = 'writer :\n' + str(writer)
    def upload(self):
        content = self.ids.content.text
        if content.isspace() or content == '':
            return            
        writer = self.ids.writer.text.replace('writer :\n', '')
        first_date = self.ids.first_date.text.replace('first write date :\n', '')
        latest_date = self.ids.latest_date.text.replace('latest write date :\n', '')
        try:
            if self.num == None:
                self.num = db.execute('SELECT COUNT(*) FROM PostInfo;')[0][0]
                db.execute("INSERT INTO PostInfo VALUES (%s, '%s', '%s', '%s', '%s');" % (self.num, writer, content, first_date, latest_date))
            else:
                db.execute("UPDATE PostInfo SET writer='%s', content='%s', first_write='%s', latest_write='%s' WHERE number=%s;" 
                           % (writer, content, first_date, latest_date, self.num))
            posting_app.goto_post_screen(self.num)
        except Exception:
            Popup(title='Error', content=Label(text='An Error Ocurred During Upload the Post!'), size_hint=(None, None), size=(400, 100), auto_dismiss=True).open()
    def goback(self):
        if self.num == None:
            posting_app.goto_postlist_screen()
        else:
            posting_app.goto_post_screen(self.num)
pes = PostEditScreen(name='Post edit screen')


#앱 전체를 나타내는 클래스
class PostingApp(App):
    sm = ScreenManager()
    def build(self):
        self.sm.add_widget(pls)
        self.sm.add_widget(ps)
        self.sm.add_widget(pes)
        return self.sm
    def goto_postlist_screen(self):
        pls.update()
        self.sm.current = 'Post list screen'
    def goto_post_screen(self, number):
        ps.intent(number)
        self.sm.current = 'Post screen'
    def goto_postedit_screen(self, number=None):
        pes.intent(number)
        self.sm.current = 'Post edit screen'
posting_app = PostingApp()
if __name__ == "__main__":
    posting_app.run()