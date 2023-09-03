from flask import Flask
from src.ipo_details import Ipo
import logging
logging.basicConfig(level=logging.INFO)


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
    logging.info("[1] Send mail route has been triggered from github action")
    ipo.handler()
    return ""


if __name__ == "__main__":
    app.run(port=3000, debug=False)
