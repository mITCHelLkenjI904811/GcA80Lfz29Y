# 代码生成时间: 2025-09-18 17:57:23
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import json

# 假设的用户数据库
USER_DATABASE = {
    "admin": "admin123"
}

class UserAuthSystem:
    """用户登录验证系统"""

    @staticmethod
    def verify_user(username, password):
        """验证用户登录信息是否正确"""
        return USER_DATABASE.get(username) == password

    @staticmethod
    def login(request):
        """处理登录请求"""
        # 从请求中获取用户名和密码
        data = request.json_body
        username = data.get("username")
        password = data.get("password")
        
        # 验证用户信息
        if not username or not password:
            return Response(json.dumps({"error": "Missing username or password"}), 
                           content_type='application/json')
        
        is_authenticated = UserAuthSystem.verify_user(username, password)
        
        # 根据验证结果返回不同的响应
        if is_authenticated:
            return Response(json.dumps({"message": "Login successful"}), 
                           content_type='application/json')
        else:
            return Response(json.dumps({"error": "Invalid username or password"}), 
                           content_type='application/json')

# 配置Pyramid应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 添加路由和视图函数
    config.add_route('login', '/login')
    config.add_view(UserAuthSystem.login, route_name='login', renderer='json')
    
    # 扫描当前目录下的所有配置类
    config.scan()
    
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()