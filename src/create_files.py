import os 
from pathlib import Path


def new_file():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    id_file_path = log_dir / "id.txt"

    try:
        with open(id_file_path, "r") as ide:
            g = ide.read().strip() 
            if not g.isdigit():
                g = "0"
            ide.close()
    except FileNotFoundError:
        g = "0"
    
    

    ide = open(id_file_path,"w")
    ide.write(str(int(g)+1))
    ide.close()

    log_dir = Path("logs/play"+str(g))
    log_dir.mkdir(exist_ok=True)

    snap = open(log_dir / ("snapshot.csv"), "w")
    snap.write("frame,velocity,rot_vel,vision,prob_fail_rot\n")
    f =  open(log_dir / "mean.csv","a")
    f.write("food_count,robots_count,avg_speed,avg_rot_vel,avg_vision,avg_fail_rot\n")

    return f,snap