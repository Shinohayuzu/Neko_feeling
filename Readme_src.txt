NekoFeel ソースコードについて

GitHub：https://github.com/Shinohayuzu/Neko_feeling
cascade.xmlはここからDLしてください：https://github.com/wellflat/cat-fancier/tree/master/detector/models/cat

＊動作確認環境＊
Windows10Home バージョン1909

＊GUI部分に関して＊
:環境
VisualStudio2019
C++

:使用ライブラリ
Siv3D

:ソースファイル
Main.cpp

:データファイル-Main.cppと同じフォルダに置いてください
dataフォルダ---cascade.xml
     　　　　└label.txt
cat_analyze.exe
model.ckpt.data-00000-of-00001
model.ckpt.index
model.ckpt.meta

Siv3Dをインストールし，VisualStudioにて新しいプロジェクト(Siv3Dアプリケーション)を作成します．
Main.cppを読み込み，ビルドすると画面が立ち上がります．

-参照情報-
・Siv3D：https://siv3d.github.io/ja-jp/


＊表情解析部分について＊
:環境
Python 3.7

:使用ライブラリ
OpenCV 3.4.2
tensorflow 1.14.0
PIL 8.1.0
NumPy 1.15.4

:ソースファイル
cnn_train.py
cnn_app.py
cat_analyze.py

:データファイル-Main.cppと同じフォルダに置いてください
dataフォルダ---cascade.xml
     　　　　└label.txt
model.ckpt.data-00000-of-00001
model.ckpt.index
model.ckpt.meta

cnn_train.pyは教師画像データを読み込み学習を行います．
学習データはインターネットからねこの画像を5000枚ほど集め，OpenCVでのねこ顔検出や人力でねこの顔を切り抜いて用意しました．
cnn_app.pyは学習したモデルデータを元に，入力された画像に対してどの表情に近いかを返します．
cat_analyze.pyは，決められたパス(data/cat.jpg)にある画像を入力として読み込み，OpenCVによるねこ顔検出切り取りを行い，cnn_app.pyに渡して表情の読み取りを行わせます．その後ねこの顔を枠で囲い，表情分析結果を文字で書き込んで，結果画像としてdata/result.jpgに保存します．
これをPyInstallerでexe化したものがcat_analyzer.exeです．

2021/02/28 最終更新