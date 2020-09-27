# AnalyzeEngineerAbility

## Concepts

GitHub 上でのユーザーの活動状況からエンジニアの能力を評価し、可視化するアプリケーションを作成する。

このアプリケーションでは、GitHub上でユーザーが解決すべき問題を Issue として明文化し、それを Pull Request として解決するという行動を評価の基準として、エンジニアとしての「課題解決能力」を測る。課題解決力を定義する上で、以下のような３つの能力を考える。

- **課題発見力**：リポジトリから課題を見つけ出して Issue 化する
- **コーディング力**：発見した課題をコードに落とし込んで解決する
- **サーチ力**：現状では自力で解決できない課題に対してソリューションを他のコードから見つけ出す

このアプリケーションではこれらの能力を定量的に評価する。

## Requirements

- Python (Python 3.8, Django 3.1)
- JavaScript (Chart.js)
- SQLite or PostgreSQL


## 実装

ユーザーは自身の GitHub のユーザー名を登録するだけで能力の分析をすることができる。ユーザーの能力は全体のスコアとして表示され、その推移も確認することができる。また、ユーザーはリポジトリごとの評価も確認することができる。

概要で示した３つの能力は以下の指標を使うことによって数値化する。

- 課題発見力：Issue の量
- コーディング力：Issue に紐付いている Pull Request の量
- サーチ力：他人のリポジトリに対するスター・フォークの数


## Run the application

- pipenv を使う場合

```
$ pipenv install  # 依存パッケージのインストール
$ pipenv run python manage.py runserver
```

GitHub API を使ってリポジトリ情報を取得するために、いくつかの環境変数を設定する必要がある。

```
API_USERNAME=$YOUR_GITHUB_USERNAME
API_TOKEN=$GITHUB_API_TOKEN
```
