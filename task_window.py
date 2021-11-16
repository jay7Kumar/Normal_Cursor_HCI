import math
import random
import time
import tkinter as tk
import tkinter.messagebox
import objects_management as om
import record_data_excel as record_data


# how to do the task: click the green button first and then click the blue target
# Once you successfully click the target, a new trial starts
# If you click a grey distractor, an error occurs
# If you click on the empty area, an error occurs

class Application(tk.Frame):






    def __init__(self, master=None):
        radius_list = [10, 20, 30]
        target_dis_list = [100, 600, 800]
        distractor_list = [10, 20, 50]
        super().__init__(master)  # Call tk.Frame.__init__(master)
        self.master = master  # Update the master object after tk.Frame() makes necessary changes to it
        window_width = 1200
        window_height = 700
        self.error_a_trial = 0
        self.canvas = tk.Canvas(self.master, width=window_width, height=window_height)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.participant_name = 'test'
        self.write_data = record_data.RecordDataToExcel()
        self.write_data.write_to_excel(("ParticipantName", "Block","index","Trial", "Radius", "Distance", "Time","Distractors","Error"))
        # dist_num_random = random.choice(distractor_list)
        # print(dist_num_random,"distractor")
        object_num = 51
        distractor_num = distractor_list # the number of distractors
        object_radius = 20  # radius of distractor and target. Note in the assignment document, target size is diameter
        target_distance = 800
        self.object_manage = om.ObjectManager(self.canvas, window_width, window_height, object_num, object_radius,
                                              target_distance,distractor_num)
        self.object_manage.radius_target_combo = self.object_manage.generate_trial_order(radius_list,target_dis_list,distractor_list)
        self.objects = self.object_manage.initail_random_targets()
        print(len(self.objects), "length")

        self.object_index = len(self.objects)

        self.task_start = False
        self.task_start_time = 0
        print("create circles executed")
        # self.createCircles()




    def mouse_left_button_press(self, event):
        if self.object_manage.status == "end of Exp":
            self.canvas.delete("all")
            tk.messagebox.showinfo("", "End of Experiment.")
            self.object_manage.status = " "

        else:
            # print(self.object_index)  # print the index of the selected object
            self.object_index = len(self.objects)  # default value

            for i in range(len(self.objects)):
                if math.hypot(self.objects[i].x - event.x, self.objects[i].y - event.y) - self.objects[i].radius <= 0:
                    self.object_index = i  # find the object clicked
                    break

            if self.object_index == 0 and not self.task_start:  # click the start button
                self.task_start = True
                self.task_start_time = int(time.time() * 1000.0)  # record the time
                self.object_manage.update_object_mouse_click(self.object_index)
                print("Task Start")

            if self.task_start:  # need to click the start button first
                if self.object_index == 1:  # click the target
                    task_time = int(time.time() * 1000.0) - self.task_start_time
                      # start a new task
                    # self.object_manage.update_object_mouse_click(self.object_index)
                    self.object_manage.generate_random_targets()
                    self.task_start = False
                    print("The target is selected and the task time is " + str(task_time))
                    print(self.objects[1].trail,"index")
                    data_row = (self.participant_name, self.objects[1].block,self.objects[1].combination_index ,self.objects[1].trail, self.objects[1].radius,
                    self.objects[1].distance, task_time,self.objects[1].distractor_num ,self.error_a_trial)
                    print("excel created")
                    # self.createCircles()
                    self.write_data.write_to_excel(data_row)
                    self.error_a_trial = 0


                elif 1 < self.object_index < len(self.objects):  # click a distractor
                    print("Selection error with distractors")
                    self.object_manage.update_object_mouse_click(self.object_index)
                    # self.object_manage.generate_random_targets()
                    self.error_a_trial += 1
                elif self.object_index == len(self.objects):  # click empty space on the interface
                    print("Selection error in empty space")
                    self.error_a_trial += 1


if __name__ == '__main__':
    master = tk.Tk()
    # master.config(cursor="none")  # hid cursor in canvas
    master.resizable(0, 0)
    app = Application(master=master)
    app.mainloop()  # mainloop() tells Python to run the Tkinter event loop. This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until the window it's called on is closed.
