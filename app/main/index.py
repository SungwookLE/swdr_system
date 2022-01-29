# file name : index.py
# pwd : /project_name/app/main/index.py
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import pandas as pd
from werkzeug.utils import secure_filename
from app.module import dbModule
import datetime


main = Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=["GET"])
def main_page():
    # /main/index.html은 사실 /project_name/app/templates/main/index.html을 카리킵니다.
    return render_template('/main/index.html')

@main.route('/project', methods=["GET"])
def project():
    render = select()
    return render

@main.route('/project/select', methods=["GET", "POST"])
def select(log_text=None):
    db_class = dbModule.Database()
    sql      = "SELECT * \
                FROM SWDR_DB.Project"
    
    if log_text is None:
        log_text="select all from database"
        
        
    #pd.read_sql
    all_data = pd.read_sql(sql, con=db_class.db)
    
    for i, eachrow in all_data.iterrows():
        count = 3
        if not eachrow['1차리뷰']:
            count-=1
        if not eachrow['2차리뷰']:
            count-=1
        if not eachrow['3차리뷰']:
            count-=1

        sql = "UPDATE SWDR_DB.Project SET 진행율 = '%s' WHERE 프로젝트명 = '%s'" %( "{:.1f}".format(count*1/3*100), eachrow['프로젝트명'])
        db_class.execute(sql)
    
    db_class.commit()

    sql      = "SELECT * \
                FROM SWDR_DB.Project"
    row      = db_class.executeAll(sql)
                
        
    return render_template('/main/project.html',
                            log=log_text,
                            resultData=row
                            )
    
# INSERT 함수 예제
@main.route('/project/insert', methods=["GET", "POST"])
def insert():
    db_class = dbModule.Database()
    get_data={}
    
    if request.method=="POST":
        get_data = request.form
        print("form 입력: ", get_data)
        date_tok = get_data['양산일'].split('-')
        sop_date = datetime.datetime(int(date_tok[0]), int(date_tok[1]), int(date_tok[2]))
        review_date = sop_date - datetime.timedelta(days=80)
        review = str(review_date.year) + '-' + str(review_date.month) + '-' + str(review_date.day)
        print(review)
        
    try:
        if get_data['프로젝트명'] =='':
            raise "NULL"
        
       
        
        sql = "INSERT INTO `SWDR_DB`.`Project` (`프로젝트명`, `플랫폼`, `양산일` ,`담당자`, `업체`, `모델`, `번들대표차종`, `비고`, `리뷰계획`) VALUES ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s')" \
            % (get_data['프로젝트명'], get_data['플랫폼'], get_data['양산일'], get_data['담당자'], get_data['업체'], get_data['모델'], get_data['번들대표차종'], get_data['비고'], review)
        
        print(sql)
        msg=db_class.execute(sql)
        
        db_class.commit()
        
        if msg is not None:
            render = select(msg)
        else:
            render = select(sql)
        
    except:
        print("프로젝트명이 비워져 있어요.")
        render=select("테이블에 넣기 실패: 프로젝트명이 비워져 있어요.")
    
    return render

@main.route('/project/delete', methods=["GET", "POST"])
def delete():
    db_class = dbModule.Database()
    sql      = "SELECT * \
                FROM SWDR_DB.Project"
    
    #pd.read_sql
    all_data = pd.read_sql(sql, con=db_class.db)
    selected=[]
    selected = request.form.getlist("check")
    
    selected.reverse()
    print(selected)
    #print(all_data)
    
    log = ''
    
    if len(selected) > 0:
        for i in (selected):
            sql = "DELETE FROM SWDR_DB.Project WHERE `프로젝트명` = ('%s')"%(all_data[all_data.index==int(i)]['프로젝트명'].values[0])
            print(i, sql)
            db_class.execute(sql)
            log += sql +", "
            
    db_class.commit()
    render = select(log)
    return render


@main.route('/project/fileupload', methods=["GET", "POST"])
def upload_file():
    db_class = dbModule.Database()
    sql      = "SELECT * \
                FROM SWDR_DB.Project"
    
    #pd.read_sql
    all_data = pd.read_sql(sql, con=db_class.db)
    selected=[]
    selected = request.form.getlist("check")
    
    selected.reverse()
    print(selected)
    print(all_data)
    
    log = '체크한 후 저장을 눌러주세요.'
    render = select(log)
    
    if request.method == "POST":
        f=request.files
        
        if len(selected) > 0:
            log = ''
            for i in (selected):
                f1 = f.getlist('1st_file')
                f2 = f.getlist('2nd_file')
                f3 = f.getlist('3rd_file')
                
                if f1[int(i)].filename:
                    print("f1", f1[int(i)])
                    
                    location = "/home/joker1251/Desktop/"+f1[int(i)].filename
                    f1[int(i)].save("/home/joker1251/Desktop/"+secure_filename(f1[int(i)].filename))
                    sql = "UPDATE SWDR_DB.Project SET 1차리뷰 = '%s' WHERE 프로젝트명 = '%s'" %(location, all_data[all_data.index==int(i)]['프로젝트명'].values[0])
                    db_class.execute(sql)
                    log += sql +", "
                
                if f2[int(i)].filename:
                    print("f2", f2[int(i)])
                    location = "/home/joker1251/Desktop/"+f2[int(i)].filename
                    f2[int(i)].save("/home/joker1251/Desktop/"+secure_filename(f2[int(i)].filename))
                    sql = "UPDATE SWDR_DB.Project SET 2차리뷰 = '%s' WHERE 프로젝트명 = '%s'" %(location, all_data[all_data.index==int(i)]['프로젝트명'].values[0])
                    db_class.execute(sql)
                    log += sql +", "
                
                if f3[int(i)].filename:
                    print("f3", f3[int(i)])
                    location = "/home/joker1251/Desktop/"+f3[int(i)].filename
                    f3[int(i)].save("/home/joker1251/Desktop/"+secure_filename(f3[int(i)].filename))
                    sql = "UPDATE SWDR_DB.Project SET 3차리뷰 = '%s' WHERE 프로젝트명 = '%s'" %(location, all_data[all_data.index==int(i)]['프로젝트명'].values[0])
                    db_class.execute(sql)
                    log += sql +", "
                
                
    db_class.commit()
    render = select(log)            
    return render