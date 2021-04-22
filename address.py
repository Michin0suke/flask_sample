from flask import Flask, render_template, request, redirect, url_for
import sqlite3

DATABASE_NAME = 'address.db'
app = Flask(__name__)


# [ヘルパ関数] SQLを実行する
def execute_sql(sql):
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    result = []
    
    for row in cur.execute(sql):
        result.append(row)

    con.commit()
    con.close()

    return result


# [ヘルパ関数] SELECT文で帰ってきたデータの配列を連想配列に変換する
# ※ データベース構造に依存する
def convert_addresses(raw_row):
    return ({
        'id': raw_row[0],
        'name': raw_row[1],
        'name_ruby': raw_row[2],
        'address': raw_row[3],
        'memo': raw_row[4]
    })


# データ一覧（トップページ）
@app.route('/', methods=['GET'])
def show():
    user_data = []

    for data in execute_sql('SELECT id, name, name_ruby, address, memo FROM addresses'):
        user_data.append(convert_addresses(data))

    return render_template('index.html', user_data=user_data)


# [処理] データ挿入
@app.route('/', methods=['POST'])
def insert():
    name = request.form['name']
    name_ruby = request.form['name_ruby']
    address = request.form['address']
    memo = request.form['memo']

    execute_sql(f'INSERT INTO addresses (name, name_ruby, address, memo) VALUES ("{name}", "{name_ruby}", "{address}", "{memo}")')

    return show()


# 詳細ページ
@app.route('/detail', methods=['POST'])
def detail():
    id = request.form['id']
    # 1行だけしか返らないはずなので、[0]を指定しておく（こんなイメージ: [[1,2,3]] → [1,2,3]）
    row_raw = execute_sql(f'SELECT * FROM addresses WHERE id = {id}')[0]
    data = convert_addresses(row_raw)

    return render_template('detail.html', data=data)


# [処理] データ削除
@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    execute_sql(f'DELETE FROM addresses WHERE id = {id}')

    return redirect(url_for('show'))


# [処理] データ更新
@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    name_ruby = request.form['name_ruby']
    address = request.form['address']
    memo = request.form['memo']

    execute_sql(f'UPDATE addresses SET name = "{name}", name_ruby = "{name_ruby}", address = "{address}", memo = "{memo}" WHERE id = {id}')

    return redirect(url_for('show'))
