下载thingscatch压缩包
压缩包外的两个文件不用管，包含在压缩包里了，放文件的时候本来想直接放的，因为文件数量太多放不进去才用压缩包的
box_pick_return_to_shelf是在取出箱子后放回架子上
然后在PowerShell里输入
cd E:\thingscatch
conda env create -f environment.yml
conda activate pinocchio
python box_pick.py
