
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def do_selenium():

    print('Enter the gmailid and password')
    gmailId, passWord = map(str, input().split())
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.get(r'https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id=1036136662547-ambacgqh5pq582hls8g7g5qdl5lvpbmm.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A40847%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&state=LY0crSHGRfzA8hG85AjN2Vems2OCZ7&access_type=offline&flowName=GeneralOAuthFlow')
        driver.get(url)
        driver.implicitly_wait(15)

        # tabIndex = driver.find_element_by_xpath('//*[@tabindex ="0"]')
        # tabIndex.click()

        loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
        # loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
        loginBox.send_keys(gmailId)

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="identifierNext"]')
        nextButton[0].click()

        passWordBox = driver.find_element_by_xpath(
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(passWord)

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="passwordNext"]')
        nextButton[0].click()

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="submit_approve_access"]')
        nextButton[0].click()

        print('Login Successful...!!')
    except:
        print('Login Failed')


if __name__ == "__main__":
    do_selenium()
