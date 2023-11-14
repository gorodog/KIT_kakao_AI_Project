import webbrowser

def open_link(url):
    webbrowser.open(url)
    
Home_url = "https://www.kumoh.ac.kr/ko/index.do"
Onestop_url = "https://www.kumoh.ac.kr/_common/login/login.do?Return_Url=https://onestop.kumoh.ac.kr"
LMS_url = "https://elearning.kumoh.ac.kr/"
Biskit_url = "https://biskit.kumoh.ac.kr/"


KITlink_Home = open_link(Home_url)
KITlink_Onestop = open_link(Onestop_url)
KITlink_LMS = open_link(LMS_url)
KITlink_Biskit = open_link(Biskit_url)