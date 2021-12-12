from flask import Flask,jsonify,render_template,request,send_from_directory,flash,redirect,url_for
from supabase_py import create_client, Client
import os
import json
import requests
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET")

load_dotenv()

def get_supabase_client():
    try:
        url: str = os.environ.get("SUPABASE_TEST_URL")
        key: str = os.environ.get("SUPABASE_TEST_KEY")
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        return render_template('error.html',error=str(e))

def get_all_pastes():
    supabase=get_supabase_client()
    data = supabase.table('paste_bin_data').select("*").execute()
    return data



@app.route('/insert',methods = ['POST'])
def insert():
    try:
        if request.method == 'POST':
            form_data = request.form.to_dict()
            print(form_data)
            if len(form_data['code'].strip())==0:
                flash("Please write some text/code")  
                return redirect(url_for('home_page'))
            else:  
                supabase=get_supabase_client()
                #data = supabase.table('paste_bin_data').select('*').execute()
                if not request.headers.getlist("X-Forwarded-For"):
                    ip = request.remote_addr
                else:
                    ip = request.headers.getlist("X-Forwarded-For")[0]

                ins_data={
                    "platform": request.user_agent.platform,
                    "browser" : request.user_agent.browser,
                    "ip" : str(ip),
                    "data": form_data['code']

                }
                data = supabase.table('paste_bin_data').insert(ins_data).execute()
                print(data)
                flash("Code added successfully")
                return redirect(url_for('home_page'))
                
    except Exception as e:
        return render_template('error.html',error=str(e))

@app.route('/')
def home_page():
    data=get_all_pastes()
    print(data)
    return render_template('home.html',paste=data['data'])
	

if __name__ == '__main__':

    app.run()