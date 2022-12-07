from App import app_init

app = app_init()

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8888, load_dotenv=True)