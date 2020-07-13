#查看lv某款包包是否有货，windows上执行
#查看lv某款包包是否有货，windows上执行
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText

def send_mail(content):
	HOST = 'smtp.qq.com'
	FROM = '564546422@qq.com'
	PWD = 'xgjzpddkpumubbha'
	SUBJECT = '通知'
	TO = ['564546422@qq.com']

	msg = MIMEText(content)
	msg['Subject'] = SUBJECT
	msg['From'] = FROM
	msg['To'] = ','.join(TO)
	try:
		server = smtplib.SMTP_SSL(HOST, 465)
		server.login(FROM, PWD)
		server.sendmail(FROM, TO, msg.as_string())
		server.quit()
		print("Send email succeed!")
	except Exception as e:
		print("Send email error: %s" % e.args[0])
	
def get_once():
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"')
	path = r'C:\Users\slxk-20161026\AppData\Local\Google\Chrome\Application\chromedriver'
	browser = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
	
	try:
		browser.get('https://www.louisvuitton.cn/zhs-cn/products/pochette-accessoires-monogram-005656')
		body = browser.find_element_by_tag_name('body')
		target = body.get_attribute('data-pv-product-stock-status')
		print('here is target {}'.format(target))
		if(str(target) == 'instock'):
			send_mail(str(target))
	except Exception as e:
		print('error {}'.format(e))

if __name__ == '__main__':
	while True:
		get_once()
		time.sleep(30)

