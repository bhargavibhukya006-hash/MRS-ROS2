import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AgentNode(Node):
    def __init__(self):
        super().__init__('agent_node')
        self.pub = self.create_publisher(String, 'agent_positions', 10)
        self.ctrl_pub = self.create_publisher(String, 'agent_control', 10)

        self.timer = self.create_timer(1.0, self.publish_data)

    def publish_data(self):
        try:
            with open("/mnt/c/Users/tanum/OneDrive/Desktop/MRS-2/MRS-2-main/agent_positions.txt", "r") as f:
                data = f.read()
        except:
            data = "Waiting..."

        msg = String()
        msg.data = data
        self.pub.publish(msg)

        ctrl = String()
        ctrl.data = "FAST"   # change to FAST for testing
        self.ctrl_pub.publish(ctrl)

        
        with open("/mnt/c/Users/tanum/OneDrive/Desktop/MRS-2/MRS-2-main/control.txt", "w") as f:
            f.write(ctrl.data)

        self.get_logger().info(f"Positions: {data} | Control: {ctrl.data}")


def main():
    rclpy.init()
    node = AgentNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
