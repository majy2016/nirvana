from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    goods_list = ["756022"]
    

    return 'HaHa --------------------'


if __name__ == '__main__':
    app.run()