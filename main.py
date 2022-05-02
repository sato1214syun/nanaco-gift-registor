import re
import pyperclip
from playwright.sync_api import Playwright, sync_playwright, expect


def run(
    playwright: Playwright,
    nanaco_id_list: list[tuple[str, str, str, str]],
    user_id,
    password,
) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.nanaco-net.jp/pc/emServlet
    page.goto("https://www.nanaco-net.jp/pc/emServlet")

    # Fill text=nanaco番号 （ハイフンを除く半角数字16桁） 会員メニュー用パスワード >> input[name="XCID"]
    page.locator(
        'text=nanaco番号 （ハイフンを除く半角数字16桁） 会員メニュー用パスワード >> input[name="XCID"]'
    ).fill(user_id)

    # Fill input[name="LOGIN_PWD"]
    page.locator('input[name="LOGIN_PWD"]').fill(password)

    # Click text=nanacoモバイルをお持ちの方 nanacoモバイル会員、nanacoネット会員 nanacoモバイルアプリのTOP画面に記載のnanaco番号と会員メニュー >> input[alt="ログイン"]
    page.locator(
        'text=nanacoモバイルをお持ちの方 nanacoモバイル会員、nanacoネット会員 nanacoモバイルアプリのTOP画面に記載のnanaco番号と会員メニュー >> input[alt="ログイン"]'
    ).click()

    # Click text=nanacoギフト登録 nanacoギフトのID登録ができます。
    page.locator("text=nanacoギフト登録 nanacoギフトのID登録ができます。").click()

    for id_tuple in nanaco_id_list:
        # Click input[alt="縺泌茜逕ｨ邏�ｬｾ縺ｫ蜷梧э縺ｮ荳翫∫匳骭ｲ"]
        with page.expect_popup() as popup_info:
            page.locator('input[src="/member/image/gift100/btn_400.gif"]').click()
        page1 = popup_info.value

        # Fill input[name="id1"]
        page1.locator('input[name="id1"]').fill(id_tuple[0])

        # Fill input[name="id2"]
        page1.locator('input[name="id2"]').fill(id_tuple[1])

        # Fill input[name="id3"]
        page1.locator('input[name="id3"]').fill(id_tuple[2])

        # Fill input[name="id4"]
        page1.locator('input[name="id4"]').fill(id_tuple[3])

        # Click input[alt="確認画面へ"]
        page1.locator('input[alt="確認画面へ"]').click()

        if page1.query_selector('input[alt="登録する"]') is not None:
            # Click input[alt="登録する"]
            page1.locator('input[alt="登録する"]').click()

        # Close page
        page1.close()

    # Click text=ログアウト
    page.locator("text=ログアウト").click()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()
    return


def GetNanacoGiftId(text: str) -> list[tuple[str, str, str, str]]:
    nanaco_id_list: list[tuple[str, str, str, str]] = []
    for row in text.split("\n"):
        res = re.search(
            r"^([a-zA-Z\d]{4})([a-zA-Z\d]{4})([a-zA-Z\d]{4})([a-zA-Z\d]{4})$",
            row.strip(),
        )
        if res is not None:
            nanaco_id_list.append(res.groups())
    return nanaco_id_list


if __name__ == "__main__":
    try:
        text = pyperclip.paste()
    except pyperclip.PyperclipException:
        text = input("ギフトコードを貼り付けてください")

    nanaco_id_list = GetNanacoGiftId(text)

    print("\nnanacoサイトのアカウント情報を入力してください")
    user_id = input("nanaco番号:")
    password = input("パスワード:")
    with sync_playwright() as playwright:
        run(playwright, nanaco_id_list, user_id, password)
    print("nanacoギフトコードの登録が完了しました")
