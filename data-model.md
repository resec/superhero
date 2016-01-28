# Mongo Data Model

## User
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
    social: {
        [github: {...}],
        [wechat: {...}],
        [google: {...}],
        [email: String],
        [website: String],
        [phone: String],
        ...
    },
    score: {
        rank: Integer
        ...
    },
    gender: String,
    avatar: String,
    register_time: Timestamp,
    description: String,
    fans_count: Integer,
    follow_count: Integer,
    post_count: Integer,
    tag_count: Integer,
    tag_list: <TagObjectID>[],
    last_login_time: Timestamp,
    last_login_ip: String
}
```
## Post
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
    parent: Post
}
```
## Tag
```
Tag: Object {
    _id: <TagObjectID>,
    name: String,
    user_count: Integer,
    post_count: Integer,
    user_list: <UserObjectID>[],
    post_list: <PostObjectID>[]
}
```
## Mark
```
Mark: Object {
    _id: <MarkObjectID>,
    user: <UserObjectID>,
    post: <PostObjectID>,
    type: Integer,
    mark_time: Timestamp,
}
```
## Relation
```
Relation: Object {
    _id: <RelationObjectID>,
    type: Integer,
    source: <UserObjectID>,
    target: <UserObjectID>
}
```
