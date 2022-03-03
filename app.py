from flask import Flask, render_template, request, make_response
app = Flask(__name__)

import json # 쿠키는 기본적으로 문자열입니다. json은 ajax에서 문자열을 배열로 전환해 받기 위해서 필요한 기능입니다.

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/basket', methods=['GET'])
def basket():
   return render_template('basket.html')


@app.route('/set_basket', methods=['POST', 'GET'])
def set_basket():
   if request.method == 'POST':
      basket_receive = request.form.getlist('basket_give') # ajax에서 배열을 받기 위해서는 request의 getlist 메소드를 사용합니다.
      basket = make_response()
      basket.set_cookie('basket', json.dumps(basket_receive))  # 쿠키로 들어갈 값으로는 리스트를 쓰지 못합니다. 문자열으로 자료형을 바꿔줘야 합니다.
      return basket
   # basket 값을 반환해야 쿠키에 데이터가 담깁니다.
   # 참조: set_cookit() 메소드의 인수에 expire를 넣어주고 DateTime 라이브러리를 활용하면 만료되는 기간을 정확히 정해줄 수 있다고 하네요.

@app.route('/get_basket', methods=['GET'])
def get_basket():
   resp = request.cookies.get('basket')
   basket = json.loads(resp) # json.loads() 메소드를 사용하여 문자열로 전환된 쿠키를 리스트로 전환합니다. json.load()와 헷갈리지 않게 조심하세요.
   return {'basket': basket} # 리스트형 자료는 ajax로 보내지 못합니다. 딕셔너리화 시켜줘야 합니다.

@app.route('/remove_basket', methods=['POST', 'GET']) # POST로만 작동하게 만들어 둡니다.
def remove_basket():
   if request.method == 'POST':
      basket = make_response()
      basket.set_cookie('basket', '', expires=0) # basket 쿠키의 만료시간을 0으로 만들어 내용물을 None으로 만듭니다.
      return basket

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)