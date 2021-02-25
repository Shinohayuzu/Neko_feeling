

#include <Siv3D.hpp> // OpenSiv3D v0.4.3
#include <string>
#include <vector>
#include <mutex>
#include <fstream>
#include <Windows.h>
#include <tchar.h>
#include "Neko.h"

using namespace std;

int IsFlag = 0; //0:探しています 1:見つけた 2:見当たらない
static bool IsFirst = true;

struct Data {
	Image texture;
	Texture cat;
};

//表情解析のexeを起動
int catchcat() {
	remove("Face.txt");

	HRESULT hResult = E_FAIL;
	STARTUPINFO si = {0};
	PROCESS_INFORMATION pi = { 0 };
	WCHAR  X[] = L"cnn_app.exe";
	LPWSTR text = X;
	BOOL res = ::CreateProcess(NULL, X, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
	if (0 == res) return -1;
	DWORD dwResult = ::WaitForSingleObject(
		pi.hProcess
		, INFINITE
	);
	if (WAIT_FAILED == dwResult) {
		hResult = HRESULT_FROM_WIN32(::GetLastError());
		goto err;
	}
	err:
	::CloseHandle(pi.hProcess);
	::CloseHandle(pi.hThread);

	ifstream ifa("Face.txt");
	if (!ifa.fail()) IsFlag = 1;
	else IsFlag = 2;
	ifa.close();
}

using App = SceneManager<String, Data>;

//タイトルシーン
class Title: public App::Scene {
private:
	const Font font, imgFont;
	const Rect imgRect;
	Size imgDraw;
	float mag;

public:
	Title(const InitData& init)
		: IScene(init)
		, font(60), imgFont(40)
		, imgRect(100, 100, 600, 400)
		, imgDraw(600,400) {
	}

	void update() override {
		//D&D処理
		if (DragDrop::HasNewFilePaths()) {
			if (const Image image{ DragDrop::GetDroppedFilePaths().front().path }) {
				getData().texture.release();
				getData().texture = image;
				getData().cat = Texture(image);
				getData().texture.save(U"data/cat.jpg");
			}
		}
		//ボタン
		if (SimpleGUI::Button(U"解析開始", Vec2(350, 500))) {
			changeScene(U"CatFace");
		}
	}

	void draw() const override {
		//背景
		Rect(0, 0, 800, 600).draw(Arg::top = ColorF(1.0, 1.0), Arg::bottom = ColorF(1.0, 0.4));
		// テキスト
		font(U"ねこ Feeling").draw(10, 10, Palette::Black);
		//枠かリサイズしたねこ画像を表示
		if (getData().cat) {

			if (getData().cat.size().x > getData().cat.size().y) getData().cat.resized(imgDraw.x).drawAt(Scene::Center());
			else getData().cat.resized(imgDraw.y).drawAt(Scene::Center());
		}
		else {
			imgRect.rounded(40).drawFrame(0, 3, Palette::Gray);
			imgFont(U"ここにねこ画像をD&D").drawAt(Scene::Center(), Palette::Black);
		}
		
	}
};

//顔検出シーン
class CatFace : public App::Scene {
private:
	const Font font;
	Size imgDraw;
	int CatFlag = 0;
	int result=0;
	int i, Flag=0, ret,count;

public:
	CatFace(const InitData& init)
		: IScene(init)
		, font(40)
		, imgDraw(600, 400) {
	}

	void update() override {

		if (IsFirst) {
			catchcat();
			IsFirst = false;
		}

		switch (IsFlag) {
		case 1:
			changeScene(U"Result");
			break;
		case 2:
			if (SimpleGUI::Button(U"最初へ戻る", Vec2(350, 500))) {
				changeScene(U"Title");
			}
		}
	}

	void draw() const override {
		//背景
		Rect(0, 0, 800, 600).draw(Arg::top = ColorF(1.0, 1.0), Arg::bottom = ColorF(1.0, 0.4));
		// テキスト
		switch (IsFlag) {
		case 0:
			font(U"ねこを探しています").draw(10, 10, Palette::Black);
			break;
		case 2:
			font(U"ねこが見当たりません").draw(10, 10, Palette::Black);
			break;
		}
		//ねこ画像
		if (getData().cat.size().x > getData().cat.size().y) getData().cat.resized(imgDraw.x).drawAt(Scene::Center());
		else getData().cat.resized(imgDraw.y).drawAt(Scene::Center());

	}

};

class Result : public App::Scene {
private:
	const Font font;
	Size imgDraw;

public:
	Result(const InitData& init)
		:IScene(init)
		, font(40)
		, imgDraw(600, 400) {

	}

	void update() override {
		//ボタン
		if (SimpleGUI::Button(U"最初へ戻る", Vec2(350, 500))) {
			changeScene(U"Title");
		}
	}

	void draw() const override {
		//背景
		Rect(0, 0, 800, 600).draw(Arg::top = ColorF(1.0, 1.0), Arg::bottom = ColorF(1.0, 0.4));
		//テキスト
		font(U"ねこはこんな顔をしています").draw(10, 10, Palette::Black);
		//ねこ画像
		if (getData().cat.size().x > getData().cat.size().y) getData().cat.resized(imgDraw.x).drawAt(Scene::Center());
		else getData().cat.resized(imgDraw.y).drawAt(Scene::Center());
	}
};

void Main() {
	App manager;

	//タイトルシーンを登録
	manager.add<Title>(U"Title");
	//顔検出シーンを登録
	manager.add<CatFace>(U"CatFace");
	//結果シーンを登録
	manager.add<Result>(U"Result");

	while (System::Update()) {
		if (!manager.update()) {
			break;
		}
	}
}

