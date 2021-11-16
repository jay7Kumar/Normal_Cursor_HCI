import math
import random
import itertools


class Circle:
    def __init__(self, x, y, radius,distance,block,combination_index,trail,distractor_num):
        self.x = x
        self.y = y
        self.radius = radius
        self.distance = distance
        self.block = block
        self.trail = trail
        self.combination_index = combination_index
        self.distractor_num = distractor_num


class ObjectManager:
    def __init__(self, canvas, window_width, window_height, object_num, object_radius, target_distance,distractor_num):
        self.canvas = canvas
        self.window_width = window_width
        self.window_height = window_height
        self.object_num = object_num + 1  # distractor number + one target
        self.object_radius = object_radius  # the size of object and distractors
        self.start_button = 0  # start button
        self.start_button_tag = 0
        self.start_button_radius = 30
        self.target_distance = target_distance
        self.objects = []  # store all distractors and the target. The 1st is the target, others are distractors
        self.object_tag_in_canvas = []  # store the tag of the distractors and the target in canvas. The 1st is the target, others are distractors
        self.last_selected_object_index = 0
        self.distractor_num = distractor_num
        self._block_total = 2  # block number
        self._trial_repeat_total = 3  # repeat number
        self.condition_in_block_index = 0  # used to indicate the condition
        self.trial_repeat_index = 0  # used to indicate the repeat of a trial
        self.combinations = []
        self._condition_total = 9
        self.block = 2
        self.block_index = 0
        self.combination = 6
        self.combination_index = 0
        self.trail_index = -1
        self.trails = 1
        self.radius_target_combo = []
        self.combi = []
        self.set_combination = 1
        self.status = ""


    def update_object_mouse_click(self, object_index):
        # object_tag is used to find the object in canvas, so that we can update the object
        object_tag = self.object_tag_in_canvas[object_index]
        if object_index == 0:
            self.canvas.itemconfig(object_tag, fill="green", outline="gray", width=6)  # the start button
        elif object_index == 1:
            self.canvas.itemconfig(object_tag, fill="blue", outline="gray", width=6)  # the target
        else:
            self.canvas.itemconfig(object_tag, fill="gray", outline="red", width=6)  # a distractor

    def paint_objects(self):
        self.canvas.delete("all")  # delete all elements on the canvas

        for i in range(len(self.objects)):
            if i == 0:
                color = "green"  # start button
            elif i == 1:
                color = "blue"  # the target
            else:
                color = "grey"  # the distractors

            tag = self.canvas.create_oval(self.objects[i].x - self.objects[i].radius,
                                          self.objects[i].y - self.objects[i].radius,
                                          self.objects[i].x + self.objects[i].radius,
                                          self.objects[i].y + self.objects[i].radius, fill=color,
                                          outline=color, width=0)
            # add object's tag to the list, so they can be accessed according to their tag
            # note that objects are indexed in the same order in both objects and object_tag_in_canvas lists
            self.object_tag_in_canvas.append(tag)
    def generate_random_targets(self):
        radius_list = [10, 20, 30]
        target_dis_list = [100, 600, 800]
        distractor_list = [10, 20, 50]
        print(self.block_index,"block")
        if self.block_index < self.block:
            if self.combination_index < self.combination:
                if self.trail_index < 1:
                    self.objects.clear()  # remove all objects
                    self.object_tag_in_canvas.clear()

                    # self.combination_index += 1
                    # if self.combination_index == 0 and self.trail_index == 0:
                    # self.combinations = self.generate_trial_order(radius_list, target_dis_list,distractor_list)
                    # print(len(self.combinations),"len of combi")
                    print(self.radius_target_combo, "radius combo")
                    # self.radius_target_combo = self.radius_target_combo[self.combination_index]
                    self.combi = self.radius_target_combo[self.combination_index]
                    target_dis = self.combi[1]
                    distractor_num = self.combi[2]

                    # print(,"combinatyiomns")
                    i = 0  # generate the start button
                    start_button = Circle(self.start_button_radius, self.window_height - self.start_button_radius,
                                          50, 0, 0, 0, 0, 0)
                    self.objects.append(start_button)

                    i = 1  # generate the target. We need to consider the distance between the target and the start button
                    target_x = 0
                    target_y = 0

                    while target_x < self.combi[0] or target_x > (self.window_width - self.combi[0]) \
                            or target_y < self.combi[0] or target_y > (self.window_height - self.combi[0]):
                        # random_target = random.choice(target_dis_list)

                        ang = random.uniform(0, 1) * 2 * math.pi
                        adj = math.cos(ang) * self.combi[1]
                        opp = math.sin(ang) * self.combi[1]
                        target_x = start_button.x + adj
                        target_y = start_button.y + opp

                    # random_radius = random.choice(radius_list)
                    target = Circle(target_x, target_y, self.combi[0], target_dis, self.block_index, self.combination_index,
                                    self.trail_index, distractor_num)
                    self.objects.append(target)

                    # generate distracotrs.
                    # random_distractor = random.choice(self.object_num)
                    # print(self.distractor_num,"distractor")
                    # random_distractor_size = random.choice(self.distractor_num)
                    # print(random_distractor_size,"random distractor")
                    while i < self.combi[2]:
                        # for rad in radius_list :
                        # random_radius = random.choice(radius_list)
                        new_object = Circle(random.randint(self.combi[0], self.window_width - self.combi[0]),
                                            random.randint(self.combi[0], self.window_height - self.combi[0]),
                                            self.combi[0], target_dis, self.block_index, self.combination_index,
                                            self.trail_index, distractor_num)

                        # print(new_object,"qq")
                        overlap = False
                        # print(self.objects,"www")
                        for j in self.objects:
                            if self.check_two_targets_overlap(new_object, j):
                                overlap = True
                                break

                        if not overlap:  # if the new object does not overlap with others, add it to the objects list.
                            self.objects.append(new_object)
                            i += 1
                    print(self.trail_index,"aaaaa")
                    self.trail_index += 1
                    print(self.trail_index,"inside if")
                    self.paint_objects()
                    self.objects[1].trail = self.trail_index
                    print(self.objects[1].trail,"obj trail index")
                    print(self.combination_index, "combination_index _if")
                    return self.objects
                else:
                    print("end trail")
                    print(self.trail_index,"inside else")
                    self.trail_index = 0
                    self.objects[1].trail = self.trail_index
                    # if self.combination_index < 2:
                    self.combination_index += 1
                    self.objects[1].combination_index = self.combination_index
                    self.objects[1].trail = self.trail_index
                    # self.objects[1].combination_index = self.combination_index
                    self.paint_objects()
                    return self.objects
            else:
                print("end combination")
                self.combination_index = 0
                self.objects[1].combination_index = self.combination_index
                if self.block_index >= self.block:
                    self.block_index = 0
                else:
                    self.block_index += 1
            # self.block_index += 1
                print(self.block_index,"block")
                self.objects[1].block = self.block_index
                self.objects[1].trail = self.trail_index
                self.objects[1].combination_index = self.combination_index
                self.paint_objects()
                return self.objects
            self.block_index += 1
            self.objects[1].block = self.block_index
            self.paint_objects
            return self.objects
        else:
            print("end of exp")
            self.status = "end of Exp"
            # self.canvas.delete("all")
            self.objects = []
            self.paint_objects
            return self.objects


    def initail_random_targets(self):
        radius_list = [10, 20, 30]
        target_dis_list = [100, 600, 800]
        distractor_list = [10, 20, 50]
        self.objects.clear()  # remove all objects
        self.object_tag_in_canvas.clear()

        # self.combination_index += 1
        # if self.combination_index == 0 and self.trail_index == 0:
        # self.combinations = self.generate_trial_order(radius_list, target_dis_list,distractor_list)
        # print(len(self.combinations),"len of combi")
        print(self.radius_target_combo, "radius combo")
        # self.radius_target_combo = self.radius_target_combo[self.combination_index]
        self.combi = self.radius_target_combo[self.combination_index]
        target_dis = self.combi[1]
        distractor_num = self.combi[2]

        # print(,"combinatyiomns")
        i = 0  # generate the start button
        start_button = Circle(self.start_button_radius, self.window_height - self.start_button_radius,
                              50, 0, 0, 0, 0, 0)
        self.objects.append(start_button)

        i = 1  # generate the target. We need to consider the distance between the target and the start button
        target_x = 0
        target_y = 0

        while target_x < self.combi[0] or target_x > (self.window_width - self.combi[0]) \
                or target_y < self.combi[0] or target_y > (self.window_height - self.combi[0]):
            # random_target = random.choice(target_dis_list)

            ang = random.uniform(0, 1) * 2 * math.pi
            adj = math.cos(ang) * self.combi[1]
            opp = math.sin(ang) * self.combi[1]
            target_x = start_button.x + adj
            target_y = start_button.y + opp

        # random_radius = random.choice(radius_list)
        target = Circle(target_x, target_y, self.combi[0], target_dis, self.block_index, self.combination_index,
                        self.trail_index, distractor_num)
        self.objects.append(target)

        # generate distracotrs.
        # random_distractor = random.choice(self.object_num)
        # print(self.distractor_num,"distractor")
        # random_distractor_size = random.choice(self.distractor_num)
        # print(random_distractor_size,"random distractor")
        while i < self.combi[2]:
            # for rad in radius_list :
            # random_radius = random.choice(radius_list)
            new_object = Circle(random.randint(self.combi[0], self.window_width - self.combi[0]),
                                random.randint(self.combi[0], self.window_height - self.combi[0]),
                                self.combi[0], target_dis, self.block_index, self.combination_index,
                                self.trail_index, distractor_num)

            # print(new_object,"qq")
            overlap = False
            # print(self.objects,"www")
            for j in self.objects:
                if self.check_two_targets_overlap(new_object, j):
                    overlap = True
                    break

            if not overlap:  # if the new object does not overlap with others, add it to the objects list.
                self.objects.append(new_object)
                i += 1
        # print(self.trail_index, "aaaaa")
        # self.trail_index += 1
        # print(self.trail_index, "inside if")
        self.paint_objects()
        # self.objects[1].trail = self.trail_index
        # print(self.objects[1].trail, "obj trail index")
        return self.objects


    def generate_trial_order(self,radius_list,target_list, distractor_number):
        #  generate combinations
        width_distance_combinations = list(itertools.product(radius_list, target_list,distractor_number))
        random.shuffle(width_distance_combinations)  # shuffle list
        return width_distance_combinations

    def check_two_targets_overlap(self, t1, t2):
        if math.hypot(t1.x - t2.x, t1.y - t2.y) > (t1.radius + t2.radius):
            return False
        else:
            return True

    '''
    def _euclidean_distance(self, point_1, point_2):
        return math.hypot(point_1.x - point_2.x,
                          point_1.y - point_2.y)
    '''
