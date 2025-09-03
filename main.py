#main파일에는 뭐가 있어야할까?
'''
1. 데이터셋을 불러오는 코드가 있어야겠다.
2. 다른 폴더들에서 만든 함수들을 import할 필요가 있겠다.
3. main파일을 실행하면 한 번에 다 동작하게 해야겠다.
'''
import warnings #파이썬 실행 중에 나오는 경고 메세지를 다루는 모듈
warnings.filterwarnings('ignore') #모든 종류의 경고메세지에 대해서 화면에 표시하지 말라는 뜻

import logging #파이썬 내장모듈/ 프로그램 실행 중에 로그 메세지를 출력하거나 파일에 저장할 수 있음
logging.basicConfig(level=logging.INFO) #info이상 레벨만 보이게 해줌

import argparse

from .service.data_setup import load_dataset




# 데이터셋을 불러오는 함수를 만들자
def main(args):
    # data load
    pass