import PySimpleGUI as sg
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


import PySimpleGUI as sg

radio_choices = ['windows', 'mac', 'その他']
layout = [
            [sg.Text('どの環境ですか')],
            [sg.Radio(text, 1) for text in radio_choices],
            [sg.Button('OK')]
         ]

window = sg.Window('脱法Deepくん', layout)
windows = True

while True:             # Event Loop
    event, values = window.Read()
    if event is None:
        break
    print(event, values)
    windows = values[0]
    window.close()
    break



if 0 == 0:
    event, values = sg.Window('脱法Deepくん',
                              [[sg.Text('翻訳したいpdfファイルを選ぼう！')],
                               [sg.InputText(), sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
                               [sg.Open(), sg.Cancel()]]).read(close=True)
    fname = values[0]
else:
    fname = sys.argv[1]

if not fname:
    sg.popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
else:
    sg.popup('このファイルを翻訳します', fname)

layout = [
    [sg.Text("pdf読み取り中です")],
]

window = sg.Window("脱法Deepくん", layout)

event, values = window.read(timeout=0)

# 読み込みたいファイルの名前
input_pdf_name = fname

# 出力用のテキストファイル
output_name_txt = input_pdf_name.split('.')[0] + '_output.txt'

output_txt = open(output_name_txt, 'w')


def find_textboxes_recursively(layout_obj):
    """
    再帰的にテキストボックス（LTTextBox）を探して、テキストボックスのリストを取得する。
    """
    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []  # その他の場合は空リストを返す。


# Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
laparams = LAParams(detect_vertical=True)

# 共有のリソースを管理するリソースマネージャーを作成。
resource_manager = PDFResourceManager()

# ページを集めるPageAggregatorオブジェクトを作成。
device = PDFPageAggregator(resource_manager, laparams=laparams)

# Interpreterオブジェクトを作成。
interpreter = PDFPageInterpreter(resource_manager, device)

output_txt = open(output_name_txt, 'w')


def print_and_write(txt):
    # print(txt)
    output_txt.write(txt)
    output_txt.write('\n')


with open(input_pdf_name, 'rb') as f:
    # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する。
    # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号（0始まり）のリストを指定するとよい。
    for page in PDFPage.get_pages(f):
        interpreter.process_page(page)  # ページを処理する。
        layout = device.get_result()  # LTPageオブジェクトを取得。

        # ページ内のテキストボックスのリストを取得する。
        boxes = find_textboxes_recursively(layout)

        # テキストボックスの左上の座標の順でテキストボックスをソートする。
        # y1（Y座標の値）は上に行くほど大きくなるので、正負を反転させている。
        boxes.sort(key=lambda b: (-b.y1, b.x0))

        for box in boxes:
            # print_and_write('-' * 10)  # 読みやすいよう区切り線を表示する。
            print_and_write(box.get_text().strip())  # テキストボックス内のテキストを表示する。

output_txt.close()

window.close()


text =''
with open(output_name_txt,'r') as f: # 保存した英語のテキストを読み込む。
    text = f.read()

sg.popup("翻訳を行います。firefoxが勝手に立ち上がりますが気にしないでください。")

# 4行空白（5回改行）で章変わり，空白二つでタイトル
text = text.replace("\n\n\n\n\n", "###").replace("-\n", "").replace("\n", " ").replace("  ", "\n")  # .replace("-"," ")


def input_key(CSS_selector, key):
    browser.find_element_by_css_selector(CSS_selector).send_keys(key)


def all_delete(CSS_selector):
    # ここはwindousだとKeys.CONTROLにする
    browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.COMMAND, "a")
    browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.DELETE)


def click(CSS_selector):
    browser.find_element_by_css_selector(CSS_selector).click()


def enter(CSS_selector):
    browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.ENTER)


def access(url):
    browser.get(url)


def get_text(CSS_selector):
    text = browser.find_element_by_css_selector(CSS_selector).text
    return text


def input_key(CSS_selector, key):
    browser.find_element_by_css_selector(CSS_selector).send_keys(key)


def all_delete(CSS_selector):
    if windows != True:
        browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.COMMAND, "a")
    else:
        browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.CONTROL, "a")

    browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.DELETE)


def click(CSS_selector):
    browser.find_element_by_css_selector(CSS_selector).click()


def enter(CSS_selector):
    browser.find_element_by_css_selector(CSS_selector).send_keys(Keys.ENTER)


def access(url):
    browser.get(url)


def get_text(CSS_selector):
    text = browser.find_element_by_css_selector(CSS_selector).get_attribute("textContent")
    return text


text_ = text.replace("###", " ###")
text_split = re.split("\. |###", text_)
text_conma = []

# ピリオド追加
for i in text_split:
    text_conma.append(i + ". ")

one_group = ""
translate_text = []
for i in range(len(text_conma)):
    # 改行命令が来たら
    if text_conma[i] == ". ":

        # one_groupの処理について（短いなら結合，長いなら独立でグループ化）
        # もし現在溜まってる文章が5000文字以下なら前の分に追加する
        if len(one_group) < 500:
            translate_text[-1] + one_group

        # 1000文字以下でなければ通常通りグループ化
        else:
            translate_text.append(one_group)

        translate_text.append("###")
        one_group = ""

    # 通常時
    else:
        one_group += text_conma[i]

        # 3500付近来たら もしくは3500に達してなくてもラストなら
        if len(one_group) > 3500 or i == len(text_conma) - 1:
            translate_text.append(one_group)
            one_group = ""

# Firefoxを指定して起動
browser = webdriver.Firefox()

access('https://www.deepl.com/ja/translator')
# browser.execute_script("window.open()") #make new tab
# browser.switch_to.window(browser.window_handles[1]) #switch new tab
# access("file:///C:/Users/NEC/AppData/Roaming/jupyter/runtime/nbserver-1484-open.html")

time.sleep(5)

for i in range(len(translate_text)):

    # 改行命令が来たら改行
    if translate_text[i] == '###':
        with open(input_pdf_name.split('.')[0] + "_翻訳ver.txt", "a") as f:

            f.write("\n\n\n\n")
    else:
        #     browser.switch_to.window(browser.window_handles[0])
        # 翻訳に入力
        input_key(".lmt__source_textarea", translate_text[i])

        # 翻訳中の時間
        time.sleep(20)

        # 翻訳結果コピー
        translate = get_text("div.lmt__textarea_container:nth-child(3)")

        # 要らない部分を除去
        translate = translate.replace("適切な語調に統一しますか？", "")
        translate = translate.replace("DeepL Proでは、カジュアルでくだけた表現を採用するか、テキストごとに選択できます。", "")
        translate = translate.replace("DeepL Proを30日間無料で体験", "")
        translate = translate.replace("\n\n   ", "\n")
        translate = translate.replace("\n\n", "##")
        translate = translate.replace("\n", "")
        translate = translate.replace(" ", "")
        translate = translate.replace("。", "。\n")
        translate = translate.replace("##", "\n----------\n")

        with open(input_pdf_name.split('.')[0] + "_翻訳ver.txt", "a") as f:

            f.write(f"{translate}")

        # 前のテキスト消去
        all_delete(".lmt__source_textarea")
        time.sleep(0.5)

sg.popup("翻訳が終わりました。お疲れ様でした。")



