import process

VERSION = 1.1

# 자원 할당 관리자의 코드입니다. 
#   - 시뮬레이터 코드에서 대기 큐에 프로세스가 존재하는동안 while문을 통해 반복되도록 구현되었으므로, 자원할당 관리자가 실행될때 하나의 프로세스씩 리턴하도록 구현하였습니다.
def get_process_to_assign_resources(_curr_resource_info, _total_resource_info, _curr_process_waiting_list):
    picked_processes = []
    is_resource_cannot_be_assigned = False

    # waiting_list의 프로세스들의 요청자원을 파악하기 위한 코드입니다.
    for curr_process in _curr_process_waiting_list:
        # 아래 if 문은 프로세스가 시스템 총 자원을 초과하는 자원량을 요청하는지를 확인하여 is_resource_cannot_be_assigned 를 T / F 로 결정합니다.
        # 만일 초과되는 자원를 요청한다면 is_resource_cannot_be_assigned를 True 로 변경하며, 반복문을 탈출합니다. 
        # 또한, is_resource_cannot_be_assigned 변수를 초기에 False로 둠으로써 아래 조건문이 만족될때만 True로 설정되도록 합니다.
        if not all(total >= temp for total , temp in zip(_total_resource_info, curr_process.get_required_resource())):
            is_resource_cannot_be_assigned = True
            break
        # 현재 가용자원과 프로세스가 요청하는 자원량을 비교하여 자원할당이 가능하다면 안전성 검사를 진행합니다.
        #   1. 안전성검사를 통과한다면 picked_processes에 해당 프로세스를 추가하며, 반복문을 탈출합니다.
        #   2. 만일 안전성검사를 통과하지 못한다면 리스트에 추가히자 않고, 다음 프로세스를 탐색합니다.
        if all(temp >= req for temp, req in zip(_curr_resource_info, curr_process.get_required_resource())):
            if run_safety_algorithm(_curr_resource_info, _curr_process_waiting_list, curr_process):
                picked_processes.append(curr_process)
                break

    # 안전성 검사를 통과한 프로세스가 존재할때 실행되는 코드입니다. 
    #   alloc_status로 1을 리턴받은 메인 시뮬레이터는 이 프로세스에 대해 자원을 할당하고, 제일 작은 워크로드를 가진 프로세서를 찾아 레디큐에 프로세스를 할당하고, 대기 큐에서 삭제합니다. 
    if len(picked_processes) > 0:
        return [1, picked_processes]
    # 시스템의 총 자원량보다 많은 수의 자원을 요청할때 실행되는 코드입니다.
    #   alloc_status로 -1을 리턴받은 메인 시뮬레이터는 프로그램을 종료합니다.  
    elif is_resource_cannot_be_assigned:
        return [-1, None]
    # 아래는 두가지 경우를 위함입니다.
    #   1. 현재 자원량으로 프로세스의 요청자원을 할당할 순 있지만, 안정성검사를 통과하지 못한 경우,
    #   2. 현재 자원량으로는 어떤 프로세스의 요청도 들어줄 수 없는 경우입니다. 
    # 자원할당 관리자는 시스템의 현재 가용자원이 더 많아질때까지 자원할당을 미룹니다.
    # 따라서 alloc_status로 0을 리턴받은 메인 시뮬레이터는 while문을 벗어나고, 다음 sim_time에서 자원할당관리자를 다시 실행합니다. 
    else:
        return [0, None]


# 안전성 검사를 위한 코드입니다. 
#   1. 먼저 가용자원량, 대기 큐, 선택된 프로세스를 파라미터로 전달 받습니다.
#   2. 선택된 프로세스가 반환하게 되는 자원을 _curr_resource_info 를 업데이트 하여 사용합니다. 
#       - 프로세스는 대기큐에 있을때 어떤 자원을 이미 할당받은 상태 일 수 있습니다. 미리 할당받았던 자원을 반환함으로써 _curr_resource_info 는 추가적인 자원을 얻게 됩니다.
#   3. 현재 자원으로 할당 가능한 프로세스를 찾을때마다 2번을 반복하며, for문을 처음부터 다시 시작합니다. 
#   4. 위의 결과를 모두 취합하여 대기 큐 내의 프로세스들에 자원을 모두 할당할 수 있다면 True, 아니라면 False를 반환합니다. 
#       - 즉, finish 리스트의 모든 값이 true 라면 true를 반환합니다. 
def run_safety_algorithm(_curr_resource_info, _curr_process_waiting_list, curr_process):
    finish = [False] * len(_curr_process_waiting_list)
    finish[_curr_process_waiting_list.index(curr_process)] = True
    # 아래의 temp_resource 는 안전성 검사를 위해 가용자원과 선택된 프로세스가 가지고 있던 자원을 합한 변수입니다. 
    temp_resource = [i + assigned for i, assigned in zip(_curr_resource_info, curr_process.get_assigned_resource())]

    for i in range(len(_curr_process_waiting_list)):
        if finish[i] == False and all(curr_resource >= req_resource for curr_resource, req_resource in zip(temp_resource, _curr_process_waiting_list[i].get_required_resource())):
            for k in range(len(temp_resource)):
                temp_resource[k] += _curr_process_waiting_list[i].get_assigned_resource()[k]
            finish[i] = True
            i = -1
            
    if False in finish :
        return False
    else :
        return True
