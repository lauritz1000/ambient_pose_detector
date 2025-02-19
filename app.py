import pywintypes
import time
import tkinter
import win32api
import win32con

import edgeiq
from PIL import Image, ImageTk

from posture import CheckPosture

"""
Use pose estimation to determine human poses in realtime. Human Pose returns
a list of key points indicating joints that can be used for applications such
as activity recognition and augmented reality.

To change the engine and accelerator, follow this guide:
https://alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html

To install app dependencies in the runtime container, list them in the
requirements.txt file.
"""


def main():
    pose_estimator = edgeiq.PoseEstimation("alwaysai/human-pose")
    pose_estimator.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(pose_estimator.model_id))
    print("Engine: {}".format(pose_estimator.engine))
    print("Accelerator: {}\n".format(pose_estimator.accelerator))

    fps = edgeiq.FPS()

    posture = CheckPosture(scale=0.8)

    bad_posture = False
    alpha = 0

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                results = pose_estimator.estimate(frame)
                # Generate text to display on streamer
                text = ["Model: {}".format(pose_estimator.model_id),
                        "Inference time: {:1.3f} s".format(results.duration)]
                for ind, pose in enumerate(results.poses):
                    text.append("Person {}".format(ind))
                    text.append('-' * 10)
                    # update the instance key_points to check the posture
                    posture.set_key_points(pose.key_points)

                    # play a reminder if you are not sitting up straight
                    correct_posture = posture.correct_posture()
                    if not correct_posture:
                        text.append(posture.build_message())
                        # make a sound to alert the user to improper posture
                        # print("\a")
                        if bad_posture:
                            alpha += 0.001
                            alpha = max(0, min(alpha, 0.5))
                        else:
                            bad_posture = True
                            alpha = 0
                        overlay(alpha)
                    else:
                        overlay(0)
                        bad_posture = False

                streamer.send_data(results.draw_poses(frame), text)

                fps.update()

                if streamer.check_exit():
                    break

                # time.sleep(2.0)
    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


def overlay(alpha):
    label.master.wm_attributes("-alpha", alpha)
    label.update_idletasks()
    label.update()
    time.sleep(.1)


if __name__ == "__main__":
    root = tkinter.Tk()
    load = Image.open("overlay3440x1440.png")
    render = ImageTk.PhotoImage(load)
    img = tkinter.Label(image=render, bg='white')
    img.image = render
    label = tkinter.Label(image=render, font=('Times New Roman', '80'), fg='black', )
    label.master.overrideredirect(True)
    label.master.geometry("+0+0")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")
    label.master.wm_attributes("-alpha", 0.5)

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    label.master.wm_attributes("-alpha", 0)

    main()
