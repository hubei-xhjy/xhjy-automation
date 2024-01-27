# Let's say we got 20 pcs of machine, and need them to work 5 by 5
import math

work_machines = ['3001', '3002', '3003', '3004', '3005', '3006', '3007', '3008', '3009', '3010',
                 '3011', '3012', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3020',
                 '3021', '3022', '3023']

machine_to_work_per_round = 5

for i in range(math.ceil(len(work_machines) / machine_to_work_per_round)):
    batch_machine = work_machines[i * machine_to_work_per_round: i * machine_to_work_per_round + machine_to_work_per_round]
    print(f'Starting round {i} with {batch_machine}')
    for machine in batch_machine:
        print(machine)

