# Simple-PyYuQue

![img](https://gw.alipayobjects.com/zos/rmsportal/cptBhNjKeyaBDrfnMKwC.svg)

一个非官方的 [“语雀”](http://yuque.com) 的Python API 封装。提供和官方 API 类似的调用方式。设计简单高效。
详细文档说明参考[https://www.yuque.com/yuque/developer/api](https://www.yuque.com/yuque/developer/api)

----
# 安装
TODO

----
# 快速开始

### 1. 实例化

```python
spyq = SimplePyYuQueAPI(token="token", app_name="py_yuque")

```
其中 `token` 是在语雀中开发者 setting -> token 中申请 ， `app_name` 为你的应用名称。

### 2. User 资源访问

* 获取认证的用户的个人信息

```python

spyq = SimplePyYuQueAPI(token="token", app_name="py_yuque")
u = spyq.User()
user_serializer = u.get_user()

```

或许你可以更加简洁一点

```python
user_serializer = SimplePyYuQueAPI(token="token", app_name="py_yuque1").User().get_user()

```

你还可以打印出原始报文
```python
print(user_serializer.base_response)
```

* 基于用户 login 或 id 获取一个用户的基本信息。
```python
user = SimplePyYuQueAPI(token="token", app_name="py_yuque").User()
print("==> Helixcs is %s", user.get_users(login="Helixcs").base_response)

#
```

详细API参考官方文档：[https://www.yuque.com/yuque/developer/user](https://www.yuque.com/yuque/developer/user)

----
# API 说明

----
# 问题排查

TODO：

----
# LICENSE

MIT


