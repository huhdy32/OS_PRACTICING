import os
import random
import process
import processor
import resource_manager

# ENVIRONMENTAL VARIABLES

# - Processor configuration
NUM_PROCESSORS = 2
PROCESSOR_SCHEDULING_ALGORITHM = "RR"
# FCFS, RR, SJF, etc.

# - Dispatch schedule
RANDOM_DISPATCH_SCHEDULE = True
DISPATCH_FILE_PATH = "./data/dispatch_schedule.txt"

# - Process generation
NUM_PROCESSES = 20
MAX_PROCESS_RUN_TIME = 10
PROCESS_GENERATION_TIME_LIMIT = 20

# - Resource constraints
NUM_OF_RESOURCE_TYPES = 5
GIVEN_RESOURCES = [5, 5, 5, 5, 5]

class ProcessSimulator(object):

    sim_time = 0
    proc_num = 1
    is_solvable = True

    scheduling_algorithm = "FCFS"
    processor_list = []
    curr_run_process_list = []

    process_waiting_list = []
    processor_ready_list = []
    processor_assign_list = []

    process_dispatch_schedule = []

    def __init__(self, _num_processors, _scheduling_algorithm) -> None:
        self.processor_list = []
        self.process_waiting_list = []

        # generate simulation environment
        self.sim_time = 0
        self.proc_num = 1
        self.is_solvable = True
        self.num_processors = _num_processors

        # Generate processors
        for i in range(0, _num_processors):
            t_processor = processor.Processor(_scheduling_algorithm)
            self.processor_list.append(t_processor)
            self.curr_run_process_list.append(-1)

    def increase_tick(self):
        self.sim_time += 1
    
    def read_dispatch_schedule_from_file(self, _file_path):
        pass

    def generate_random_dispatch_schedule(self, _num_of_processes=10, _max_proc_run_tick=1, _proc_gen_time_limit=10):
        self.process_dispatch_schedule = []

        proc_dispatch_time = [random.randint(0, PROCESS_GENERATION_TIME_LIMIT) for p in range(0, NUM_PROCESSES)]
        proc_dispatch_time.sort()

        print("================================================")
        print("Generated tasks: [task number, dispatch time, expected run time, required resources]")

        for i in range(0, _num_of_processes):
            # Generate random process run time
            t_proc_run_time = random.randint(1,_max_proc_run_tick)

            t_required_resources = [0]*NUM_OF_RESOURCE_TYPES
            for j in range(0, NUM_OF_RESOURCE_TYPES):
                t_required_resources[j] = random.randint(0, round(GIVEN_RESOURCES[j]/2))
            self.process_dispatch_schedule.append([i+1, proc_dispatch_time[i], t_proc_run_time, t_required_resources])
            print([i+1, proc_dispatch_time[i], t_proc_run_time, t_required_resources])
        print("================================================")

    def generate_new_process(self, _required_run_time, _required_resource_info):
        proc_num_to_assign = self.proc_num
        self.proc_num += 1
        return process.Process(proc_num_to_assign, _required_resource_info, _required_run_time)

    
    def put_process_to_waiting_list(self, _process_to_put):
        self.process_waiting_list.append(_process_to_put)

    def get_process_waiting_list(self):
        return self.process_waiting_list
    
    def put_process_to_ready_list(self, _process_to_put):
        self.processor_ready_list.append(_process_to_put)

    def get_processor_ready_list(self):
        return self.processor_ready_list

    def get_processor_list(self):
        return processor_list

    def get_dispatch_schedule(self):
        return self.process_dispatch_schedule

    def get_curr_sim_time(self):
        return self.sim_time
    
    def generate_processes_with_info(self, _req_run_time, _req_resource_info):
        t_process = simulator.generate_new_process(_req_run_time, _req_resource_info)

        return t_process
    
    def generate_processes_with_schedule_info(self, _sim_time, _req_run_time):
        if len(self.process_dispatch_schedule) > 0:
            while self.process_dispatch_schedule[0][0] == _sim_time:

                t_proc_info = self.process_dispatch_schedule[0]
                # [process_dispatch_time, required_resource_info, required_run_time]

                # generate process and add the process to ready list
                t_process = simulator.generate_new_process(t_proc_info[2], t_proc_info[3])
                simulator.put_process_to_ready_list(t_process)


