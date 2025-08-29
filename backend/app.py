from flask import Flask, request, jsonify, make_response, abort
from flask_cors import CORS
import urllib.parse
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

MASTER_NOTES_CONTENT = """大神遞給你一張泛黃的筆記，上面寫著：
「資安之路，道阻且長。唯有不斷學習，方能窺得其奧秘。
此為我多年心得，望你善用：
token: %47%4f%41%54
記住，真正的力量不在於工具，而在於對知識的渴望與實踐。還有 Be a goodhacker :)。
"""

@app.route('/')
def index():
    return "AIS3 Challenge Backend is running!"

@app.route('/get_master_notes', methods=['GET'])
def get_master_notes():
    return make_response(jsonify({"notes": MASTER_NOTES_CONTENT}))

@app.route('/check_option_status', methods=['GET'])
def check_option_status():
    ais3_token_encoded = request.cookies.get('ais3_token')
    show = False
    if ais3_token_encoded:
        try:
            if urllib.parse.unquote(ais3_token_encoded) == "GOAT":
                show = True
        except Exception:
            pass
    return jsonify({"show_option_3": show})

@app.route('/goodhacker', methods=['GET'])
def good_hacker():
    ais3_token_encoded = request.cookies.get('ais3_token')
    try:
        if not ais3_token_encoded or urllib.parse.unquote(ais3_token_encoded) != "GOAT":
            abort(404)
    except Exception:
        abort(404)

    url_to_fetch = request.args.get('url')
    if not url_to_fetch:
        response_message = """恭喜你變成大神！......恩？但flag呢？
/api/goodhacker 似乎會去幫你 fetch 某個網址的內容，只是你給的網址要夠『內行』才行  在flag.txt
"""
        return jsonify({"status": "hint", "message": response_message})

    print(f"Backend: /goodhacker - Attempting to SSRF fetch URL: {url_to_fetch}")
    try:
        response = requests.get(url_to_fetch, timeout=5)
        content = f"成功為你從 {url_to_fetch} 獲取資源內容：\n\n{response.text}"
        return jsonify({"status": "success", "message": content})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"讀取遠端資源時發生錯誤: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
