from syt.app import create_app

# 使用开发环境
app = create_app('development')

if __name__ == '__main__':
    app.run()
