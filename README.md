# Hiking
## 摘要
家人喜歡爬山，但由於台灣步道選擇多，然而考量時間等成本以及喜好，例如:地區、風景或是海拔，因此找尋可依照自身需求挑選步道的網站就很重要，然而家人一直沒有找到滿意的篩選設計，
我以此為初衷設計一個簡單版且較多篩選條件的UI介面，使用者可透過UI呈現篩選成果，另外我註冊一個簡單版的Line官方帳號，因此也可以透過Line呈現篩選成果，此外使用者可直接透過Line輸入步道名稱得到其相關資訊。
## 程式設計概論
1. 個人化多條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5或是連動至Line官方帳號呈現篩選成果。
2. 個人化單一條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5呈現篩選成果。
3. 單一步道相關資料查詢 ： 在Line官方帳號輸入步道名稱即可從MySQL或MongoDB得到該步道相關資料。<br/>
------------------------------------------------------------------------------------------------
以下分別介紹每個.py執行之成果 :
### hiking_mysql_module_single_selection.py
以PyQt5顯示從MySQL個人化單一條件步道篩選之成果
### hiking_mysql_module_multiple_selection.py
以PyQt5顯示從MySQL個人化多條件步道篩選之成果
### hiking_mysql_module_multiple_selection_line_carousel.py
以PyQt5以及Line官方帳號顯示從MySQL個人化多條件步道篩選之成果
### hiking_mysql_linebot.py
以Line官方帳號顯示從MySQL得到單一步道相關資料
### hiking_nosql_module_single_selection.py
以PyQt5顯示從MongoDB個人化單一條件步道篩選之成果
### hiking_nosql_module_multiple_selection.py
以PyQt5顯示從MongoDB個人化多條件步道篩選之成果
### hiking_nosql_module_multiple_selection_line_carousel.py
以PyQt5以及Line官方帳號顯示從MongoDB個人化多條件步道篩選之成果
### hiking_nosql_linebot.py
以Line官方帳號顯示從MongoDB得到單一步道相關資料
### hiking_Taiwan_distribution.py
以PyQt5顯示matplotlib視覺化台灣步道地區分布的成果
### hiking_difficulty.py
以PyQt5顯示matplotlib視覺化台灣步道難易度分布的成果
### hiking_distance.py
以PyQt5顯示matplotlib視覺化台灣步道長度分布的成果
### hiking_altitude.py
以PyQt5顯示matplotlib視覺化台灣步道海拔高度分布的成果
### hiking_height_different.py
以PyQt5顯示matplotlib視覺化台灣步道高度落差分布的成果


