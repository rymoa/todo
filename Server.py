from todo_pb2 import *
from todo_pb2_grpc import add_TodoGatewayServicer_to_server, TodoGatewayServicer

from concurrent import futures
from datetime import datetime
import time
import grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def get_timestamp():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class RouteTodoServicer(TodoGatewayServicer):
    """
    Todoサーバーの実装
    protoで定義したservice名のメソッドを実装する
    """

    todos = {}

    # TODOを作成するロジック
    def TodoCreate(self, request, response):
        # request.fieldでprotoで定義した値にアクセスできる
        print("Todo Create Called : %s" % request.timestamp)
        try:
            self.todos[request.todo_name] = TodoComponent(
                todo_name=request.todo_name,
                is_done=False    # 作成時はTODO完了していないためFalse
            )
            is_success = True
            message = None
        except:
            import traceback
            traceback.print_exc()
            is_success = False
            message = "something happen"

        # レスポンスを返す時はreturnするだけで良い
        return TodoCreateResponse(
            response=ServerResponseComponent(
                is_success=is_success,
                message=message
            ),
            timestamp=get_timestamp()
        )

    def TodoShow(self, request, response):
        print("Todo Show Called : %s" % request.timestamp)
        try:
            todo_list = [
                todo for todo in self.todos.values()
            ]
        except:
            import traceback
            traceback.print_exc()
            todo_list = []
        return TodoShowResponse(todos=todo_list, timestamp=get_timestamp())

    def TodoUpdate(self, request, response):
        print("Todo Update Called : %s" % request.timestamp)
        try:
            if request.todo.todo_name in self.todos:
                message = None
                # 入れ子になっているfieldにもアクセスできる
                self.todos[request.todo.todo_name].is_done = request.todo.is_done
            else:
                message = "No such a todo"
            is_success = True
        except:
            is_success = False
            message = "something happen"
        return TodoUpdateResponse(
            response=ServerResponseComponent(
                is_success=is_success,
                message=message
            ),
            timestamp=get_timestamp()
        )

# サーバーの実行


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TodoGatewayServicer_to_server(
        RouteTodoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server Start!!")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
