import nepali_datetime
from flask import Flask, render_template, request, redirect, url_for
from src.ipo_api import Ipo


app = Flask(__name__)
ipo = Ipo()

# @app.route('/', methods=['GET'])
# def index():
#     try:
#         return render_template(
#             "ipo.html",
#             ipos=ipo.data,
#             date_today=nepali_datetime.datetime.today().strftime('%y-%B-%d')
#         )
#     except Exception as e:
#         return f"{e} occured"


@app.route('/send_mail')
def send_mail():
    ipo.call_send_mail()
    return ""


if __name__ == "__main__":
    app.run(port=3000, debug=True)
