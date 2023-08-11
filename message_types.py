class MessageTypes:
    # Chat Messages
    CHAT_MESSAGE = 100
    SERVER_MESSAGE = 101
    ERROR_MESSAGE = 102

    # User Commands
    SET_USERNAME_COMMAND = 200
    GET_USERINFO_COMMAND = 201
    CHANGE_USERNAME_COMMAND = 202
    GET_USERS_COMMAND = 203
    QUIT_COMMAND = 205

    # Command Responses
    ERROR_SETTING_USERNAME = 204
    SUCCESS_SETTING_USERNAME = 206
    SUCCESS_JOINING_CHAT = 207
    SUCCESS_QUITTING_CHAT = 208
    ERROR_JOINING_CHAT = 209
    RETRIEVE_USER_INFO = 210
    PING_REQUEST = 211
    PONG_RESPONSE = 212

    # Chat Notifications
    JOIN_MESSAGE = 300
    LEAVE_MESSAGE = 301
    USER_CHANGED_USERNAME_MESSAGE = 302
    USERS_LIST_MESSAGE = 303

    # Mapping from codes to lowercase descriptions
    descriptions = {
        CHAT_MESSAGE: "chat message",
        SERVER_MESSAGE: "server message",
        ERROR_MESSAGE: "error message",
        SET_USERNAME_COMMAND: "set username command",
        GET_USERINFO_COMMAND: "get userinfo command",
        CHANGE_USERNAME_COMMAND: "change username command",
        GET_USERS_COMMAND: "get users command",
        QUIT_COMMAND: "quit command",
        ERROR_SETTING_USERNAME: "error setting username",
        SUCCESS_SETTING_USERNAME: "success setting username",
        SUCCESS_JOINING_CHAT: "success joining chat",
        SUCCESS_QUITTING_CHAT: "success quiting chat",
        ERROR_JOINING_CHAT: "error joining chat",
        RETRIEVE_USER_INFO: "retrieve user info",
        PING_REQUEST: "ping request",
        PONG_RESPONSE: "pong response",
        JOIN_MESSAGE: "join message",
        LEAVE_MESSAGE: "leave message",
        USER_CHANGED_USERNAME_MESSAGE: "user changed username message",
        USERS_LIST_MESSAGE: "users list message",
    }