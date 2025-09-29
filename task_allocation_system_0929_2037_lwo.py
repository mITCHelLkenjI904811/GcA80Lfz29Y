# 代码生成时间: 2025-09-29 20:37:58
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 定义数据库连接
DATABASE_URL = 'sqlite:///task_allocation.db'

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
Session = sessionmaker(bind=engine)

# 定义模型基类
Base = declarative_base()

# 定义任务分配模型
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    assigned_to = Column(String(255), nullable=True)

    def __repr__(self):
        return f"Task(title='{self.title}', assigned_to='{self.assigned_to}')"

# 创建数据库表
Base.metadata.create_all(engine)

# 设置配置器
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        # 扫描视图
        config.scan()
        # 添加路由
        config.add_route('home', '/')
        config.add_route('add_task', '/add_task')
        config.add_route('assign_task', '/assign_task')

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    session = Session()
    tasks = session.query(Task).all()
    return {'tasks': tasks}

@view_config(route_name='add_task', renderer='templates/add_task.pt')
def add_task_view(request):
    title = request.params.get('title')
    description = request.params.get('description')
    session = Session()
    if title and description:
        task = Task(title=title, description=description)
        session.add(task)
        session.commit()
        return HTTPFound(location='/')
    return {'error': 'Please fill in the title and description fields.'}

@view_config(route_name='assign_task', renderer='templates/assign_task.pt')
def assign_task_view(request):
    task_id = int(request.params.get('task_id'))
    assigned_to = request.params.get('assigned_to')
    session = Session()
    if task_id and assigned_to:
        task = session.query(Task).filter(Task.id == task_id).one()
        task.assigned_to = assigned_to
        session.commit()
        return HTTPFound(location='/')
    return {'error': 'Please select a task and assignee.'}

# 定义模板文件
# templates/home.pt
# templates/add_task.pt
# templates/assign_task.pt