# 예외처리(FileNotFoundError, PostNotFoundError, IndexError, ValueError)
# 데코레이터(자동저장, 실행권한)
# 메소드 구현(save, load)
import os
import datetime
import hashlib
import getpass

class User():
    def __init__(self, sign_in_id=None):
            self.sign_in_id = sign_in_id

    def signup(self):
        uid = input('아이디 : ')
        upasswd = getpass.getpass(prompt = '비밀번호 : ', stream = None)
        hexdigest_upw = hashlib.sha256(upasswd.encode()).hexdigest()
        data = {uid:hexdigest_upw}
        with open('account.csv', 'a', encoding = "euc-kr") as f:
            # [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]
            [f.write(f'{key},{value}\n') for key, value in data.items()] # python 3.6↑부터 지원
        self.sign_in_id = uid
        
    def signin(self):
            self.sign_in_id = input('아이디 : ')
            sign_in_pw = getpass.getpass(prompt = '비밀번호 : ', stream = None)
            hexdigest_pw = hashlib.sha256(sign_in_pw.encode()).hexdigest()
            # account = '{0},{1}'.format(self.sign_in_id,hexdigest_pw)
            account = f'{self.sign_in_id},{hexdigest_pw}'
            with open('account.csv', mode = 'r', encoding = 'euc-kr') as f:
                account_list = [line.rstrip() for line in f] # 개행문자 제거한 리스트 생성
            if account not in account_list: # 아이디,패스워드 값을 account_list와 비교
                clear()
                print_login_message()
                m = int(input(' >'))
                if m == 1 :
                    user.signin()
                if m == 2 :
                    user.signup()
            clear()
            return
                    
class Board():
    post_per_pages = 15
    
    def __init__(self):
          self.posts = []
          self.current_page = 1
          ##self.load() ## 파일이 존재하지 않는 상황에 대한 예외처리 필요

    def search_post_by_id(self, pid):
        for index, post in enumerate(self.posts):
            if post.has_pid(pid):
                return index, post
   
    def list_posts(self):
        if self.posts == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return
        
        page_from = (self.current_page - 1) * Board.post_per_pages
        page_to = self.current_page * Board.post_per_pages
        for post in self.posts[page_from : page_to]:
            print(post)
            

    def create_post(self): #1
        title = input('작성 > ')
        self.posts.insert(0, Post(title))

    def modify_post(self): #잘못된 글 번호 입력에 대한 예외처리 필요 #2
        pid = int(input('몇번 글을 수정할까요? '))
        new_title = input('수정 > ')
        _, post = self.search_post_by_id(pid)
        post.modify(new_title)
                      
    def delete_post(self): #삭제가 아닌 hidden 처리 필요 #잘못된 글 번호 입력에 대한 예외처리 필요 #3
        pid = int(input('몇번 글을 지울까요? '))
        index, _ = self.search_post_by_id(pid)
        del self.posts[index]

    def next_page(self): #4
        if self.current_page * Board.post_per_pages < len(self.posts):
            self.current_page += 1

    def previous_page(self): #5
        if self.current_page < 1:
            self.current_page -= 1    

class Post():
    pid = 1

    def __init__(self, title, pid=None, created_at=None):
        self.pid = Post.pid
        self.title = title
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.sign_id = user.sign_in_id
        Post.pid += 1

    def __str__(self):
        return '{:^8} | {:60.60} | {} | {}'.format(self.pid, self.title, self.sign_id, self.created_at)

    def modify(self, new):
        self.title = new

    def has_pid(self, pid):
        return self.pid == pid
    

def print_greeting_message():
    greeting_message = '''
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
    어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주
    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 
    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에
    품고서 오늘도 밤을 지새우며 코드를 작성합니다.
    '''
    print(greeting_message)
    input('프로그램을 시작하시려면 로그인하세요...')

def print_login_message():
    login_message = '''
    -------------------------------------------------------------
    1. 로그인
    2. 회원가입
    -------------------------------------------------------------
    '''
    print(login_message)


def feature_list():
    feature_list = '''
    1. 작성하기
    2. 수정하기
    3. 삭제하기
    4. 다음 페이지로
    5. 이전 페이지로
    '''
    print(feature_list)
    print('--------------------------------------------------------')

def success_signin_message():
    # print('로그인 성공 : 환영합니다', '{}님!'.format(user.sign_in_id))
    print('로그인 성공 : 환영합니다', f'{user.sign_in_id}님!')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    print_greeting_message()
    user = User()
    print_login_message()
    m = int(input(' >'))
    if m == 1 :
        user.signin()
    if m == 2 :
        user.signup()
    success_signin_message()
    board = Board()
    while True:
        ##clear()
        board.list_posts()
        feature_list()
        n = int(input(' >'))
        if n == 1 :
             board.create_post()
        elif n == 2:
             board.modify_post()
        elif n == 3:
             board.delete_post()
        elif n == 4:
             board.next_page()
        elif n == 5:
             board.previous_page()
