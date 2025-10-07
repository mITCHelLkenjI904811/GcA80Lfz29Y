# 代码生成时间: 2025-10-07 16:27:53
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response

# 定义智能家居设备类
class SmartHomeDevice:
    def __init__(self, name):
        self.name = name

    def turn_on(self):
        # 模拟设备开启
        return f"{self.name} turned on."

    def turn_off(self):
        # 模拟设备关闭
        return f"{self.name} turned off."

# 定义智能家居控制器类
class SmartHomeController:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def control_device(self, device_name, action):
        for device in self.devices:
            if device.name == device_name:
                if action == 'on':
                    return device.turn_on()
                elif action == 'off':
                    return device.turn_off()
                else:
                    return f"Invalid action for {device_name}."
        return f"Device {device_name} not found."

# Pyramid视图函数
@view_config(route_name='smart_home_control', renderer='json')
def smart_home_control(request):
    # 创建智能家居控制器实例
    controller = SmartHomeController()

    # 添加设备
    controller.add_device(SmartHomeDevice('Light'))
    controller.add_device(SmartHomeDevice('Thermostat'))

    # 获取请求参数
    device_name = request.params.get('device')
    action = request.params.get('action')

    # 控制设备
    response = controller.control_device(device_name, action)

    # 返回响应
    return {'message': response}

# 配置Pyramid应用
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('smart_home_control', '/control')
    config.scan()
    return config.make_wsgi_app()
