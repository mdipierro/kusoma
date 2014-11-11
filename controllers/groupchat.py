@auth.requires_login()
def history():
    return dict(group_chats=get_group_chat_messages())