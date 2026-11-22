"""本地练习启动器：使用Selenium Manager，原赛题驱动路径保留在test_SF.py。"""
import os,json,argparse
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from test_SF import TestSF
p=argparse.ArgumentParser();p.add_argument('--ids',nargs='*');p.add_argument('--show',action='store_true');args=p.parse_args()
here=Path(__file__).resolve().parent
run=here/'运行记录'/datetime.now().strftime('%Y%m%d-%H%M%S');run.mkdir(parents=True);os.chdir(run)
os.environ['SE_AVOID_STATS']='true'
options=webdriver.ChromeOptions()
if not args.show:options.add_argument('--headless=new')
options.add_argument('--window-size=1600,1200')
d=webdriver.Chrome(options=options);d.set_page_load_timeout(35)
records=[]
try:
 for c in TestSF.CASES:
  if args.ids and c['id'] not in args.ids:continue
  for handle in d.window_handles[1:]:d.switch_to.window(handle);d.close()
  d.switch_to.window(d.window_handles[0])
  rec=TestSF()._run_case(d,c);records.append(rec)
  print(c['id'],rec['status'],rec['actual'][:160],flush=True)
finally:
 (run/'summary.json').write_text(json.dumps({'browser':d.capabilities.get('browserVersion'),'results':records},ensure_ascii=False,indent=2),encoding='utf-8')
 d.quit()
print('RUN',run,flush=True)
