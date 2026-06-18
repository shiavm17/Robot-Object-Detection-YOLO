import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

import json


class YoloDetectorNode(Node):

    def __init__(self):
        super().__init__('yolo_detector_node')

        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('model_path', 'models/yolov8n.pt')
        self.declare_parameter('confidence_threshold', 0.5)

        camera_topic = self.get_parameter('camera_topic').get_parameter_value().string_value
        model_path = self.get_parameter('model_path').get_parameter_value().string_value
        self.conf_threshold = self.get_parameter('confidence_threshold').get_parameter_value().double_value

        self.bridge = CvBridge()

        self.get_logger().info(f'Loading YOLO model from {model_path}')
        self.model = YOLO(model_path)

        self.subscription = self.create_subscription(
            Image,
            camera_topic,
            self.image_callback,
            10
        )

        self.detection_publisher = self.create_publisher(String, '/detections', 10)
        self.image_publisher = self.create_publisher(Image, '/detection_image', 10)

        self.get_logger().info(f'YOLO Detector Node started, subscribed to {camera_topic}')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        results = self.model(frame, conf=self.conf_threshold, verbose=False)

        detections = []
        annotated_frame = frame.copy()

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    'label': label,
                    'confidence': round(conf, 3),
                    'bbox': [x1, y1, x2, y2]
                })

                color = (0, 255, 0) if label == 'person' else (255, 0, 0)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    annotated_frame,
                    f'{label} {conf:.2f}',
                    (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

        detection_msg = String()
        detection_msg.data = json.dumps(detections)
        self.detection_publisher.publish(detection_msg)

        annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding='bgr8')
        annotated_msg.header = msg.header
        self.image_publisher.publish(annotated_msg)


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()