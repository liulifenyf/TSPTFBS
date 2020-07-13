import numpy as np
import re
import logging 
# 限定模型文件后缀
ALLOWED_EXTENSIONS = set(['fa'])


# 模型后缀检查函数
def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

def Matrix(seq_list):
        seq_array=[]
        for seq in seq_list:
                # if (re.match('>',line.decode('utf-8')) is None) or (not len(line.decode('utf-8').strip())): 
            value=np.zeros((201,4),dtype='float32')
            for index,base in enumerate(seq.strip()):
                    if re.match(base,'A|a'):
                            value[index,0]=1
                    if re.match(base,'T|t'):
                            value[index,1]=1
                    if re.match(base,'C|c'):
                            value[index,2]=1
                    if re.match(base,'G|g'):
                            value[index,3]=1
            seq_array.append(value)
        # files.close()
        return np.array(seq_array)

def deal_file(args,logger):
    soln = {}
    fa_file = args['uplode_fa_file']
    if allowed_files(fa_file.filename) == False:
        logger.error(fa_file.filename + ' is not a csv file')
        soln["code"] = 100001
        soln['message'] = "请上传正确的文件！"
        return False, soln, None
    lines = fa_file.readlines()
    sample=[]; ids = []
    count = 0
    for line in lines:
        line = line.decode('utf-8')
        count += 1
        if (re.match('>',line) is None) or (not len(line.strip())): 
            if len(line.strip()) != 201:
                logger.error('The length of DNA seq in {} line should be 201!'.format(count))
                soln["code"] = 100002
                soln['message'] = 'The length of DNA seq in {} line should be 201!'.format(count)
                return False, soln, None
            elif 'N' in line.strip().upper():
                logger.error("The DNA seq in {} line contain 'N or n'!".format(count))
                soln["code"] = 100003
                soln['message'] = "The DNA seq in {} line contain 'N or n'!".format(count)
                return False, soln, None
            else:
                sample.append(line)
        elif re.match('>',line): 
                ids.append(line.strip()[1:])    
         
    seq2pre = Matrix(sample)

    rargs = {}
    rargs['seq2pre'] = seq2pre
    rargs['ids'] = ids
    return True, soln, rargs