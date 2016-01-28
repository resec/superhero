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
    title: String,
    content: String,
    tag_list: <TagObjectID>[],
    up_count: Integer,
    down_count: Integer,
    mark_count: Integer,
    visit_count: Integer,
    commentable: Boolean,
    initial: Boolean,
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
```
##### Enum
```
Post.type: Integer {
    0 = artical
    1 = comment
}
```
## PostHistory
##### Object
```
PostHistory {
    _id: <PostHistoryObjectID>,
    from: <PostObjectID>,
    to: <PostObjectID>,
    initial: <PostObjectID>
}
```
##### Default
```
```
##### Enum
```
```
## Tag
##### Object
```
Tag: Object {
    _id: <TagObjectID>,
    name: String,
    user_count: Integer,//default 0
    post_count: Integer,//default 0
    [user_list: <UserObjectID>[]],
    [post_list: <PostObjectID>[]]
}
```
##### Default
```
Tag.user_count: Integer = 0
Tag.post_count: Integer = 1
```
##### Enum
```
```
## Mark
##### Object
```
Mark: Object {
    _id: <MarkObjectID>,
    user: <UserObjectID>,
    post: <PostObjectID>,
    type: Integer, //0:voteup(like) 1:votedown(unlike) 2:mark
    mark_time: Timestamp,
}
```
##### Default
```
```
##### Enum
```
Mark.type: Integer {
    0 = mark,
    1 = up,
    2 = down
}
```
## Relation
##### Object
```
Relation: Object {
    _id: <RelationObjectID>,
    type: Integer, //0: follow, 1: fans
    source: <UserObjectID>,
    target: <UserObjectID>
}
```
##### Default
```
```
##### Enum
```
Relation.type: Integer {
    0 = follow
}
```
