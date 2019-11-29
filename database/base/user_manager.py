# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: user_manager.py
# 本模块包含：
# 不对外可见的数据库操作函数
from database.models.model import UserInfo
from database.models.model import Follow
from database.models.model import QuestionInfo
from database.base.question_manager import delete_question_by_id



# 根据用户名查找用户
def get_user_by_name(user, session):
    user_info = session.query(UserInfo).filter_by(name=user["name"]).first()
    res = {}
    if isinstance(user_info, UserInfo):
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s fond successfully" % user["name"]
        res["content"] = user_info.to_dict()
    else:
        res["success"] = True
        res["status"] = 1000
        res["message"] = "User: %s not fond" % user["name"]
        res["content"] = None

    return res


# 插入新用户
def insert_user(user, session):
    res = {}

    user_info = get_user_by_name(user, session)
    if isinstance(user_info, UserInfo):
        res["success"] = False
        res["status"] = 1002
        res["message"] = "User: %s already exits!!!" % user["name"]
        res["content"] = None
    else:
        user_info = UserInfo()

        user_info.dict_init(user)

        session.add(user_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s insert successfully" % user["name"]
        res["content"] = None
    return res


# 根据用户名删除用户
def delete_user_by_name(name, session):
    res = {}

    try:
        # 检查数据库中是否存在用户
        user_info = session.query(UserInfo).filter_by(name=name["name"]).first()


        session.delete(user_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s deleted successfully!" % name["name"]

        res["content"] = " "
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message

        res["content"] = " "

    return res


# 修改用户密码
def update_user_pwd(user, session):
    res = {}
    # 检查数据库中是否存在用户
    user_info = session.query(UserInfo).filter_by(name=user["name"]).first()

    # 若用户不存在
    if not isinstance(user_info, UserInfo):
        res["success"] = False
        res["status"] = 1000
        res["message"] = "User: %s not fond" % user["name"]
        res["content"] = None
    else:
        user_info.password = user["password"]
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s password update successfully!!" % user["name"]
        res["content"] = user_info.to_dict()
        session.commit()

    return res



# 获取用户关注列表

def get_user_follow(user, session):
    res = {}
    user_info = session.query(UserInfo).filter_by(name=user["name"]).first()
    follow_list = []
    # 若用户不存在
    if not isinstance(user_info, UserInfo):
        res["success"] = False
        res["status"] = 1000
        res["message"] = "User: %s not fond" % user["name"]
        res["content"] = None
    else:
        follow_info_list = session.query(Follow).filter_by(uid=user_info.uid).all()
        for follow_info in follow_info_list:

            question_info = session.query(UserInfo).filter_by(quid=follow_info.quid).first()

            follow_list.append(question_info.to_dict())

        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s's follow fond" % user["name"]
        res["content"] = follow_list

    return res


# 增加关注
def insert_follow(follow, session):
    res = {}
    try:
        follow_info = Follow()
        follow_info.dict_init(follow)
        session.add(follow_info)
        session.commit()

        res["success"] = True
        res["status"] = 0
        res["message"] = "Follow: %s to %s insert successfully" % (follow_info.uid, follow_info.quid)
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


# 删除关注
def delete_follow(follow, session):
    res = {}
    try:
        follow_info = session.query(Follow).filter_by(uid=follow["uid"],quid=follow["quid"]).first()
        session.delete(follow_info)
        session.commit()

        res["success"] = True
        res["status"] = 0
        res["message"] = "Follow: %s to %s deleted successfully" % (follow_info.uid, follow_info.quid)
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res
