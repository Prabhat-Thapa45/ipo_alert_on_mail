from flask import Flask
from src.ipo_details import Ipo


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

@app.route('/', methods=['GET'])
def index():
    return "welcome to ipo alerts"


@app.route('/send_mail')
def send_mail():
    ipo.handler()
    return "hello"


if __name__ == "__main__":
    app.run(port=3000, debug=False)
