#-*- coding: utf-8 -*-
try:
    from tqdm import tqdm
    import time
except:
    exit('[ERROR!][waiting] no required modules')

def waiting(wait_time, wait_desc):
    with tqdm(total=wait_time, desc=wait_desc) as pbar:
        for i in range(1,wait_time):
            time.sleep(1)
            pbar.update(1)
        pbar.close()