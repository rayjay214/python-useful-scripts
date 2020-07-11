'''
破解亿赛通软件，亿赛通只对某些指定后缀名的文件加密存储
上传到非加密服务器之后再将其后缀名还原
'''
import os

g_ext_trans_dict = {'.cpp':'.app', '.h':'.hpp'}
g_ext_trans_dict_reverse = {'.app':'.cpp', '.hpp':'.h'}

#非加密服务器上调用
def revert_file_ext(root, file, ext):
    new_file = os.path.splitext(file)[0] + g_ext_trans_dict_reverse[ext]
    file_path = os.path.join(root, file)
    new_file_path = os.path.join(root, new_file)
    os.rename(file_path, new_file_path)

#装有亿赛通的windows机器上调用
def rename_to_unencrpt_ext(root, file, ext):
    new_file = os.path.splitext(file)[0] + g_ext_trans_dict[ext]
    file_path = os.path.join(root, file)
    new_file_path = os.path.join(root, new_file)
    print(new_file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    with open(new_file_path, 'w') as f:
        f.write(content)
    os.remove(file_path)

def tranverse():
    for root, dirs, files in os.walk('.'):
        for file in files:
            ext = os.path.splitext(file)[1]
            if g_ext_trans_dict.get(ext, None) is not None:
                rename_to_unencrpt_ext(root, file, ext)

            elif g_ext_trans_dict_reverse.get(ext, None) is not None:
                revert_file_ext(root, file, ext)

if __name__ == '__main__':
    tranverse()
