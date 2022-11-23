import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CSS_SEL_FE_ERR_MSG_CONTENT = "tbody .ds-u-text-align--left:nth-child(2)"


class TestNodeSampleApp():
    driver_ready = False

    def setup_method(self, method):
        if not TestNodeSampleApp.driver_ready:
            time.sleep(20)
            TestNodeSampleApp.driver_ready = True
            print("set driver_ready={}".format(TestNodeSampleApp.driver_ready))
        else:
            print("driver_ready={}".format(TestNodeSampleApp.driver_ready))

        opt = webdriver.ChromeOptions()
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-web-security")
        opt.add_argument("--allow-running-insecure-content")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("--disable-popup-blocking")
        opt.add_argument("--enable-javascript")
        opt.add_argument('--allow-insecure-localhost')
        opt.add_argument('--window-size=1920,1080')
        opt.add_argument("--whitelisted-ips=''")

        # opt.add_argument('--headless')
        # self.driver = webdriver.Chrome(options=opt)
        self.driver = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub', options=opt)

    def teardown_method(self, method):
        self.driver.quit()

    def _find_elem_xpath(self, xpath_expr, **kwargs):
        elems = self.driver.find_elements(By.XPATH, xpath_expr)
        assert elems is not None
        return elems

    def _find_and_click(self, timeout_sec, by, by_expr, **kwargs):
        elem = WebDriverWait(self.driver, timeout_sec).until(
            EC.visibility_of_element_located((by, by_expr)))
        assert elem is not None
        elem.click()
        return elem

    def _find_and_return(self, timeout_sec, by, by_expr, **kwargs):
        elem = WebDriverWait(self.driver, timeout_sec).until(
            EC.visibility_of_element_located((by, by_expr)))
        assert elem is not None
        return elem

    def _find_and_sendkey(self, timeout_sec, by, by_expr, txt, **kwargs):
        elem = WebDriverWait(self.driver, timeout_sec).until(
            EC.visibility_of_element_located((by, by_expr)))
        assert elem is not None
        elem.send_keys(txt)
        return elem

    def _assert_EOB_table_header_present(self):       
        self._find_and_return(30, By.ID, "column_1")
        self._find_and_return(30, By.ID, "column_2")
        self._find_and_return(30, By.ID, "column_3")

    def _assert_EOB_table_records_present(self, cnt):
        xpath = "//table/tbody/tr/td[@data-title='NDC Code']"
        elements = self._find_elem_xpath(xpath)
        assert len(elements) == cnt

    def _assert_EOB_table_error_present(self):
        element = self._find_and_return(30,
                                        By.CSS_SELECTOR,
                                        CSS_SEL_FE_ERR_MSG_CONTENT)
        assert element is not None
        print(element.text)

    def _input_user_and_passwd_and_login(self):
        self._find_and_sendkey(30, By.ID, "username-textbox", "BBUser10000")
        self._find_and_sendkey(30, By.ID, "password-textbox", "PW10000!")
        self._find_and_click(30, By.ID, "login-button")

    def test_node_sample_app_grant_access(self):
        self.driver.get("http://client:3000/")
        self.driver.set_window_size(1500, 1800)
        elem = self._find_and_click(30, By.ID, "auth_btn")
        assert elem is not None
        self._input_user_and_passwd_and_login()
        self._find_and_click(30, By.ID, "approve")
        time.sleep(5)
        self._assert_EOB_table_header_present()
        self._assert_EOB_table_records_present(10)

    def test_node_sample_app_grant_access_no_demographic(self):
        self.driver.get("http://client:3000/")
        self.driver.set_window_size(1500, 1800)
        elem = self._find_and_click(30, By.ID, "auth_btn")
        assert elem is not None
        self._input_user_and_passwd_and_login()
        # select radio button "No Demographic Data"
        self._find_and_click(30, By.CSS_SELECTOR, "label:nth-child(5)")
        self._find_and_click(30, By.ID, "approve")
        time.sleep(5)
        self._assert_EOB_table_header_present()
        self._assert_EOB_table_records_present(10)

    def test_node_sample_app_deny_access(self):
        self.driver.get("http://client:3000/")
        self.driver.set_window_size(1500, 1800)
        elem = self._find_and_click(30, By.ID, "auth_btn")
        assert elem is not None
        self._input_user_and_passwd_and_login()
        self._find_and_click(30, By.ID, "deny")
        time.sleep(5)
        self._assert_EOB_table_error_present()

    def test_node_sample_app_grant_followed_by_deny_access(self):
        '''
        this is to verify that the cached result from previous
        authorized eob query is clean up (should not see cached claims)
        '''
        self.driver.get("http://client:3000/")
        self.driver.set_window_size(1500, 1800)
        elem = self._find_and_click(30, By.ID, "auth_btn")
        assert elem is not None
        self._input_user_and_passwd_and_login()
        self._find_and_click(30, By.ID, "approve")
        time.sleep(5)
        self._assert_EOB_table_records_present(10)
        # go again
        elem = self._find_and_click(30, By.ID, "auth_btn")
        assert elem is not None
        self._input_user_and_passwd_and_login()
        self._find_and_click(30, By.ID, "deny")
        time.sleep(5)
        # should see error message
        self._assert_EOB_table_error_present()
