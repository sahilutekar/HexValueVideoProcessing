import cv2
import numpy as np

class VideoProcessor:
    def __init__(self, video_path, output_video_path):
        self.video_path = video_path
        self.output_video_path = output_video_path
        self.roi_top_left = None
        self.roi_bottom_right = None
        self.fps = None
        self.frame_width = None
        self.frame_height = None
        self.video_capture = None
        self.output_video = None

    def select_roi(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_top_left = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.roi_bottom_right = (x, y)
            cv2.destroyAllWindows()

    def process_video(self):
        self.video_capture = cv2.VideoCapture(self.video_path)
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.output_video = cv2.VideoWriter(self.output_video_path, fourcc, self.fps, (self.frame_width, self.frame_height))

        cv2.namedWindow("Select ROI")
        cv2.setMouseCallback("Select ROI", self.select_roi)

        while True:
            ret, frame = self.video_capture.read()

            if not ret:
                break

            cv2.imshow("Select ROI", frame)

            if cv2.waitKey(int(1000 / self.fps)) & 0xFF == ord('q'):
                break

            if self.roi_top_left is not None and self.roi_bottom_right is not None:
                roi = frame[self.roi_top_left[1]:self.roi_bottom_right[1], self.roi_top_left[0]:self.roi_bottom_right[0]]
                b, g, r = cv2.split(roi)

                hex_values = ['#{:02x}{:02x}{:02x}'.format(b_val, g_val, r_val) for b_val, g_val, r_val in zip(b.flatten(), g.flatten(), r.flatten())]

                for i, hex_val in enumerate(hex_values):
                    x = i % roi.shape[1]
                    y = i // roi.shape[1]
                    cv2.putText(roi, hex_val, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                text_bg = 255 * np.ones(roi.shape, dtype=np.uint8)
                text_with_bg = cv2.putText(text_bg, '\n'.join(hex_values), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                frame[self.roi_top_left[1]:self.roi_bottom_right[1], self.roi_top_left[0]:self.roi_bottom_right[0]] = text_with_bg

            cv2.imshow("Video with Hex Values", frame)
            self.output_video.write(frame)

        self.video_capture.release()
        self.output_video.release()
        cv2.destroyAllWindows()

# Example usage
video_path = "your_path"
output_video_path = "your_path"

processor = VideoProcessor(video_path, output_video_path)
processor.process_video()
