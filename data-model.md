User
Post
Tag
Mark
Relation

#User
User: Object {
    _id: ObjectID,
    username: String,
    nickname: String,
    password: String,
    role: Role[],
    locked: boolean,
    social: Social,
    score: Score,
    gender: String,
    avatar: String,
    register_time: Timestamp,
    description: String,
    fans_count: Integer,
    follow_count: Integer,
    post_count: Integer,
    tag_count: Integer,
    tag_list: Tag[],
    last_login_time: Timestamp,
    last_login_ip: String
}

Role: Object {
    type: Integer,
    ...    
}

Social: Object {
    github: Object {},
    wechat: Object {},
    google: Object {},
    email: String,
    website: String,
    phone: String
}        
        
Score: Object {
    rank: Integer    
}
        
User_Min: Object {
    username: String,
    nickname: String,
    score: Score,
    avatar: String
}

#Tag
Tag: Object {
    _id: ObjectID,
    name: String,
    user_count: Integer,
    post_count: Integer,
    user_list: User[],
    post_list: Post[]
}

#Post
Post: Object {
    _id: ObjectID,
    author: User,
    type: Integer,
    create_time: Timestamp,
    title: String,
    content: String,
    tag_list: Tag[],
    up_count: Integer,
    down_count: Integer,
    mark_count: Integer,
    visit_count: Integer,
    commentable: Boolean,
    parent: Post
}

#Mark
Mark: Object {
    user: User,
    post: Post,
    type: Integer,
    mark_time: Timestamp,
}

#Relation
Relation: Object {
    type: Integer,
    source: User,
    target: User
}
