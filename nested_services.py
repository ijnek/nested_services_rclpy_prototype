import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from std_srvs.srv import Trigger


class Node1(Node):

    def __init__(self):
        super().__init__('node1')
        self.service = self.create_service(Trigger, 'node1/trigger', self.srv_cb)
        self.client = self.create_client(Trigger, 'node2/trigger')

    def srv_cb(self, request, header, response):

        def async_cb(future):
            response = Trigger.Response()
            response.message = "Node 2 said: '" + future.result().message + "'"
            self.service.send_response(response, header)

        request_inner = Trigger.Request()
        self.future = self.client.call_async(request_inner)
        self.future.add_done_callback(async_cb)
        return self.future

class Node2(Node):

    def __init__(self):
        super().__init__('node2')
        self.service = self.create_service(Trigger, 'node2/trigger', self.srv_cb)

    def srv_cb(self, request, header, response):
        print("HERE2")
        return Trigger.Response(message="Hello!")

def main(args=None):
    rclpy.init(args=args)
    executor = SingleThreadedExecutor()
    node_1 = Node1()
    node_2 = Node2()
    executor.add_node(node_1)
    executor.add_node(node_2)
    executor.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