if __name__ == "__main__":
    # Check code version
    is_all_files_up_to_date = True
    if hasattr(process, 'VERSION'):
        if process.VERSION != 1.1:
            is_all_files_up_to_date = False
            print("ERROR: process.py update required.")
    else:
        is_all_files_up_to_date = False
        print("ERROR: process.py update required.")

    if hasattr(processor, 'VERSION'):
        if processor.VERSION != 1.1:
            is_all_files_up_to_date = False
            print("ERROR: processor.py update required.")
    else:
        is_all_files_up_to_date = False
        print("ERROR: processor.py update required.")

    if hasattr(resource_manager, 'VERSION'):
        if resource_manager.VERSION != 1.1:
            is_all_files_up_to_date = False
            print("ERROR: resource_manager.py update required.")
    else:
        is_all_files_up_to_date = False
        print("ERROR: resource_manager.py update required.")

    if is_all_files_up_to_date:
        print("All files are up to date!")
        print()
    else:
        print("Files have to be updated!!")
        exit()

    # Environment variables
    num_processors = NUM_PROCESSORS
    current_resources = GIVEN_RESOURCES
    scheduling_algorithm = PROCESSOR_SCHEDULING_ALGORITHM

    processor_list = [None]*NUM_PROCESSORS

    # 1. Initialize
    #    i) Generate processors
    #    ii) Set task scheduling algorithm to the processors' task queues
    simulator = ProcessSimulator(num_processors, scheduling_algorithm)

    # 2. Generate processes dispatch schedule
    # open file
    # while reach to the EOF, put process dispatch schedule
    if RANDOM_DISPATCH_SCHEDULE:
        simulator.generate_random_dispatch_schedule(NUM_PROCESSES, MAX_PROCESS_RUN_TIME)
    else:
        simulator.read_dispatch_schedule_from_file(DISPATCH_FILE_PATH)
    
    proc_dispatch_schedule = simulator.get_dispatch_schedule().copy()

    is_sim_finish = False

    print("#PROC #TICK : PROC ID     | # CPU WAIT | # WAITING QUEUE | CURRENT RESORUCES")
    print("-------------------------------------------------------------------------------")

    while not is_sim_finish:
        is_sim_finish = False
        is_task_in_processing = True
        is_dispatched_tasks_exists = False

        # 1.
        #   i) Update current status
        curr_sim_time = simulator.get_curr_sim_time()
        curr_processor_info = simulator.get_processor_list()
        curr_dispatch_schedule = simulator.get_dispatch_schedule()

        # 2.
        #   i) Generate process based on dispatch schedule
        #   ii) If there is no job in process or waiting, ready, terminate simulation
        if len(curr_dispatch_schedule) > 0:
            is_sim_finish = False
            is_dispatched_tasks_exists = True

            is_process_dispatched = True
            while is_process_dispatched:
                is_process_dispatched = False
                for i in range(0, len(curr_dispatch_schedule)):
                    if curr_dispatch_schedule[i][1] == curr_sim_time:
                        t_process = simulator.generate_processes_with_info(curr_dispatch_schedule[i][2], curr_dispatch_schedule[i][3])
                        simulator.put_process_to_waiting_list(t_process)
                        is_process_dispatched = True
                        del curr_dispatch_schedule[i]
                        break
            else:
                pass
        else:
            is_task_in_processing = False
            for i in range(0, num_processors):
                if simulator.processor_list[i].curr_process is not None:
                    is_task_in_processing = True
        
        is_ready_task_exists = False
        for i in range(0, num_processors):
            if len(simulator.processor_list[i].processor_ready_queue) > 0:
                is_ready_task_exists = True
        
        if is_sim_finish is False and is_task_in_processing is False and is_ready_task_exists is False and is_dispatched_tasks_exists is False:
            is_sim_finish = True
        else:
            is_sim_finish = False
            
        # 4.
        #   i)   Check available/required resources
        #   ii)  Allocate resources to process
        #   iii) Put the process to ready queue
        curr_process_waiting_list = simulator.get_process_waiting_list()

        while len(curr_process_waiting_list) > 0:
            # i) Run resource manager to pick process 
            [alloc_status, picked_processes] = resource_manager.get_process_to_assign_resources(current_resources, GIVEN_RESOURCES, curr_process_waiting_list)

            if alloc_status == -1:
                simulator.is_solvable = False
                is_sim_finish = True
                print("ERROR: PROBLEM NOT SOLVABLE!! (Resource cannot be assigned forever)")
                break
            elif alloc_status == 0:
                # Processes have to be wait until resource is available
                break
                pass
            elif alloc_status == 1:
                # ii) Allocate resource to the process
                for i in range(0, len(picked_processes)):
                    t_required_resources = picked_processes[i].get_required_resource()
                    picked_processes[i].assign_resource(t_required_resources)
                    current_resources = [a - b for a, b in zip(current_resources, t_required_resources)]

                # iii) Put process to processor(=CPU)'s ready queue
                for j in range(0, len(picked_processes)):
                    min_work_load = 100000000000
                    min_processor_idx = -1
                    for i in range(0, num_processors):
                        # get processor's workload
                        t_processor_workload = simulator.processor_list[i].get_total_workload()
                        if t_processor_workload < min_work_load:
                            min_processor_idx = i
                            min_work_load = t_processor_workload
                    
                    simulator.processor_list[min_processor_idx].put_process_to_ready_queue(picked_processes[j])
                    curr_process_waiting_list.remove(picked_processes[j])
            else:
                simulator.is_solvable = False
                is_sim_finish = True
                print("ERROR OCCURED!!")
                break
        
        if simulator.is_solvable is False:
            break
        
        if len(curr_process_waiting_list) > 0:
            is_sim_finish = False
        
        # 5.
        #   i) Assign and Run processes
        print(" P{0:03d}  T{1:03d} :".format(num_processors, simulator.get_curr_sim_time()), end=" ")

        for i in range(0, num_processors):
            simulator.processor_list[i].check_and_assign_process()

        for i in range(0, num_processors):
            if simulator.processor_list[i].curr_process is None:
                print("--", end=" ")
            else:
                print("{0:2d}".format(simulator.processor_list[i].curr_process.get_process_number()), end=" ")
            simulator.processor_list[i].run_process()

        print("|", end=" ")

        for i in range(0, num_processors):
            if len(simulator.processor_list[i].processor_ready_queue) == 0:
                print("*", end=" ")
            else:
                print("{0}".format(len(simulator.processor_list[i].processor_ready_queue)), end=" ")


        for i in range(0, num_processors):
            returned_resources = simulator.processor_list[i].cleanup_process()
            if returned_resources is not None:
                current_resources = [a + b for a, b in zip(current_resources, returned_resources)]

        # print("Remaining dispatch schedule:", curr_dispatch_schedule)
        # print(curr_process_waiting_list, end="")

        print("   | {0}".format(len(curr_process_waiting_list)), end="")
        print("               | {0}".format(current_resources), end="")

        simulator.increase_tick()
        input()


    print("Finish!")
    pass
