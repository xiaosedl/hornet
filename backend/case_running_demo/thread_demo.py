import threading
from time import sleep, ctime


def music():
    print("listening music ", ctime())
    sleep(2)


def movie():
    print("listening movie ", ctime())
    sleep(2)


def super_player(name, t):
    print(f"执行播放 {name} {ctime()}")
    sleep(2)


play_list = [["孤勇者", 3], ["四海", 5]]
threads = []
for play in play_list:
    t = threading.Thread(target=super_player, args=(play[0], play[1]))
    threads.append(t)

# t1 = threading.Thread(target=music)
# t2 = threading.Thread(target=movie)


if __name__ == "__main__":
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("all over time ", ctime())