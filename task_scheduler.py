

def get_process_idx_from_queue(_curr_process, _process_ready_queue, _scheduling_algorithm, _curr_process_run_tick=-1, _time_quantum=-1):
    selected_idx = -1

    # 프로세서의 레디 큐에 프로세스가 존재하지 않을 경우, 스케줄링 알고리즘이 필요 없으므로 -1 을 리턴하도록 합니다.
    if len(_process_ready_queue) == 0:
        return -1
    
    if _scheduling_algorithm == "FCFS":
        selected_idx = first_come_first_served(_curr_process, _process_ready_queue)
    elif _scheduling_algorithm == "RR":
        selected_idx = round_robin(_curr_process, _process_ready_queue, _curr_process_run_tick, _time_quantum)
    elif _scheduling_algorithm == "SJF":
        selected_idx = shortest_job_first(_curr_process, _process_ready_queue)
    elif _scheduling_algorithm == "SRJF":
        selected_idx = shortest_remaining_job_first(_curr_process, _process_ready_queue)

    return selected_idx


# 선입 선출 알고리즘입니다.
#   1. 선입선출 알고리즘은 비선점 알고리즘입니다. 따라서 프로세스에 프로세서가 할당된 상태라면 -1 을 리턴함으로써 비선점을 구현합니다.
#   2. 만약 할당된 프로세스가 없다면 가장 첫번째로 삽입된 프로세스를 리턴하기 위해 0을 리턴합니다.
def first_come_first_served(_curr_process, _process_ready_queue):
    selected_idx = -1
    if _curr_process == None :
        return 0
    return selected_idx


# 라운드 로빈 알고리즘 입니다.
#   1. 선점알고리즘 입니다. 하지만, 타임슬라이스(time_quantum) 만큼의 실행이 되지 않았다면 선점하지 않습니다. 
#       - 따라서, 현재 프로세스가 프로세스에서 몇초만큼 실행이 됬는지를 나타내는 _curr_process_run_tick 와 _time_quantum 을 비교해 리턴값을 결정합니다.
#   2. 라운드로빈은 선입선출과도 유사합니다. 따라서 가장 먼저 삽입된 프로세스의 idx인 0을 리턴합니다. 
def round_robin(_curr_process, _process_ready_queue, _curr_process_run_tick=-1, _time_quantum=-1):
    selected_idx = -1
    if _curr_process_run_tick < _time_quantum :
        return selected_idx
    else :
        return 0


# SJF 알고리즘입니다.
#   1. 비선점형 알고리즘입니다. 따라서 프로세스에 프로세서가 할당된 상태라면 -1 을 리턴함으로써 비선점을 구현합니다.
#   2. 레디큐에 존재하는 모든 프로세스 중에 가장 짧은 실행시간을 가지는 프로세스의 index를 리턴합니다. 
def shortest_job_first(_curr_process, _process_ready_queue):
    selected_idx = -1
    if _curr_process != None:
        return -1
    shortest_time = 999999999
    for i in range(len(_process_ready_queue)):
        if shortest_time > _process_ready_queue[i].req_run_time:
            shortest_time = _process_ready_queue[i].req_run_time
            selected_idx = i
    return selected_idx


# SRJF 알고리즘입니다.
#   1. 선점형 알고리즘입니다. 현재 실행중인 프로세스의 남은 실행시간과 레디큐의 프로세스들의 남은 실행시간을 비교하여 실행할 프로세스의 index를 리턴합니다.
#   2. 실행중인 프로세스가 있는 경우와 없는 경우를 구분하여 실행합니다. 
def shortest_remaining_job_first(_curr_process, _process_ready_queue):
    selected_idx = -1
    if _curr_process != None:
        shortest_process_time = _curr_process.get_remaining_time()
    else :
        shortest_process_time = 999999999
    for i in range(len(_process_ready_queue)):
        temp = _process_ready_queue[i].get_remaining_time()
        if shortest_process_time > temp:
            shortest_process_time = temp
            selected_idx = i
    return selected_idx