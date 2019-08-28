



## ユーザー(apps.users.models.User)

```
カスタムユーザーモデル.
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|パスワード |password |varchar(128) | | | | | |
|最終ログイン |last_login |datetime(6) | | | |Both | |
|スーパーユーザー権限 |is_superuser |bool | | | | | |
|id |id |char(32) |True |True | | | |
|メールアドレス |email |varchar(254) | |True | | | |
|名前 |full_name |varchar(100) | | | |Blank | |
|スタッフ権限 |is_staff |bool | | | | | |
|有効 |is_active |bool | | | | | |
|登録日 |date_joined |datetime(6) | | | | | |
|tenant id |tenant_id |integer | | | | | |
|グループ |groups | | | | |Blank |M2M:django.contrib.auth.models.Group (through: apps.users.models.User_groups) |
|ユーザーパーミッション |user_permissions | | | | |Blank |M2M:django.contrib.auth.models.Permission (through: apps.users.models.User_user_permissions) |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```


## tenant(apps.tenants.models.Tenant)

```
Tenant(id, name, subdomain_prefix, is_active, created_at)
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|id |id |integer |True |True | | | |
|name |name |varchar(100) | | | | | |
|subdomain prefix |subdomain_prefix |varchar(100) | |True | | | |
|有効 |is_active |bool | | | | | |
|created at |created_at |datetime(6) | | | | | |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```


## kintone_ key(apps.ds.models.kitone_key.Kintone_Key)

