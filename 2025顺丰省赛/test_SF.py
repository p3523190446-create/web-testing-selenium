import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture( scope="function" )
def driver():
    # 提交最终代码脚本时，请将驱动路径换回官方路径"C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"
    service = Service(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe" )
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get( "https://www.sf-express.com/" )
    driver.maximize_window()
    driver.implicitly_wait( 10 )
    yield driver
    driver.quit()


class TestSF:

    # test-code-start

    CASES = [{'id': 'SF_R001_001', 'r': 1, 'origin': ['广州市', '黄埔区'], 'dest': ['南京市', '鼓楼区'], 'details': ['黄埔东苑', '南京大学']}, {'id': 'SF_R001_002', 'r': 1, 'origin': ['南京市', '鼓楼区'], 'dest': ['广州市', '黄埔区'], 'details': ['南京大学', '黄埔东苑']}, {'id': 'SF_R002_001', 'r': 2}, {'id': 'SF_R003_001', 'r': 3}, {'id': 'SF_R004_001', 'r': 4, 'weight': 19, 'dims': [5, 8, 6]}, {'id': 'SF_R004_002', 'r': 4, 'weight': 20, 'dims': [5, 8, 6]}, {'id': 'SF_R004_003', 'r': 4, 'weight': 19, 'dims': [100, 80, 90]}, {'id': 'SF_R004_004', 'r': 4, 'weight': 20, 'dims': [100, 80, 90]}, {'id': 'SF_R005_001', 'r': 5, 'service': '保价'}, {'id': 'SF_R005_002', 'r': 5, 'service': '代收贷款'}, {'id': 'SF_R005_003', 'r': 5, 'service': '签单返还'}, {'id': 'SF_R005_004', 'r': 5, 'service': '包装服务'}, {'id': 'SF_R006_001', 'r': 6, 'city': '上海市', 'district': '黄浦区', 'keyword': '兴业太古汇', 'store': '南京路店'}, {'id': 'SF_R007_001', 'r': 7, 'city': '广州市', 'district': '天河区', 'keyword': '天河花市', 'store': '龙步街店'}, {'id': 'SF_R007_002', 'r': 7, 'city': '深圳市', 'district': '罗湖区', 'keyword': '天虹商场', 'store': '耀华楼店'}, {'id': 'SF_R007_003', 'r': 7, 'city': '南京市', 'district': '玄武区', 'keyword': '新世界百货', 'store': '进香河路店'}, {'id': 'SF_R007_004', 'r': 7, 'city': '杭州市', 'district': '西湖区', 'keyword': '西城广场', 'store': '电信大楼店'}, {'id': 'SF_R008_001', 'r': 8, 'keyword': '电子', 'item': '电子琴'}, {'id': 'SF_R008_002', 'r': 8, 'keyword': '电脑', 'item': '笔记本电脑'}, {'id': 'SF_R009_001', 'r': 9, 'keyword': '猫咪'}, {'id': 'SF_R009_002', 'r': 9, 'keyword': '硫酸'}, {'id': 'SF_R009_003', 'r': 9, 'keyword': '现金'}, {'id': 'SF_R009_004', 'r': 9, 'keyword': '古董'}, {'id': 'SF_R010_001', 'r': 10, 'province': '广东省', 'city': '广州市', 'district': '番禺区', 'street': ''}, {'id': 'SF_R010_002', 'r': 10, 'province': '广东省', 'city': '广州市', 'district': '番禺区', 'street': '大石街道'}, {'id': 'SF_R010_003', 'r': 10, 'province': '新疆维吾尔自治区', 'city': '喀什地区', 'district': '伽师县', 'street': ''}, {'id': 'SF_R010_004', 'r': 10, 'province': '新疆维吾尔自治区', 'city': '喀什地区', 'district': '伽师县', 'street': '米夏乡'}]

    @staticmethod
    def _visible(driver, css):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        return WebDriverWait(driver, 10).until(lambda d: next((e for e in d.find_elements(By.CSS_SELECTOR, css) if e.is_displayed()), False))

    @staticmethod
    def _click(driver, label):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        import time
        e = WebDriverWait(driver, 10).until(lambda d: next((e for e in d.find_elements(By.XPATH, "//*[normalize-space(.)=" + repr(label) + " and not(*[normalize-space(.)=" + repr(label) + "])]") if e.is_displayed()), False))
        driver.execute_script('window.scrollTo(0,0)')
        time.sleep(.2)
        e.click()
        time.sleep(.65)

    @staticmethod
    def _fill(element, value):
        from selenium.webdriver.common.keys import Keys
        import time
        element.click()
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(str(value))
        element.send_keys(Keys.TAB)
        time.sleep(.2)
        assert element.get_attribute('value') == str(value), '输入未被正确保留：' + str(value)

    def _address(self, driver, control, path, mode='search'):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        import time
        control.click();time.sleep(.6)
        if mode == 'search':
            field=self._visible(driver,'.city-search')
            field.send_keys(path[0]);time.sleep(.8)
            e=WebDriverWait(driver,10).until(lambda d: next((e for e in d.find_elements(By.CSS_SELECTOR,'.address-name') if e.is_displayed() and all(s in e.text for s in path)),False))
            e.click();time.sleep(.6)
        else:
            if mode=='hk':self._click(driver,'港澳台')
            elif mode=='province':self._click(driver,'省/直辖市')
            for label in path:self._click(driver,label)

    def _open_store(self,driver,name):
        from selenium.webdriver.common.by import By
        import time
        markers=driver.find_elements(By.CSS_SELECTOR,'.BMap_Marker.BMap_noprint')
        for e in markers[:60]:
            try:
                e.click();time.sleep(.2)
                if name in driver.find_element(By.TAG_NAME,'body').text:return
            except Exception:continue
        raise AssertionError('当前查询地图中未找到指定网点：{}'.format(name))

    def _execute(self, driver, c):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from datetime import datetime, timedelta, timezone
        import time
        driver.get('https://www.sf-express.com/')
        WebDriverWait(driver,20).until(lambda d:d.find_elements(By.TAG_NAME,'body'))
        for e in driver.find_elements(By.XPATH,"//*[normalize-space(.)='不同意']"):
            if e.is_displayed():e.click();break
        self._click(driver,'服务支持')
        r=c['r'];module='运费时效' if r<=5 else '服务网点' if r<=7 else '收寄标准' if r<=9 else '服务范围'
        self._click(driver,module)
        if r<=4:
            WebDriverWait(driver,10).until(lambda d:len(d.find_elements(By.CSS_SELECTOR,'.item-city'))>=2)
            controls=driver.find_elements(By.CSS_SELECTOR,'.item-city')
            self._address(driver,controls[0],c.get('origin',['香港','九龙城区']),'search' if r==1 else 'hk')
            controls=driver.find_elements(By.CSS_SELECTOR,'.item-city')
            self._address(driver,controls[1],c.get('dest',['南京市','鼓楼区']),'search' if r==1 else 'hot')
            if r==1:
                for e,v in zip(driver.find_elements(By.CSS_SELECTOR,'input[placeholder="详细地址（选填）"]'),c['details']):self._fill(e,v)
            self._fill(self._visible(driver,'.weight-field input'),c.get('weight',100 if r==3 else 5))
            for e,v in zip(driver.find_elements(By.CSS_SELECTOR,'.dimension-input input'),c.get('dims',[20,15,25]) if r!=3 else ['','','']):self._fill(e,v)
            driver.find_element(By.CSS_SELECTOR,'.el-date-editor').click();time.sleep(.5)
            if r==2:self._click(driver,'此刻')
            elif r==1:
                driver.find_element(By.CSS_SELECTOR,'.el-date-table td.today').click();self._visible(driver,'.el-date-picker .el-picker-panel__footer button.is-plain').click()
            else:
                day=(datetime.now(timezone(timedelta(hours=8)))+timedelta(days=1 if r==3 else 2)).strftime('%Y-%m-%d')
                self._fill(self._visible(driver,'input[placeholder="选择日期"]'),day)
                self._fill(self._visible(driver,'input[placeholder="选择时间"]'),'15:00:00' if r==3 else '08:00:00')
                self._visible(driver,'.el-date-picker .el-picker-panel__footer button.is-plain').click()
            self._click(driver,'查询')
            WebDriverWait(driver,18).until(lambda d:'快递产品' in d.find_element(By.TAG_NAME,'body').text)
            if r==4:self._click(driver,'大件（20kg+）')
            body=driver.find_element(By.TAG_NAME,'body').text
            section=body.split('快递产品',1)[1].split('其他服务',1)[0]
            assert '我们的产品' in section and ('元' in section or '暂' in section or '20kg以下物品，请选择快递服务' in section),'没有查到完整查询结果'
            driver.execute_script('window.scrollTo(0,0)')
            return '已按指定输入查询；页面结果：'+section[:1600]
        if r==5:
            label=c['service']
            note=''
            if label=='代收贷款':
                label='代收货款'
                note='题面文字“代收贷款”与现页“代收货款”有差异；按同一服务说明进入当前页面。'
            old=driver.current_url;handles=driver.window_handles
            self._click(driver,label);time.sleep(1)
            if len(driver.window_handles)>len(handles):driver.switch_to.window(driver.window_handles[-1])
            WebDriverWait(driver,12).until(lambda d:d.current_url!=old)
            body=driver.find_element(By.TAG_NAME,'body').text
            assert label in body,'跳转后未找到服务名称'
            return note+'跳转至'+driver.current_url+'；'+body[:1400]
        if r<=7:
            self._address(driver,self._visible(driver,'input[placeholder="选择收寄件区域"]'),[c['city'],c['district']],'hot' if r==6 else 'search')
            field=self._visible(driver,'#range-key-word');field.send_keys(c['keyword']);time.sleep(1)
            options=[e for e in driver.find_elements(By.CSS_SELECTOR,'.key-word-query li') if e.is_displayed() and c['keyword'] in e.text]
            if options:options[0].click();time.sleep(.5)
            self._click(driver,'查询');time.sleep(3)
            self._open_store(driver,c['store'])
            if r==6:self._visible(driver,'.BMap_zlCity').click()
            else:
                thumb=self._visible(driver,'.BMap_stdMpSliderBar');track=self._visible(driver,'.BMap_stdMpSlider')
                ActionChains(driver).drag_and_drop_by_offset(thumb,0,-int(track.size['height'])).perform()
                time.sleep(.8)
                assert int(thumb.value_of_css_property('top').replace('px',''))<=1,'缩放滑块未到最顶端'
            body=driver.find_element(By.TAG_NAME,'body').text
            assert c['store'] in body and ('电话' in body or '营业' in body),'网点详情不完整'
            return '已查询、打开网点详情并操作地图缩放；'+body[:1500]
        if r<=9:
            self._address(driver,self._visible(driver,'input[placeholder*="始发地"]'),['广东省','深圳市','光明区'] if r==8 else ['深圳市','南山区'],'province' if r==8 else 'hot')
            self._address(driver,self._visible(driver,'input[placeholder*="目的地"]'),['江苏省','南京市','鼓楼区'] if r==8 else ['香港','湾仔区','铜锣湾'],'province' if r==8 else 'hk')
            if r==9:
                self._click(driver,'请选择寄件人身份');self._click(driver,'个人');self._click(driver,'请选择收件人身份');self._click(driver,'公司')
            field=self._visible(driver,'input[placeholder*="托寄物品"]');field.send_keys(c['keyword']);time.sleep(.8)
            if r==8:self._click(driver,c['item'])
            self._click(driver,'查询');time.sleep(2)
            body=driver.find_element(By.TAG_NAME,'body').text
            section=self._visible(driver,'.result-box').text
            assert '暂无查询结果' in section or (c.get('item',c['keyword']) in section and '收寄' in section),'查询结果未出现'
            driver.execute_script('window.scrollTo(0,0)')
            return '查询结果：'+section
        self._address(driver,self._visible(driver,'input[placeholder="选择收寄件区域"]'),[c['province'],c['city'],c['district']])
        if c['street']:
            self._visible(driver,'input[placeholder*="乡/镇/街道"]').click();self._click(driver,c['street'])
        self._click(driver,'查询')
        WebDriverWait(driver,18).until(lambda d:c['district'] in d.find_element(By.TAG_NAME,'body').text and ('可达' in d.find_element(By.TAG_NAME,'body').text or '收件服务区域' in d.find_element(By.TAG_NAME,'body').text))
        body=driver.find_element(By.TAG_NAME,'body').text
        assert c['district'] in body and ('全境街道/乡镇可达' in body or '全境行政村可达' in body or '收件服务区域' in body),'未识别到指定区域服务范围结果'
        if c['street']:assert c['street'] in body,'街道未带入结果'
        driver.execute_script('window.scrollTo(0,0)')
        return '已查询指定区域和街道；'+body[:1600]

    def _run_case(self, driver, c):
        import json,time
        from pathlib import Path
        from selenium.webdriver.common.by import By
        rec={'id':c['id'],'input':c,'status':'未通过'}
        try:
            rec['actual']=self._execute(driver,c);rec['status']='通过'
        except Exception as exc:
            rec['actual']=type(exc).__name__+': '+str(exc).split('Stacktrace:')[0][:1200]
        finally:
            # 原版截图函数不作修改；每条只调用一次，失败现场也是实际证据。
            self.take_screenshot(driver,c['id']+'.png')
            files=list(Path('screenshots').glob('*_'+c['id']+'.png'))
            rec['screenshot']=max(files,key=lambda f:f.stat().st_mtime).name
            rec['url']=driver.current_url
            rec['observed_text']=driver.find_element(By.TAG_NAME,'body').text[:16000]
            Path('results').mkdir(exist_ok=True)
            Path('results',c['id']+'.html').write_text(driver.page_source,encoding='utf-8')
            Path('results').mkdir(exist_ok=True)
            Path('results',c['id']+'.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
        return rec

    def _group(self,driver,r):
        results=[self._run_case(driver,c) for c in self.CASES if c['r']==r]
        assert all(c['status']=='通过' for c in results), '; '.join(c['id']+' '+c['actual'][:150] for c in results if c['status']!='通过')

    def test_SF_R001(self, driver):
        self._group(driver,1)

    def test_SF_R002(self, driver):
        self._group(driver,2)

    def test_SF_R003(self, driver):
        self._group(driver,3)

    def test_SF_R004(self, driver):
        self._group(driver,4)

    def test_SF_R005(self, driver):
        self._group(driver,5)

    def test_SF_R006(self, driver):
        self._group(driver,6)

    def test_SF_R007(self, driver):
        self._group(driver,7)

    def test_SF_R008(self, driver):
        self._group(driver,8)

    def test_SF_R009(self, driver):
        self._group(driver,9)

    def test_SF_R010(self, driver):
        self._group(driver,10)

    # test-code-end

    @staticmethod
    def take_screenshot(driver, file_name):
        timestamp = datetime.now().strftime( "%H%M%S%d%f" )[:-3]
        timestamped_file_name = f"{timestamp}_{file_name}"
        screenshots_dir = "screenshots"
        if not os.path.exists( screenshots_dir ):
            os.makedirs( screenshots_dir )
        screenshot_file_path = os.path.join( screenshots_dir, timestamped_file_name )
        driver.save_screenshot( screenshot_file_path )
