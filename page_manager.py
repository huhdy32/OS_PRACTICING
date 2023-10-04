VERSION = 1.0



class PageManager(object):

    ref_counter = 0
    page_frame = None
    page_frame_info = None
    page_replacement_algorithm = "FIFO"
    # FIFO, LRU, SC(Second Chance)

    def __init__(self, _page_frame_size, _page_replacement_algorithm="LRU"):
        self.ref_counter = 0
        self.page_frame = [-1] * _page_frame_size
        self.page_frame_info = [0] * _page_frame_size
        self.page_replacement_algorithm = _page_replacement_algorithm
        self.curr_frame_idx = -1 # 교체되는 프레임의 인덱스를 반환하기 위함

    def get_curr_page_frame(self):
        return self.page_frame

    def get_curr_page_frame_info(self):
        return self.page_frame_info

    def reference_page(self, _given_page_num):
        is_page_fault = True
        is_page_frame_available = False
        referenced_frame_number = -1

        # 1. check page exists
        for i in range(0, len(self.page_frame)):
            if self.page_frame[i] == _given_page_num:
                referenced_frame_number = i
                
                # i) update frame reference information
                if self.page_replacement_algorithm == "LRU":
                    self.page_frame_info[referenced_frame_number] = self.ref_counter
                elif self.page_replacement_algorithm == "SC":
                    self.page_frame_info[referenced_frame_number] = 1

                is_page_fault = False
                break

        # 2. if page fault occurs, insert or replace page
        if referenced_frame_number == -1:

            # i) check available page exists in the page frame
            for i in range(0, len(self.page_frame)):
                if self.page_frame[i] == -1:
                    is_page_frame_available = True
                    self.page_frame[i] = _given_page_num
                    if self.page_replacement_algorithm == "FIFO":
                        self.page_frame_info[i] = self.ref_counter
                    elif self.page_replacement_algorithm == "LRU":
                        self.page_frame_info[i] = self.ref_counter
                    elif self.page_replacement_algorithm == "SC":
                        self.page_frame_info[i] = 1
                    referenced_frame_number = i # 몇번째 프레임를 참조했는지를 표가허기 위함
                    break
                    
                    
                

            # ii) if page frame is not available, replace page
            if not is_page_frame_available:
                referenced_frame_number = self.replace_page(_given_page_num)

        # 3. update timestamp (=ref_counter)
        self.ref_counter += 1

        return [is_page_fault, referenced_frame_number]


    def replace_page(self, _given_page_num):
        replaced_frame_number = -1

        if self.page_replacement_algorithm == "FIFO":
            replaced_frame_number = self.replace_page_with_FIFO(_given_page_num)
        elif self.page_replacement_algorithm == "LRU":
            replaced_frame_number = self.replace_page_with_LRU(_given_page_num)
        elif self.page_replacement_algorithm == "LRU":
            replaced_frame_number = self.replace_page_with_LRU(_given_page_num)
        elif self.page_replacement_algorithm == "SC":
            replaced_frame_number = self.replace_page_with_second_chance(_given_page_num)
        
        return replaced_frame_number


    def replace_page_with_FIFO(self, _given_page_num):
        # Implement page replacement algorithm with FIFO
        replaced_frame_number = -1
        self.curr_frame_idx = (self.curr_frame_idx+1) % len(self.page_frame)
        replaced_frame_number = self.curr_frame_idx
        self.page_frame[replaced_frame_number] = _given_page_num

        return replaced_frame_number


    def replace_page_with_LRU(self, _given_page_num):
        # Implement page replacement algorithm with LRU
        replaced_frame_number = -1
        latest = 1000
        for i in range(len(self.page_frame_info)) :
            if latest > self.page_frame_info[i] :
                replaced_frame_number = i
                latest = self.page_frame_info[i]
        if replaced_frame_number != -1:
            self.page_frame[replaced_frame_number] = _given_page_num
            self.page_frame_info[replaced_frame_number] = self.ref_counter
        return replaced_frame_number

    
    def replace_page_with_second_chance(self, _given_page_num):
        replaced_frame_number = -1
        while(True):
            self.curr_frame_idx = (self.curr_frame_idx+1) % len(self.page_frame)
            if self.page_frame_info[self.curr_frame_idx] == 0:
                self.page_frame_info[self.curr_frame_idx] = 1
                self.page_frame[self.curr_frame_idx] = _given_page_num
                replaced_frame_number = self.curr_frame_idx
                break
            else:
                self.page_frame_info[self.curr_frame_idx] = 0
            
        return replaced_frame_number

