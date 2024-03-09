<!-- 项目标志 -->
<div align="center">

  <h3 align="center">flect</h3>
  <p align='center'>
    <em>Turning ideas into web app fast.</em>
  </p>
  <p align="center">
    <a href="https://github.com/Chaoyingz/flect/actions?query=workflow" target="_blank">
        <img src="https://github.com/Chaoyingz/flect/actions/workflows/test.yaml/badge.svg?event=push&branch=main" alt="Test">
    </a>
    <a href="https://pypi.python.org/pypi/flect" target="_blank">
        <img src="https://img.shields.io/pypi/v/flect.svg" alt="pypi">
    </a>
    <a href="https://github.com/Chaoyingz/flect" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/flect.svg" alt="versions">
    </a>
    <a href="https://github.com/Chaoyingz/flect/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/chaoyingz/flect.svg" alt="license">
    </a>
  </p>
  <p align="center">
    快速将想法转化为 Web 应用。
    <br />
    <a href="https://flect.celerforge.com/"><strong>探索文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Chaoyingz/flect/issues">报告错误</a>
    ·
    <a href="https://github.com/Chaoyingz/flect/issues">请求新功能</a>
    ·
    <a href="https://github.com/Chaoyingz/flect/">English</a>
  </p>
</div>

<!-- flect 是什么 -->

## flect 是什么

flect 是一个用于构建全栈 Web 应用程序的 Python 框架。它通过在后端使用与前端 React 组件属性相对应的 Pydantic 模型来构建用户界面。
这种集成允许开发者利用 Python 快速开发具有交互性和美观的用户界面。

主要特性包括：

- **快速开发**：使用 Python 编写整个应用，无缝集成后端逻辑和前端 UI。
- **简单的表单验证**：定义单一的 Pydantic 模型，实现整个应用中的无缝且一致的表单验证，提高开发速度，减少潜在错误。
- **基于文件夹的路由**：通过文件夹结构轻松管理路由。
- **客户端路由**：无需重新加载即可实现快速、流畅的页面转换。
- **SEO 友好**：支持服务器端渲染，以获得更好的搜索引擎可见性。

您也可以访问[文档网站](https://flect.celerforge.com/docs/introduction/)，该网站完全使用 flect 构建，并通过 [Vercel](https://vercel.com/) 部署，源代码可以在[这里](https://github.com/Chaoyingz/flect/tree/main/docs)找到。

## 为什么使用 flect ?

flect 利用 Python 代码开发 web 应用程序的用户界面，带来了几个好处：

> 如果你是 Python 开发者 —— 你可以使用 React 构建响应式 web 应用程序，而无需编写任何 JavaScript 代码或接触 npm。
>
> 如果你是前端开发者 —— 你可以专注于构建真正可复用的神奇组件，无需为每个视图复制粘贴组件。
>
> 对于每个人来说 —— 真正的关注点分离，后端定义整个应用程序；而前端自由地只实现用户界面。
>
> — _来自 FastUI_

## 示例

在这个例子中，我们将演示如何使用 flect 构建一个简单的待办事项应用程序。由于 flect 是建立在 [FastAPI](https://fastapi.tiangolo.com/) 之上的，因此您可以使用 FastAPI 的语法定义路由。

注意：在实际的 flect 应用程序中，为了更好的组织，将 page 路由和 post 路由会定义在不同的文件中。

以下是一个简单的待办事项应用程序。

```python
import json
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from flect import PageResponse, ActionResponse
from flect import components as c
from flect import form as f
from flect.actions import Notify

# 定义一个创建新待办事项的模型，只有一个 'task' 字段
class TodoInCreate(BaseModel):
    task: str = f.Input(placeholder="Enter task...")

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
![flect-todo](https://github.com/Chaoyingz/flect/assets/32626585/f48415d8-b25c-432d-8dc4-d0bd4d65777d)

## 了解更多

- [文档](https://flect.celerforge.com/)

## 鸣谢

本项目受到以下框架的启发：

- [FastUI](https://github.com/pydantic/FastUI)
- [Next.js](https://nextjs.org/)

## 证书

这个项目遵守 MIT 许可证.
