# 代码生成时间: 2025-10-12 02:16:24
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPInternalServerError
import json


# 定义一个薪资计算器的类
class SalaryCalculator:
    def __init__(self, base_salary):
        self.base_salary = base_salary

    def calculate(self, hours_worked, rate_per_hour):
        """
        计算薪资
        :param hours_worked: 工作小时数
        :param rate_per_hour: 每小时费率
        :return: 计算后的薪资
        """
        try:
            total_hours = float(hours_worked)
            rate_per_hour = float(rate_per_hour)
            return total_hours * rate_per_hour
        except ValueError:
            raise ValueError("Invalid input values for hours_worked and rate_per_hour")


# Pyramid视图函数
@view_config(route_name='calculate_salary', renderer='json')
def calculate_salary(request):
    """
    计算薪资视图函数
    :param request: Pyramid请求对象
    :return: JSON响应包含计算结果
    """
    try:
        # 获取请求参数
        base_salary = request.params.get('base_salary')
        hours_worked = request.params.get('hours_worked')
        rate_per_hour = request.params.get('rate_per_hour')

        # 创建薪资计算器实例
        calculator = SalaryCalculator(base_salary)

        # 调用计算方法
        result = calculator.calculate(hours_worked, rate_per_hour)

        # 返回JSON响应
        return {
            'status': 'success',
            'result': result
        }
    except ValueError as e:
        # 错误处理
        return Response(json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json', status=400)
    except Exception as e:
        # 内部服务器错误处理
        raise HTTPInternalServerError("Error calculating salary: " + str(e))


# Pyramid配置函数
def main(global_config, **settings):
    """
    Pyramid配置函数
    :param global_config: 全局配置对象
    :param settings: 应用设置
    """
    config = Configurator(settings=settings)
    config.add_route('calculate_salary', '/calculate_salary')
    config.scan()
    return config.make_wsgi_app()

# 运行程序（用于测试）
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None, **{'reload': True})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()