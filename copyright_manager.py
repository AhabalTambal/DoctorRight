from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import *
from selenium import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time


class links:
    video_manager = 'https://www.youtube.com/my_videos?o=U'


class copyright_actions:
    remove_song_option = 'remove song'
    remove_song_action = 'remove this song'
    save_copyright_action = 'save as new video'


REMOVE_MUSIC_TOKEN = u'\u05d4\u05e1\u05e8 \u05d0\u05ea \u05d4\u05e9\u05d9\u05e8'


def delete_old_videos(to_delete_urls):
    click_counter = 0
    driver.get(links.video_manager)
    time.sleep(5)

    videos = driver.find_elements_by_class_name('vm-video-item-content')
    for video in videos:
        try:
            video_url = video.find_element_by_class_name(
                'vm-video-side-notification-text-item').find_element_by_tag_name('a').get_attribute('href')
            if video_url in to_delete_urls:
                video.find_element_by_css_selector('.video-checkbox').click()
                click_counter += 1
        except Exception:
            pass
    if click_counter > 0:
        # click on action button
        driver.find_elements_by_class_name('vm-video-list-action-menu')[1].click()
        driver.save_screenshot('lol.jpg')

        # click the delete action
        filter(lambda label: label.text.lower() == 'Delete'.lower(),
               driver.find_elements_by_class_name('yt-ui-menu-item-label'))[0].click()

        driver.save_screenshot('lol1.jpg')
        # confirm deletion
        driver.find_element_by_class_name('vm-video-actions-delete-button-confirm').click()

def solve_problem(copyright_urls):
    for copyright_url in copyright_urls:
        driver.get(copyright_url)
        copyright_options = wait.until(lambda driver: driver.find_elements_by_class_name('copynotice-options'))
        for option in copyright_options:
            if option.text.lower() == copyright_actions.remove_song_option.lower():
                main_window = driver.current_window_handle
                link = option.find_element_by_tag_name('a')
                link.click()
                time.sleep(5)

                # Switch focus to the new opening tab
                remove_song_window = driver.window_handles[1]
                driver.switch_to.window(remove_song_window)
                buttons = driver.find_elements_by_class_name('yt-uix-button-content')

                # remove all copyrighted songs
                for button in buttons:
                    if button.text.lower() == copyright_actions.remove_song_action:
                        button.click()

                # save changes as new video
                for button in buttons:
                    if button.text.lower() == copyright_actions.save_copyright_action:
                        button.click()

                        # close tab after saving new video
                        driver.close()

                        # switch back to main window
                        driver.switch_to.window(main_window)

                        driver.get(links.video_manager)
                        break
                break


def youtube_enter_creds(username, password):
    wait.until(lambda driver: driver.find_element_by_id('Email')).send_keys(username)
    wait.until(lambda driver: driver.find_element_by_id('next')).click()
    wait.until(lambda driver: driver.find_element_by_id('Passwd')).send_keys(password)
    wait.until(lambda driver: driver.find_element_by_id('signIn')).click()


def choose_channel(channel_name):
    channels = wait.until(lambda driver: driver.find_elements_by_class_name('identity-prompt-account-list-item'))
    for channel in channels:
        if channel_name.lower() in channel.text.lower():
            channel.click()
            ok_button = wait.until(lambda driver: driver.find_element_by_id('identity-prompt-confirm-button'))
            ok_button.click()
            return


def init_driver(link=links.video_manager, username='spammeallday8', password='Omer6789', channel='The Blue Pill', timeout=300):
    driver = webdriver.Chrome()
    wait = ui.WebDriverWait(driver, timeout)
    driver.get(links.video_manager)
    youtube_enter_creds(username, password)
    choose_channel(channel)
    return driver, wait


if __name__ == '__main__':
    try:
        # options = webdriver.ChromeOptions()
        # options.add_argument("user-data-dir=C:\Users\omer\AppData\Local\Google\Chrome\User Data\Default")
        # driver, wait = init_driver()
        # while True:

        driver = webdriver.Chrome()
        wait = ui.WebDriverWait(driver, timeout=300)
        driver.get(links.video_manager)
        youtube_enter_creds('spammeallday8', 'Omer6789')
        choose_channel('SdarotIL')

        try:
            copyrights = wait.until(
                lambda driver: driver.find_elements_by_class_name('vm-video-side-notification-text-item'))

            copyright_urls = map(lambda copyright: copyright.find_element_by_tag_name('a').get_attribute('href'),
                                 copyrights)
            solve_problem(copyright_urls)

            # delete old videos after handling them
            delete_old_videos(copyright_urls)
        except Exception:
            # driver.quit()
            # time.sleep(60)
            # driver, wait = init_driver()
            pass

    except Exception:
        # driver.quit()
        raise
