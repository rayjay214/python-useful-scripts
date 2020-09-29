'''
破解亿赛通软件，亿赛通只对某些指定后缀名的文件加密存储
上传到非加密服务器之后再将其后缀名还原
'''
import os
from chardet import detect

g_ext_trans_dict = {'.cpp':'.ctt', '.h':'.htt'}
g_ext_trans_dict_reverse = {'.ctt':'.cpp', '.htt':'.h'}

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
    with open(file_path, 'r', encoding='utf8') as f:
        content = f.read()
    with open(new_file_path, 'w', encoding='utf8') as f:
        f.write(content)
    os.remove(file_path)

#所有文件先统一编码成utf8
def encode_to_utf8(root, file):
    file_path = os.path.join(root, file)
    with open(file_path, 'rb+') as fp:
        content = fp.read()
        encoding = detect(content)['encoding']
        content = content.decode(encoding, 'ignore').encode('utf8')
        fp.seek(0)
        fp.write(content)
 
def tranverse():
    for root, dirs, files in os.walk('.'):
        for file in files:
            ext = os.path.splitext(file)[1]
            if g_ext_trans_dict.get(ext, None) is not None:
                encode_to_utf8(root, file)
                rename_to_unencrpt_ext(root, file, ext)

            elif g_ext_trans_dict_reverse.get(ext, None) is not None:
                revert_file_ext(root, file, ext)

if __name__ == '__main__':
    tranverse()
