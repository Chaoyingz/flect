<!-- 项目标志 -->
<div align="center">

  <h3 align="center">tui framework</h3>

  <p align="center">
    快速将想法转化为 Web 应用。
    <br />
    <a href="https://tui.celerforge.com/"><strong>探索文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Chaoyingz/tui/">English</a>
    ·
    <a href="https://github.com/Chaoyingz/tui/issues">报告错误</a>
    ·
    <a href="https://github.com/Chaoyingz/tui/issues">请求新功能</a>
  </p>
</div>

<!-- tui 是什么 -->

## tui 是什么

tui 是一个用于构建全栈 Web 应用程序的 Python 框架。它通过在后端使用与前端 React 组件属性相对应的 Pydantic 模型来构建用户界面。
这种集成允许开发者利用 Python 快速开发具有交互性和美观的用户界面。

主要特性包括：

- **快速开发**：使用 Python 编写整个应用，无缝集成后端逻辑和前端 UI。
- **SEO 友好**：支持服务器端渲染，以获得更好的搜索引擎可见性。
- **客户端路由**：无需重新加载即可实现快速、流畅的页面转换。
- **基于文件夹的路由**：通过文件夹结构轻松管理路由。
- **简单的表单验证**：定义单一的 Pydantic 模型，实现整个应用中的无缝且一致的表单验证，提高开发速度，减少潜在错误。

## 系统要求

- Python 3.9+

## 安装

```console
$ pip install tuiframework

---> 100%
```

## 示例

- 下面展示了一个简单的待办事项应用。

```python
import json
from typing import Annotated, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tui import PageResponse
from tui import components as c
from tui import form as f
from tui.actions import Notify
from tui.response import ActionResponse

# 定义一个创建新待办事项的模型，只有一个 'task' 字段
class TodoInCreate(BaseModel):
    task: Annotated[str, f.Input(placeholder="Enter task...")]

# 定义存储在数据库中的待办事项模型，扩展创建模型添加 'id' 和 'completed' 字段
class TodoInDB(TodoInCreate):
    id: int
    completed: Optional[bool] = False

# 初始化一个待办事项列表
todos = [
    TodoInDB(id=1, task="Task 1", completed=False),
    TodoInDB(id=2, task="Task 2", completed=True),
    TodoInDB(id=3, task="Task 3", completed=False),
]

# 定义要显示的页面
async def page() -> PageResponse:
    return PageResponse(
        element=c.Container(
            # 支持 tailwind css
            class_name="container mx-auto px-32 py-10",
            children=[
                # 在页面上添加标题
                c.Heading(
                    level=1,
                    text="Todo App",
                    class_name="text-3xl mb-10",
                ),
                # 添加创建新待办事项的表单
                c.Form(
                    model=TodoInCreate,
                    submit_url="/",
                    class_name="mb-5 border p-5",
                ),
                # 添加显示所有待办事项的表格
                c.Table(
                    datasets=todos,
                    class_name="border p-5",
                )
            ]
        )
    )

# 定义 todo 表单处理逻辑
async def post(form: TodoInCreate) -> ActionResponse:
    todos.append(
        TodoInDB(
            id=len(todos) + 1,
            task=form.task,
            completed=False,
        )
    )
    # 返回一个包含提交的表单值的通知
    return ActionResponse(
        action=Notify(
            title="You submitted the following values:",
            description=json.dumps(jsonable_encoder(form), indent=2),
        )
    )
```

渲染出来的效果如下：
![tui-todo](https://github.com/Chaoyingz/tui/assets/32626585/f48415d8-b25c-432d-8dc4-d0bd4d65777d)

## 演示

请查看项目仓库中的 `docs` 文件夹。文档网站直接从这些源文件构建。

## 证书

这个项目遵守 MIT 许可证.
