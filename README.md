# Neko_feel
Do you understand the feelings of cats?

これはなに：
ねこのきもちを考えてみるアプリです．
tensorflowを用いて，切り取ったねこの顔画像から表情を分類します．
表情は5クラス，教師データは全部で4800枚ほどです．

動作解説：
本アプリはGUIの部分をC++(Siv3D)，分類部分をPythonで作っています．
分類部分をPyInstallerでexe化して配置しておき，GUIのコードから実行させる形で組み合わせています．(頭のいい方法が思いつかなかった)
分類部分はOpenCVでねこの顔を検出し切り取り→tensorflowの学習済みモデルに入れて分類という流れです．

ファイル詳細：
cnn_train.py 画像分類を学習する人
cnn_app.py 学習済みモデルで分類する人
cat_analyze.py ねこの顔画像を切り取り，分類にかける人
cat_analyze.exe ↑の人がPyInstallerでexe化された姿
Neko_GUI/Main.cpp GUIのコード
model.ckpt.* 学習済みモデルデータ
label.txt クラスラベル．学習すると生成される

外部参照：
ねこの顔検出に使用したカスケードファイルはこちらからお借りしました
・https://github.com/wellflat/cat-fancier/tree/master/detector/models/cat
