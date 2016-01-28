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




## Tag
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
insert
//update tag 

delete
//delete from Tag
//delete tag from Post
//delete tag from User tag_list

edit
//update Tag.name

query
//tag query: Input(TagObjectID, FieldList)

## Mark
```
Mark: Object {
    _id: <MarkObjectID>,
    user: <UserObjectID>,
    post: <PostObjectID>,
    type: Integer, //0:voteup 1:votedown 2:mark
    mark_time: Timestamp,
}
```
###insert
voteup: update Vote - Input(user_id, post_id, type=0), update Post(up_count +1)
votedown: update Vote - Input(user_id, post_id, type=1), update Post(down_count + 1)
mark: update Vote - Input(user_id, post_id, type=2), update Post(mark_count + 1)

delete
//voteup: update post(up_count -1) and delete from Vote 
//votedown: update post(down_count -1)  and delete from Vote 
//mark: update post(mark_count -1) and delete from Vote 

edit(edit means insert or delete, no other means here)

query
// query the post list
//query voteup: input(use_id, type:0), output(post_id)
//query votedown: input(use_id, type:1), output(post_id)
//query mark: input(use_id, type:2), output(post_id)

// query statistic 
//query voteup: input(user_id, type: 0), output: post_count
//query votedown: input(user_id, type: 1), output: post_count
//query mark: input(user_id, type: 2), output: post_count

## Relation
```
Relation: Object {
    _id: <RelationObjectID>,
    type: Integer, //0: follow, 1: fans
    source: <UserObjectID>,
    target: <UserObjectID>
}
```
insert(source_id, target_id)
//follow a person: 
//update source_id(follow_count + 1) and insert into Relation(source source_id, target target_id)
//update target_id(fans_couont + 1)

delete(source_id, target_id) 
//cancel follow:
//update source_id(follow_count -1) and delete from Relation(source source_id, target target_id)
//update target_id(fans_count -1)

edit(edit means insert or delete, no other means here)

query(UserObjectID)
//query my followed: query from relation - input UserObjectID as source and query target
//query my fans: fans: query from relation - input UserObjectID as target and query source
