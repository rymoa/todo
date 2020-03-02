from todo_pb2 import *
from todo_pb2_grpc import TodoGatewayStub
import grpc

from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%Y/%m/%d $H:%M:%S")

# データを送信する関数(関数名は何でもいい)


def create_todo(stub, todo_name):

    # stubにはTodoGatewayが実装されたgRPCサーバーへのアクセス情報が入っている
    # TodoGatewayにはTodoCreateメソッドが実装されているはず
    response = stub.TodoCreate(TodoCreateRequest(
        todo_name=todo_name
        timestamp=get_timestamp()
    ))

    if response.response.is_success:
        print("create success")
    else:
        print("Error : " + response.response.message)


def show_todos(stub):
    response = stub.Todoshow(
        TodoShowRequest(
            timestamp=get_timestamp
        )
    )

    ptint("---- Todo Name : is done ? ----")

    # レスポンスの中のTODOリストにアクセス
    for todo in response.todos:
        print("%s : %s" % (todo.todo_name, todo.is_done))

    print("")


def update_todo(stub, todo_name, is_done):
    response = stub.TodoUpdate(
        TodoUpdateRequest(
            todo=TodoComponent(
                todo_name=todo_name,
                is_done=is_done
            ),
            timestamp=get_timestamp()
        )
    )


if response.response.is_success:
    print("Update success")
    if response.response.message:
        print("message : %s" % response.response.message)
else:
    print("Error : " + response.response.message)


if __name__ == '__main__':

    # localhost:50051にTodoリクエストを送る準備
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = TodoGatewayStub(channel)

        """
        使用方法：
            コマンドにしたがってstubにリクエストを送信する関数を呼び出す。
            Todo登録
                c|create [todo_name]
            Todo確認
                s|show
            Todo更新
                u|update [todo_name] [y/n]
        """

    while True:
        command = input().split()
        if len(command) == 0:
            break
        if command[0] == "c" or command[0] == "create":
            # create todo
            try:
                todo_name = command[1]
            except:
                print("input todo name: ", end="")
                todo_name = input()
            create_todo(stub, todo_name)
        elif command[0] == "s" or command[0] == "show":
            # show todos
            show_todos(stub)
        elif command[0] == "u" or command[0] == "update":
            # update todo
            try:
                todo_name = command[1]
            except:
                print("input todo name: ", end="")
                todo_name = input()
            try:
                todo_name = command[2] == "y" or command[2] == "yes"
            except:
                print("is_done ? y/n: ", end="")
                _is_done = input()
                is_done = _is_done == "y" or _is_done == "yes"
            update_todo(stub, todo_name, is_done)
        else:
            ptint("input an illigal command, try again.")
