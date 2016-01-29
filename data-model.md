# Mongo Data Model

## User
##### Object
```
User {
    _id: <UserObjectID>,
    username: String,
    nickname: String,
    password: String,
    role: [{
        type: Integer,
        ...    
    }...],
    locked: Boolean,
    [social: {
        [github: {...}],
        [wechat: {...}],
        [google: {...}],
        [email: String],
        [website: String],
        [phone: String],
        ...
    }],
    score: {
        rank: Integer
        ...
    },
    [gender: String],
    [avatar: String],
    register_time: Timestamp,
    [description: String],
    fans_count: Integer,
    follow_count: Integer,
    post_count: Integer,
    tag_count: Integer,
    [tag_list: <TagObjectID>[]],
    last_login_time: Timestamp,
    last_login_ip: String
}
```
##### Default
```
User.locked: Boolean = false
User.score.rank: Integer = 0
User.fans_count: Integer = 0
User.follow_count: Integer = 0
User.post_count: Integer = 0
User.tag_count: Integer = 0
```
##### Enum
```
User.role: Integer {
    0 = admin,
    1 = user
}
```
## Post
##### Object
```
Post: Object {
    _id: <PostObjectID>,
    author: <UserObjectID>,
    type: Integer,
    create_time: Timestamp,
    modify_time: Timestamp,
    title: String,
    content: String,
    tag_list: <TagObjectID>[],
    up_count: Integer,
    down_count: Integer,
    mark_count: Integer,
    visit_count: Integer,
    commentable: Boolean,
    locked: Boolean,
    [history_list: PostHistory[
        PostHistory: Object {
            insert_time: Timestamp,
            title: String,
            content: String,
            tag_list: <TagObjectID>[]
        }
        ...
    ]]
    [parent: Post]
}
```
##### Default
```
Post.up_count: Integer = 0
Post.down_count: Integer = 0
Post.mark_count: Integer = 0
Post.visit_count: Integer = 1
Post.commentable: Boolean = true
Post.locked: Boolean = false
```
##### Enum
```
Post.type: Integer {
    0 = artical
    1 = comment
}
```
##### CURD Remark
###### Insert
```
Insert Post.tag_list to Tag for any new tag
Update Tag.post_count += 1 for any existed tag in Post.tag_list
Update User.post_count += 1 where Uset._id = Post.author
```
###### Update
```
Query previous post from Post with Post._id
Turncate queried post to PostHistory
Insert PostHistory to Post with Post._id
Update Post with Post._id
```
## Tag
##### Object
```
Tag: Object {
    _id: <TagObjectID>,
    name: String,
    user_count: Integer,
    post_count: Integer,
    locked: Boolean,
    [user_list: <UserObjectID>[]],
    [post_list: <PostObjectID>[]]
}
```
##### Default
```
Tag.user_count: Integer = 0
Tag.post_count: Integer = 1
Tag.locked: Boolean = false
```
##### CURD Remark
###### Delete
```
Delete from Post.tag_list where Post.tag_list contains Tag._id
Delete from User.tag_list where User.tag_list contains Tag._id
```
## Mark
##### Object
```
Mark: Object {
    _id: <MarkObjectID>,
    user: <UserObjectID>,
    post: <PostObjectID>,
    type: Integer, 
    mark_time: Timestamp,
}
```
##### Enum
```
Mark.type: Integer {
    0 = up,
    1 = down
    2 = mark,
}
```
##### CURD Remark
###### Create
- Create regarding type
```
When Mark.type = 0, update Post.up_count += 1 where Mark.post == Post._id
When Mark.type = 1, update Post.down_count += 1 where Mark.post == Post._id
When Mark.type = 2, update Post.mark_count += 1 where Mark.post == Post._id
```
###### Delete
- Delete regarding type
```
When Mark.type = 0, update Post.up_count -= 1  where Mark.post == Post._id
When Mark.type = 1, update Post.down_count -= 1 where Mark.post == Post._id
When Mark.type = 2, update Post.mark_count -= 1 where Mark.post == Post._id
```
## Relation
##### Object
```
Relation: Object {
    _id: <RelationObjectID>,
    type: Integer,
    source: <UserObjectID>,
    target: <UserObjectID>
}
```
##### Enum
```
Relation.type: Integer {
    0 = follow
}
```
##### CURD Remark
###### Create
```
Update User.follow_count += 1 where User._id = Relation.source_id
Update User.fans_couont += 1 where User._id = Relation.target_id
```
###### Delete
```
Update User.follow_count -= 1 where User._id = Relation.source_id
Update User.fans_couont -= 1 where User._id = Relation.target_id
```



