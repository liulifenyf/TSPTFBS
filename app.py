# -*- coding: utf-8 -*-
"""
Created on Tue nov 5 14:40:06 2019

@author: ZHY

Change Format and 3nd edition: on Mon Feb 26 12:40:24 2020 (DS,YYK)
"""
import os
import logging
from flask_restplus import Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import predict_function as pf
from processing import *
from werkzeug.datastructures import FileStorage
import traceback ##
import detection_function as detect

dirpath = os.path.dirname(os.path.realpath(__file__))

# 创建一个logger格式
formatter = logging.Formatter('-%(asctime)s - %(levelname)s - %(message)s')
loggername = 'log'
logPath = os.path.join('/file_and_log', loggername + '.log')
logger = logging.getLogger(loggername)
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler(loggername + '.log', encoding='utf8')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# 限定模型文件后缀
ALLOWED_EXTENSIONS = set(['fa'])


# 模型后缀检查函数
def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS


# 简历api参数
app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决前端请求跨域问题******
# 支持swagger
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='拟南芥转录因子结合位点预测 API')

ns_iba = api.namespace('Predicting_operate', description='上传fasta文件进行拟南芥转录因子结合位点预测，预测时间耗时较长请耐心等待！')


# 健康检测接口
@app.route('/healthz')
def healthz():
    return "OK"


# 配置参数装饰器
Predicting_parser = reqparse.RequestParser()
Predicting_parser.add_argument('uplode_fa_file', location='files', type=FileStorage, required=True, help='上传fasta文件')

# Predicting接口
@ns_iba.route('/Predicting')
@ns_iba.expect(Predicting_parser)
# 接口运行函数配置
class Predict(Resource):
    # 通过post 上传、处理文件并返回json文件
    def post(self):
        '''
        文件上传接口，将返回计算得到的预测概率。
        输入：长度为201bp的带预测的fasta文件
        输出：fasta文件中每条序列的id号和预测为对应结合位点概率的文件
        '''
        # 取参数字典
        logger.info("Starting to get file!")
        args = Predicting_parser.parse_args()
        
        soln = {}  # 初始化结果
        logger.info(str(args))
        # 处理参数   ##
        key, conta, rargs = detect.deal_file(args, logger)
        if key == True:
            soln = conta
            args = rargs
        elif key == False:
            soln = conta
            logger.error(str(soln))
            return jsonify(soln)
        else:
            logger.error("Function deal_file() goes wrong!")
            soln["code"] = 100004
            soln['message'] = "文件处理函数错误！"
            #soln = conta
            logger.info(str(soln))
            return jsonify(soln)
        # 获取one-hot矩阵，和每条序列对应的ID号，一般为染色体位置。
        seq2pre, ids = args['seq2pre'], args['ids']
        logger.info("Starting calculations!")
        # 启动主函数
        pf.main(seq2pre, ids)
        # 返回的字典
        soln["code"] = 0
        soln['message'] = {"consequence": "请求成功"}
        logger.info(str(soln))
        logger.info("Program finished.")
        return send_from_directory(dirpath, filename="result.csv", as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

