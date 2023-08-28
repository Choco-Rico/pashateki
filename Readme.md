このアプリは撮ったスクショからテキストを抽出するアプリです。

## 必要
* GoogleCloudVisionの認証ファイル（各自取得）
  
## インストール
* リリースから最新版のソースコードをインストールしてください。
* インストール時にOSやブラウザからエラーが出ることがありますが、問題ありませんので無視して進めてください。
* インストールが完了したら、``pashateki.exe``等があるディレクトリにGoogleCloudVisionの認証ファイルを追加してください。この際に、名前をGCP.jsonにしてください。
* ``pashateki.exe``のショートカットを作成しスタートアップフォルダに追加して実行します。

## 設定
* ``pashateki.exe``等があるディレクトリにGoogleCloudVisionの認証ファイルを追加してください。この際に、名前をGCP.jsonにしてください。

## 使い方
* スクショを``pashateki/schフォルダ``に.``jpg``または``png``形式で保存すると、それを検知しテキスト抽出が行われ、数秒で抽出したテキストがGUIに表示されます。
* 中央下部に表示されるsaveボタンを押してウィンドウを閉じると、``pashateki/text``フォルダにテキストファイルとして保存されます。

windowsの場合はGreenShotという素敵なスクショ撮影ツールがおすすめです。
GreenShotは範囲選択のスクショが撮れ出力先フォルダも指定できます。

[GreenShot](https://getgreenshot.org/downloads/)


## 注意
* いくらスクショを撮っても``pashateki/sch``フォルダに``.jpg``もしくは``.png``形式で追加しない限りアプリは反応しません。
* GCP.jsonファイルに名前変更しないとアプリに認識されません。
* GCP.jsonファイルは漏洩してはいけません。大事に管理してください。



## English

This app extracts text from the screencaps you take.

## Required.
* GoogleCloudVision authorization file (obtained on your own)
  
## Install
* Install the latest version of the source code from the release.
* You may get an error from your OS or browser during installation, but it is not a problem, please ignore it and proceed.
* After installation is complete, add the GoogleCloudVision authentication file to the directory where ``pashateki.exe`` etc. are located. At this time, please set the name to GCP.json.
* Create a shortcut for ``pashateki.exe`` and add it to your startup folder and run it.

## Configuration.
* Add the GoogleCloudVision authentication file to the directory where ``pashateki.exe`` etc. are located. At this time, please set the name to GCP.json.

## Usage.
* Add the squash to the ``pashateki/sch folder``. jpg`` or ``png`` format in the ``pashateki/sch folder``, it will detect it and perform text extraction, and the extracted text will be displayed in the GUI in a few seconds.
* If you close the window by pressing the save button that appears at the bottom center, the text will be saved as a text file in the ``pashateki/text`` folder.

For windows, we recommend GreenShot, a nice screencast tool.
GreenShot allows you to take a range selection squash and specify the output folder.


## Caution.
* No matter how many screencaps you take, the app will not respond unless you add them to the ``pashateki/sch`` folder in ``.jpg`` or ``.png`` format.
* The app will not recognize it unless you rename it to a GCP.json file.
* The GCP.json file must not be leaked. Please manage it carefully.
