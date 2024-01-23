import os.path


def convert(file_path):
    """
    Convert purchased twitter list with this format:\n
    DoriaBruni45661----UQSH1024l----sallhiwuwuw@hotmail.com----HIiuvUp61----6R6OTNQKMM36ITCV----9fc6f13b42ce466049cdc8906fd2f02f2239f947 \n
    To this format: \n
    DoriaBruni45661,UQSH1024l,sallhiwuwuw@hotmail.com,HIiuvUp61,6R6OTNQKMM36ITCV,9fc6f13b42ce466049cdc8906fd2f02f2239f947 \n

    :param file_path:
    :return:
    """
    file_path = os.path.join(os.getcwd(), file_path)
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    results = []
    for line in lines:
        account_credential = line.split('----')
        account_credential[-1] = account_credential[-1].rstrip()
        account_credential = ','.join(account_credential)
        results.append(account_credential)
    return results


def convert_and_output(file_path, target_file_path):
    converted_list = convert(file_path)
    with open(target_file_path, 'w') as target_file:
        target_file.write('\n'.join(converted_list))