```

Kintoneへのアクセス情報の管理テーブル
[更新説明]
・必要に応じて随時、admin管理画面より追加/修正/削除を行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|名前 |name |varchar(100) | | | | | |
|DOMAIN |domain |varchar(100) | | | | | |
|APP ID |app_id |varchar(100) | | | | | |
|API TOKEN |api_token |varchar(100) | | | | | |
|削除フラグ |deleted |bool | | | | | |

Options
```
unique_together : (('tenant', 'app_id'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## customer(apps.ds.models.customer.Customer)

```

顧客情報のマスタテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客番号 |no |integer | | | | | |
|顧客名 |name |varchar(200) | | | |Both | |
|顧客名カナ |name_kana |varchar(200) | | | |Both | |
|郵便番号 |zip_code |varchar(10) | | | |Both | |
|都道府県 |prefecture_name |varchar(100) | | | |Both | |
|市町村 |city_name |varchar(100) | | | |Both | |
|レコードタイトル |title |varchar(200) | | | |Both | |
|更新者名 |updated_by |varchar(50) | | | |Both | |
|作成日時_元 |created_at_origin |datetime(6) | | | |Both | |
|更新日時_元 |updated_at_origin |datetime(6) | | | |Both | |
|ホームページURL |hp_url |varchar(2048) | | | |Both | |
|締日 |sme_day |varchar(3) | | | |Both | |
|支払月 |pay_month |varchar(3) | | | |Both | |
|支払日 |pay_day |varchar(3) | | | |Both | |
|課題 |task |longtext | | | |Both | |
|取扱商品 |products |varchar(200) | | | |Both | |
|顧客ランク |rank |varchar(10) | | | |Both | |
|ニーズ |needs |longtext | | | |Both | |
|年商 |yealy_sales |integer | | | |Both | |
|代表者名 |representative |varchar(100) | | | |Both | |
|顧客管理コード |manage_cd |varchar(20) | | | |Both | |
|顧客管理名 |manage_name |varchar(200) | | | |Both | |
|決算月 |settlement_month |varchar(3) | | | |Both | |
|決定権者・決済額 |settlement |varchar(300) | | | |Both | |
|帝国データバング |teikoku_data |varchar(100) | | | |Both | |
|業種 |industry_type |varchar(100) | | | |Both | |
|会社情報備考 |remark |longtext | | | |Both | |
|電話番号 |tel |varchar(20) | | | |Both | |
|FAX番号 |fax |varchar(20) | | | |Both | |
|社員数 |employee_number |integer | | | |Both | |

Options
```
unique_together : (('tenant', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## employee(apps.ds.models.employee.Employee)

```

社員情報のマスタテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|社員管理番号 |no |integer | | | | | |
|社員コード |code |varchar(20) | | | | | |
|社員コード省略版 |code_short |varchar(20) | | | |Both | |
|社員名 |name |varchar(200) | | | |Both | |
|社員名カナ |name_kana |varchar(200) | | | |Both | |
|社員名検索用 |name_search |varchar(200) | | | |Both | |
|所属部署 |department |varchar(50) | | | |Both | |
|作成日時_元 |created_at_origin |datetime(6) | | | |Both | |
|更新日時_元 |updated_at_origin |datetime(6) | | | |Both | |
|廃止区分 |deleted_kbn |varchar(20) | | | |Both | |
|廃止日時 |deleted_at |datetime(6) | | | |Both | |

Options
```
unique_together : (('tenant', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken(apps.ds.models.anken.Anken)

```

商談案件のテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|商談案件番号 |no |integer | | | | | |
|商談案件名 |name |varchar(200) | | | |Both | |
|レコードタイトル |title |varchar(200) | | | |Both | |
|作成日時_元 |created_at_origin |datetime(6) | | | |Both | |
|更新日時_元 |updated_at_origin |datetime(6) | | | |Both | |
|社員管理ID |employee |integer | | |True |Null |FK:apps.ds.models.employee.Employee |
|社員管理番号 |employee_no |integer | | | |Both | |
|営業担当社員名 |employee_name |varchar(50) | | | |Both | |
|顧客管理ID |customer |integer | | |True |Null |FK:apps.ds.models.customer.Customer |
|顧客番号 |customer_no |integer | | | | | |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|顧客部署名 |section_name |varchar(200) | | | |Both | |
|顧客部署TEL種類 |section_tel_type |varchar(100) | | | |Both | |
|顧客部署TEL番号 |section_tel |varchar(20) | | | |Both | |
|顧客側担当 |customer_person |varchar(50) | | | |Both | |
|成約予定日 |close_plan_dt |date | | | |Both | |
|成約予定金額合計 |close_plan_total |integer | | | | | |
|成約予定粗利合計 |close_plan_profit |integer | | | | | |
|成約予定月額合計 |close_plan_mamount |integer | | | | | |
|成約計上日 |close_dt |date | | | |Both | |
|売上予定日（1回目） |sales_plan_dt |date | | | |Both | |
|売上予定粗利合計 |sales_plan_profit |integer | | | | | |
|売上予定月額合計 |sales_plan_mamount |integer | | | | | |
|結果 |result |varchar(20) | | | |Both | |
|結果分析 |result_analyze |longtext | | | |Both | |
|備考 |remarks |longtext | | | |Both | |
|成約確率 |salse_probability |smallint | | | | | |
|結果区分 |result_kbn |smallint | | | | | |

Options
```
unique_together : (('tenant', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## history(apps.ds.models.history.History)

```

商談履歴のテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|商談履歴番号 |no |integer | | | | | |
|商談案件管理ID |anken |integer | | |True |Null |FK:apps.ds.models.anken.Anken |
|商談案件番号 |anken_no |integer | | | |Both | |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|レコードタイトル |title |varchar(200) | | | |Both | |
|作成日時_元 |created_at_origin |datetime(6) | | | |Both | |
|更新日時_元 |updated_at_origin |datetime(6) | | | |Both | |
|社員管理ID |employee |integer | | |True |Null |FK:apps.ds.models.employee.Employee |
|社員管理番号 |employee_no |integer | | | |Both | |
|営業担当社員名 |employee_name |varchar(50) | | | |Both | |
|顧客管理ID |customer |integer | | |True |Null |FK:apps.ds.models.customer.Customer |
|顧客番号 |customer_no |integer | | | | | |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|訪問予定日時 |visit_plan_dt |datetime(6) | | | |Both | |
|訪問時間（予定） |visit_plan_times |smallint | | | |Both | |
|実訪問日時 |visit_dt |datetime(6) | | | |Both | |
|訪問時間（実績） |visit_times |smallint | | | |Both | |
|面談目的 |purpose |longtext | | | |Both | |
|面談手段（予定） |meet_method |varchar(100) | | | |Both | |
|面談手段（実績） |meet_result |varchar(100) | | | |Both | |
|面談結果 |result |longtext | | | |Both | |
|備考 |remarks |longtext | | | |Both | |
|課題 |future_issue |longtext | | | |Both | |
|次回設定 |next_action |longtext | | | |Both | |
|次回アクション日時 |next_action_dt |datetime(6) | | | |Both | |
|注目 |attention |varchar(10) | | | |Both | |
|いいね数 |good_count |smallint | | | |Both | |

Options
```
unique_together : (('tenant', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## rulebook(apps.ds.models.rulebook.Rulebook)

```

ルールブックのテーブル
[更新説明]
・ルールブック画面での随時更新
・更新時は、idをキーにしてUpdateを行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|ルール名 |name |varchar(200) | | | |Both | |
|ルールタイプ |ruletype |smallint | | | | |1:アドバイス, 2:アラート |
|アドバイス（アラート） |comment |longtext | | | | | |
|ルール重要度 |rank |smallint | | | | | |
|有効 |is_active |bool | | | | | |
|更新ユーザー管理ID |update_user |char(32) | | |True |Null |FK:apps.users.models.User |
|更新ユーザー名 |update_user_name |varchar(100) | | | |Both | |
|条件内容 |condition_where |longtext | | | |Both | |

Options
```
unique_together : (('tenant', 'name', 'ruletype'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ advice(apps.ds.models.anken_advice.Anken_Advice)

```

アドバイス（アラート）のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken, ds_history, ds_customer, ds_rulebook etc より取得したデータを基にして更新する。
（ds_anken.result='継続'に紐づくanken_id or ds_history.anken_id=Nullに紐づくcustomer_idが対象）
・全データを対象として、Delete + Insert を行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True |Null |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|最終訪問日時 |last_visit_dt |datetime(6) | | | |Both | |
|ルールブック管理ID |rulebook |integer | | |True | |FK:apps.ds.models.rulebook.Rulebook |
|ルールタイプ |rulebook_ruletype |smallint | | | | | |
|ルール名 |rulebook_name |varchar(200) | | | |Both | |
|アドバイス（アラート） |rulebook_comment |longtext | | | | | |
|ルール重要度 |rulebook_rank |smallint | | | | | |

Options
```
unique_together : (('tenant', 'customer', 'anken', 'rulebook'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ near(apps.ds.models.anken_near.Anken_Near)

```

類似案件のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_anken, ds_customer より取得したデータを基にして更新する。
（ds_history.updated_atが本日であるデータに紐づくcustomer_id, anken_idが対象）
・customer_idとanken_idが同じであるデータが存在した場合は、Delete + Insertを行う。
（anken_idがNullの場合（未案件分）は、anken_id=Nullを条件とする。）
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True |Null |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|商談案件管理ID（類似） |anken_near |integer | | |True | |FK:apps.ds.models.anken.Anken |
|商談案件名（類似） |anken_near_name |varchar(200) | | | |Both | |
|結果 |anken_result |varchar(20) | | | |Both | |
|類似率 |near_rate |double precision | | | | | |
|結果区分 |anken_result_kbn |smallint | | | | | |

Options
```
unique_together : (('tenant', 'customer', 'anken', 'anken_near'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ successrt_ cmt(apps.ds.models.anken_successrt_cmt.Anken_Successrt_Cmt)

```

案件成約確率コメントのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken, ds_history, ds_customer より取得したデータを基にして更新する。
（ds_anken.result='継続'であるデータに紐づくanken_idが対象）
・全データを対象として、Delete + Insert を行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True | |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|案件分析コメント |comment |longtext | | | | | |
|成約上昇率 |successup_rate |double precision | | | | | |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ successrt_ history(apps.ds.models.anken_successrt_history.Anken_Successrt_History)

```

案件成約確率履歴のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken_successrt より取得したデータを基にして更新する。
・create_dtが本日であるデータを対象として、Delete + Insert を行う。（基本的にDeleteは発生しない）
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True | |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|成約確率 |success_rate |double precision | | | | | |
|作成日付 |created_dt |date | | | | | |

Options
```
unique_together : (('tenant', 'customer', 'anken', 'created_dt'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ successrt(apps.ds.models.anken_successrt.Anken_Successrt)

```

案件成約確率のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken, ds_history, ds_customer より取得したデータを基にして更新する。
（ds_anken.result='継続'であるデータに紐づくanken_idが対象）
・全データを対象として、Delete + Insert を行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True | |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|成約確率 |success_rate |double precision | | | | | |

Options
```
unique_together : (('tenant', 'customer', 'anken'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## customer_ news(apps.ds.models.customer_news.Customer_News)

```

顧客ニュースのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_customer より取得したデータを基にして更新する。
（ds_customer_news.created_atが古い順に指定件数が対象）
・customer_id が同一であるデータがある場合は、customer_id単位で最初に1回 Deleteした上で、Insertする。
・customer_idに対する取得ニュースが0件である場合は、news_no=0をセットして、空レコードを登録する。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|ニュースNo |news_no |smallint | | | | | |
|URL |news_url |longtext | | | |Both | |
|感情値 |news_sentiment |double precision | | | | | |
|要約 |news_semantic_role |longtext | | | |Both | |

Options
```
unique_together : (('tenant', 'customer', 'news_no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## dictionary(apps.ds.models.dictionary.Dictionary)

```

辞書のテーブル
[更新説明]
・辞書管理画面での随時更新、又は1回/日の間隔にて学習用の更新を行う。
・更新時は、idをキーにしてUpdateを行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|辞書グループ名 |grpname |varchar(200) | | | | | |
|辞書タイプ |typekbn |smallint | | | | |1:単語@, 2:振る舞い# |
|辞書キーワード |distword |varchar(200) | | | | | |
|辞書ポイント |point |smallint | | | | | |
|全一致区分 |is_perfect_match |bool | | | | | |
|学習済区分 |is_learned |bool | | | | | |
|学習日時 |learned_at |datetime(6) | | | |Both | |
|有効 |is_active |bool | | | | | |
|更新ユーザー管理ID |update_user |char(32) | | |True |Null |FK:apps.users.models.User |
|更新ユーザー名 |update_user_name |varchar(100) | | | |Both | |

Options
```
unique_together : (('tenant', 'grpname', 'typekbn'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## keyword(apps.ds.models.keyword.Keyword)

```

キーワードのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_dictonary より取得したデータを基にして更新する。
（ds_history.updated_atが本日であるデータが対象）
・history_idが同じであるデータが存在した場合は, 最初にhistory_id単位でDeleteし、
 その後Insert時に、history_id + dictionary_idが同じデータが既存する場合はスキップする。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|商談履歴管理ID |history |integer | | |True | |FK:apps.ds.models.history.History |
|面談結果 |history_result |longtext | | | |Both | |
|実訪問日時 |history_visit_dt |datetime(6) | | | |Both | |
|顧客管理ID |customer |integer | | |True | |FK:apps.ds.models.customer.Customer |
|顧客名 |customer_name |varchar(200) | | | |Both | |
|商談案件管理ID |anken |integer | | |True |Null |FK:apps.ds.models.anken.Anken |
|商談案件名 |anken_name |varchar(200) | | | |Both | |
|辞書管理ID |dictionary |integer | | |True |Null |FK:apps.ds.models.dictionary.Dictionary |
|辞書グループ名 |dictionary_grpname |varchar(200) | | | | | |
|辞書タイプ |dictionary_typekbn |smallint | | | | | |
|辞書キーワード |dictionary_distword |varchar(200) | | | | | |
|辞書ポイント |dictionary_point |smallint | | | | | |

Options
```
unique_together : (('tenant', 'history', 'dictionary'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## dictionary_ synonym(apps.ds.models.dictionary_synonym.Dictionary_Synonym)

```

辞書類似ワードのテーブル
[更新説明]
・辞書管理画面での随時更新、又は1回/日の間隔にて学習用の更新を行う。
・更新時は、dictonary_idをキーにしてDelete + Insertを行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|辞書管理ID |dictionary |integer | | |True | |FK:apps.ds.models.dictionary.Dictionary |
|辞書グループ名 |dictionary_grpname |varchar(200) | | | |Both | |
|辞書キーワード |dictionary_distword |varchar(200) | | | |Both | |
|類似ワードNo |no |smallint | | | | | |
|類似ワード |synonymword |varchar(200) | | | | | |

Options
```
unique_together : (('tenant', 'dictionary', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## rulebook_ condition(apps.ds.models.rulebook_condition.Rulebook_Condition)

```

ルールブック条件のテーブル
[更新説明]
・ルールブック画面での随時更新
・更新時は、rulebook_idをキーにしてDelete + Insertを行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|ルールブック管理ID |rulebook |integer | | |True | |FK:apps.ds.models.rulebook.Rulebook |
|ルール名 |rulebook_name |varchar(200) | | | |Both | |
|条件No |no |smallint | | | | | |
|条件タイプ |conditiontype |smallint | | | | |0:先頭条件, 1:AND条件, 2:OR条件 |
|項目ID |item_id |integer | | | | | |
|項目名称 |item_name |varchar(200) | | | |Both | |
|項目タイプ |item_type |smallint | | | | |1:文字, 2:数字 |
|項目値 |item_val |longtext | | | |Both | |
|比較タイプ |cmpr_type |smallint | | | | |1:等しい, 2:等しくない, 3:以上, 4:以下, 5:より大きい, 6:より小さい, 7:含む, 8:含まない |

Options
```
unique_together : (('tenant', 'rulebook', 'no'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## code_ name(apps.ds.models.code_name.Code_Name)

```

コード名称のマスタテーブル
[更新説明]
・管理者用画面にて追加・修正・削除を行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|コード |code |varchar(20) | | | | | |
|コード名称 |name |varchar(200) | | | |Both | |
|項目ID |item_id |integer | | | | | |
|項目名称 |item_name |varchar(200) | | | |Both | |
|項目タイプ |item_type |smallint | | | | |1:文字, 2:数字 |
|項目値 |item_val |longtext | | | |Both | |
|項目値その2 |item_val2 |longtext | | | |Both | |
|項目値その3 |item_val3 |longtext | | | |Both | |
|有効 |is_active |bool | | | | | |

Options
```
unique_together : (('tenant', 'code', 'item_id'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## anken_ karte_ disp config(apps.ds.models.anken_karte_dispconfig.Anken_Karte_DispConfig)

```

案件カルテ表示設定のテーブル
[更新説明]
・案件カルテ画面で、各カードの位置情報を変更した際に更新する。
・user_idでDeleteした後、Insertを行う。
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|tenant |tenant |integer | | |True | |FK:apps.tenants.models.Tenant |
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|作成日時 |created_at |datetime(6) | | | |Blank | |
|更新日時 |updated_at |datetime(6) | | | |Blank | |
|LOCK ID |lock_id |integer | | | | | |
|ユーザー管理ID |user |char(32) | | |True |Null |FK:apps.users.models.User |
|ユーザー名 |user_name |varchar(100) | | | |Both | |
|表示No |dispno |smallint | | | | | |
|項目ID |item_id |integer | | | | | |
|項目名称 |item_name |varchar(200) | | | |Both | |

Options
```
unique_together : (('tenant', 'user', 'dispno'),)
default_permissions : ('add', 'change', 'delete', 'view')
```


## access_ logs(apps.dblogs.models.access_logs.Access_Logs)

```

アクセス履歴テーブル
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|session key |session_key |varchar(1024) | | | |Blank | |
|path |path |varchar(1024) | | | |Blank | |
|method |method |varchar(8) | | | |Blank | |
|data |data |longtext | | | |Both | |
|ip address |ip_address |varchar(45) | | | |Blank | |
|referrer |referrer |varchar(512) | | | |Both | |
|timestamp |timestamp |datetime(6) | | | |Blank | |
|tenant id |tenant_id |integer | | | |Both | |
|tenant name |tenant_name |varchar(100) | | | |Both | |
|user id |user_id |varchar(128) | | | |Both | |
|user name |user_name |varchar(100) | | | |Both | |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```


## process(apps.dblogs.models.process.Process)

```

PROCESS管理テーブル
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|name |name |varchar(100) | | | | | |
|type |type |varchar(20) | | | | |RestAPI:REST API, BGJob:Back Ground Job, Etc:その他 |
|comment |comment |varchar(300) | | | |Both | |
|created at |created_at |datetime(6) | | | |Blank | |
|updated at |updated_at |datetime(6) | | | |Blank | |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```


## process_ logs(apps.dblogs.models.process_logs.Process_Logs)

```

PROCESS実行履歴テーブル
    
```

|Fullname|Name|Type|PK|Unique|Index|Null/Blank|Comment|
|---|---|---|---|---|---|---|---|
|ID |id |integer AUTO_INCREMENT |True |True | |Blank | |
|process id |process_id |integer | | | | | |
|process name |process_name |varchar(100) | | | |Both | |
|process type |process_type |varchar(20) | | | |Both | |
|tenant id |tenant_id |integer | | | |Both | |
|status |status |varchar(1) | | | |Both |I:Infomation, W:Warning, E:Error, C:Critical |
|created at |created_at |datetime(6) | | | |Blank | |
|updated at |updated_at |datetime(6) | | | |Blank | |
|process log |process_log |longtext | | | |Both | |

Options
```
default_permissions : ('add', 'change', 'delete', 'view')
```



