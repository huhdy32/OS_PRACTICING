import time
import process
import task_scheduler

VERSION = 1.1

class Processor(object):
    curr_process = None
    curr_proc_run_tick = 0
    scheduling_algorithm = None
    processor_ready_queue = None
    time_quantum = -1

    def __init__(self, _scheduling_algorithm="FCFS", _time_quantum=-1):
        self.curr_process = None
        self.scheduling_algorithm = _scheduling_algorithm
        self.processor_ready_queue = list()
        self.time_quantum = _time_quantum
    
    def get_total_workload(self):
        total_workload = 0

        if self.curr_process is not None:
            total_workload += self.curr_process.get_remaining_time()

        for i in range(0, len(self.processor_ready_queue)):
            total_workload += self.processor_ready_queue[i].get_remaining_time()
        
        return total_workload

    def get_assigned_process(self):
        return self.curr_process
    
    def put_process_to_ready_queue(self, _given_process):
        self.processor_ready_queue.append(_given_process)
        self.curr_proc_run_tick = 0


    def check_and_assign_process(self):
        # Check process ready queue and select
        selected_idx = self.select_process_idx_to_assign()

        if selected_idx == -1:
            return

        selected_process = self.processor_ready_queue[selected_idx]
        
        if self.curr_process is None:
            pass
        else:
            self.put_assigned_process_to_ready_queue()

        self.curr_process = selected_process
        self.processor_ready_queue.remove(selected_process)

        self.curr_proc_run_tick = 0

        return
    
    def run_process(self):
        if self.curr_process is not None:
            self.curr_process.run_proc(1)
            self.curr_proc_run_tick += 1
    
    def cleanup_process(self):
        if self.curr_process is not None:
            if self.curr_process.get_remaining_time() == 0:
                # terminate process
                resources_to_return = self.curr_process.get_assigned_resource()
                self.curr_process = None
                self.curr_proc_run_tick = 0

                return resources_to_return
            else:
                return None
        else:
            return None
    
    def put_assigned_process_to_ready_queue(self):
        self.processor_ready_queue.append(self.curr_process)
        self.curr_process = None
    
    def select_process_idx_to_assign(self):
        process_idx = task_scheduler.get_process_idx_from_queue(self.curr_process, self.processor_ready_queue, self.scheduling_algorithm, self.curr_proc_run_tick, self.time_quantum)

        return process_idx
