import time

VERSION = 1.1

class Process(object):
    proc_num = -1
    req_resources = []
    req_run_time = 0
    state = -1

    assigned_resources = []
    accumulated_run_time = 0

    process_tick = 0

    ###################################################
    # Class initialization
    ###################################################

    def __init__(self, _proc_num, _req_resources, _req_run_time):
        self.proc_num = _proc_num
        self.req_resources = _req_resources
        self.req_run_time = _req_run_time

        self.assigned_resources = [0]*len(self.req_resources)
        self.accumulated_run_time = 0


    ###################################################
    # Get process number (not id)
    ###################################################
    
    def get_process_number(self):
        return self.proc_num

    ###################################################
    # Methods w.r.t process' remaining time and run
    ###################################################

    def get_remaining_time(self):
        return self.req_run_time-self.accumulated_run_time

    def run_proc(self, _run_time_tick):
        self.accumulated_run_time += _run_time_tick

    ###################################################
    # Method to check whether process is finished
    ###################################################
        
    def is_proc_finished(self):
        if self.accumulated_run_time >= self.req_run_time:
            return True
        else:
            return False

    ###################################################
    # Methods w.r.t resources
    ###################################################

    def get_required_resource(self):
        return [a - b for a, b in zip(self.req_resources, self.assigned_resources)]

    def assign_resource(self, _given_resource):
        self.assigned_resources = [a + b for a, b in zip(self.assigned_resources, _given_resource)]
    
    def release_resource(self):
        _released_resources = self.assigned_resources
        self.assigned_resources -= self.assigned_resources
        return _released_resources

    def get_assigned_resource(self):
        return self.assigned_resources


if __name__ == "__main__":

    t_proc_num = 1
    t_req_resources = [1, 2, 1, 2]
    t_req_run_time = 10

    # Generate test process
    test_process = Process(t_proc_num, t_req_resources, t_req_run_time)

    # Check process info
    print("Process number:", test_process.get_process_number())
    print("Required time to run:", test_process.get_remaining_time())
    print("Allocated resources:", test_process.get_assigned_resource())
    print("----------------------------------------")

    # Assign resources
    print("Allocate resource...")
    test_process.assign_resource([1,2,1,2])
    print("Allocated resources:", test_process.get_assigned_resource())

    # Run process
    print("Required time to run:", test_process.get_remaining_time())
    print("----------------------------------------")
    print("Run process for 5 tick...")
    test_process.run_proc(5)
    print("Required time to run:", test_process.get_remaining_time())
    print("Is process finished? (T/F):", test_process.is_proc_finished())
    print("----------------------------------------")
    print("Run process for 5 tick...")
    test_process.run_proc(5)
    print("Required time to run:", test_process.get_remaining_time())
    print("Is process finished? (T/F):", test_process.is_proc_finished())