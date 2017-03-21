import time
import pymysql.cursors
import requests


conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='testdb',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def fetch():
    sql = "select apikey, apipassword from tmkoo"
    with conn.cursor() as cursor:
        cursor.execute(sql)
    results = cursor.fetchall()
    return results


def clean(results):
    profile = "http://api.tmkoo.com/profile.php?apiKey={apikey}&apiPassword={apipassword}"
    delete = "delete from tmkoo where apikey = '{apikey}'"
    for result in results:
        apikey = result['apikey']
        url = profile.format(**result)
        response = requests.get(url)
        time.sleep(5)
        data = response.json()
        valid = data['validDate']
        if data['ret'] == "1":
            sql = delete.format(apikey=apikey)
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
            print("%s已过期，有效期：%s，删除完毕！" % (apikey, valid))
        else:
            print("%s有效，有效期：%s" % (apikey, valid))


def main():
    results = fetch()
    clean(results)


if __name__ == '__main__':
    main()
