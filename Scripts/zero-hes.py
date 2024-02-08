with open('frozen.txt', 'r') as input_file:
    frozen_opt = []
    
    for line in input_file:
        if line.startswith('$frozen_opt'):
            for line in input_file:
                if line.startswith('$end'):
                    break
                frozen_opt.extend(line.split())
                    
    with open('output.txt', 'w') as output_file:
        output_file.write('$opt\nFIXED\n')
        for option in frozen_opt:
            output_file.write(f'{option:<4}XYZ\n')
        output_file.write('ENDFIXED')
        output_file.write('$end')

