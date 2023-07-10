# Hiking
## 摘要
家人喜歡爬山，但由於台灣步道選擇多，然而考量時間等成本以及喜好，例如:地區、風景或是海拔，因此找尋可依照自身需求挑選步道的網站就很重要，然而家人一直沒有找到滿意的篩選設計，
我以此為初衷設計一個簡單版且較多篩選條件的UI介面，使用者可透過UI呈現結果，另外我註冊一個簡單版的Line官方帳號，因此也可以透過Line呈現篩選結果，此外使用者可直接透過Line輸入步道名稱得到其相關資訊。
## 程式設計概論
個人化多條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5或是連動至Line官方帳號呈現篩選結果。
個人化單一條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5呈現篩選結果。
單一步道相關資料查詢 ： 可在Line官方帳號輸入步道名稱即可得到該步道相關資料
## hiking_mysql_module_single_selection.py
