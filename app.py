from flask import Flask,request,jsonify,abort
import dbm
from janome.tokenizer  import Tokenizer
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/')#これにアクセスした際に起動される
def root():#これはなんでもいい
    return '<h1>hello World!<h1>'
@app.route('/oit')
def oit():
    return '<h1>Robotics and Design!<h1>'
@app.route('/greet/<name>')
def greet(name):
    return f'Hello {name}!'

def wakachi(s):
    t = Tokenizer()
    words = t.tokenize(s,wakati = True) 
    ret = ""
    for w in words:
        ret += w + '/'
    return ret
        
@app.route('/v1/messages',methods=['POST'])
def post():
    
    date = request.get_json()
    print(date['message'])
    with dbm.open('message.dbm','c') as db:#ファイル名,'Cはクリエイト'
        if 'id' not in db:#idがなかったらin 
            db['id'] = str(0)
        id = int(db['id'])
        id += 1
        db['id'] = str(id)
        db[str(id)] = wakachi(date['message'])
    return jsonify({'id':id})
@app.route('/v1/messages',methods=['GET'])
def get_all():
    msgs = []
    with dbm.open('message.dbm','c') as db:#ファイル名,'Cはクリエイト'
        for k in db.keys():
            if k == b'id':continue
            msgs.append(db[k].decode('utf-8'))
    print(msgs)   
    return jsonify(msgs)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)