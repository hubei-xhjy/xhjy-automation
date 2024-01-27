import pandas as pd

# 读取原始CSV文件
original_df = pd.read_csv('../private/100_Twitters.csv')

# 创建新的DataFrame用于存储合并后的数据
machine_info_columns = [
    'AdsSerialNo', 'Ip', 'Email', 'Password', 'MetamaskMnemonic',
    'MetamaskPublicKey', 'MetamaskPrivateKey', 'MetamaskPassword',
    'TwitterUsername', 'TwitterPassword', 'Twitter2FA', 'TwitterToken'
]
machine_info_df = pd.DataFrame(columns=machine_info_columns)

# 生成AdsSerialNo列
machine_info_df['AdsSerialNo'] = range(3001, 3001 + len(original_df))

# 将原始数据添加到machine_info_df中
machine_info_df['Email'] = original_df['Email']
machine_info_df['Password'] = original_df['EmailPassword']
machine_info_df['TwitterUsername'] = original_df['Username']
machine_info_df['TwitterPassword'] = original_df['Password']
machine_info_df['Twitter2FA'] = original_df['2FA']
machine_info_df['TwitterToken'] = original_df['Token']

# 填充其他列（如果需要）

# 将数据写入machine_info.csv
machine_info_df.to_csv('../private/machine_info.csv', index=False)
