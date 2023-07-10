# Hiking
## 摘要
由於爸媽喜歡爬山，但台灣步道選擇甚多，再加上時間等成本考量，以及喜好考量，例如:地區、風景或是海拔等因素，所以我想要找一個可以依照自身需求挑選步道的網站，然而一直沒有找到滿意的篩選設計，
我以此為初衷設計一個簡單版且較多篩選條件的UI介面，並透過UI呈現結果，另外我註冊一個間單版的Line官方帳號，也可以透過Line呈現篩選結果，且也可直接透過Line輸入步道名稱得到其相關資訊。
## 設計
個人化多條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5或是連動至Line機器人呈現篩選結果。
個人化單一條件步道篩選 : 利用PyQt5介面操作，從MySQL或MongoDB抓取資料後再以PyQt5呈現篩選結果。
## hiking_mysql_module_single_selection.py
