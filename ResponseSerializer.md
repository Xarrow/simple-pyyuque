
## UserSerializer

一般在列表的场景返回的用户信息。

|属性|类型|示例|说明|
|---|-----|----|----|
|id|int|104023||
|type|str|User||
|space_id|int|0||
|account_id|int|10838||
|login|str|helixcs||
|name|str|Helixcs||
|avatar_url|str|https://cdn.nlark.com/yuque/0/2018/png/104023/1539315567419-aad17f80-8365-4a08-af1e-e301a3c2c7f5.png||
|large_avatar_url|str|https://cdn.nlark.com/yuque/0/2018/png/104023/1539315567419-aad17f80-8365-4a08-af1e-e301a3c2c7f5.png?x-oss-process=image/resize,m_fill,w_320,h_320||
|medium_avatar_url|str|https://cdn.nlark.com/yuque/0/2018/png/104023/1539315567419-aad17f80-8365-4a08-af1e-e301a3c2c7f5.png?x-oss-process=image/resize,m_fill,w_160,h_160||
|small_avatar_url|str|https://cdn.nlark.com/yuque/0/2018/png/104023/1539315567419-aad17f80-8365-4a08-af1e-e301a3c2c7f5.png?x-oss-process=image/resize,m_fill,w_80,h_80||
|books_count|int|3||
|public_books_count|int|2||
|followers_count|int|3||
|following_count|int|3||
|public|int|1||
|description|str|Java 糊口，Python 兴趣||
|created_at|str|2018-04-23T02:43:33.000Z||
|updated_at|str|2018-12-07T17:00:03.000Z||
|_serializer|str|v2.user_detail||

详细文档参考：[https://www.yuque.com/yuque/developer/userserializer](https://www.yuque.com/yuque/developer/userserializer)


-----
##DocSerializer

文档基本信息，一般用在列表场景。

|属性|类型|示例|说明|
|---|-----|----|----|
|id|int|1040104||
|slug|string|kksbh7||
|title|string|Untitled||
|description|string|||
|user_id|int|104023||
|book_id|int|186611||
|format|string|asl||
|public|int|1||
|status|int|0||
|likes_count|int|0||
|comments_count|int|0||
|content_updated_at|string|2018-12-09T10:44:00.000Z||
|created_at|string|2018-12-09T10:44:00.000Z||
|updated_at|string|2018-12-09T10:44:00.000Z||
|published_at|None|None||
|draft_version|int|0||
|last_editor_id|int|104023||
|word_count|int|0||
|last_editor|<UserSerializer>|||
|book|<BookSerializer>|||
|_serializer|string|v2.doc||


详细文档参考：[https://www.yuque.com/yuque/developer/docserializer](https://www.yuque.com/yuque/developer/docserializer)


----
BookSerializer
一般在列表的场景返回的仓库信息。

|属性|类型|示例|说明|
|---|-----|----|----|

|id|int|186611||
|type|string|Book||
|slug|string|dyrs3g||
|name|string|test_repo||
|user_id|int|221642||
|description|string|test_repo_des||
|creator_id|int|104023||
|public|int|0||
|items_count|int|4||
|likes_count|int|0||
|watches_count|int|1||
|content_updated_at|string|2018-12-09T12:08:47.894Z||
|updated_at|string|2018-12-09T12:08:47.000Z||
|created_at|string|2018-12-08T14:12:50.000Z||
|namespace|string|rn15gw/dyrs3g||
|user|<UserSerializer>|||
|_serializer|string|v2.book||

详细文档参考：[https://www.yuque.com/yuque/developer/bookserializer](https://www.yuque.com/yuque/developer/bookserializer)