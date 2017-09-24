Algo is very hard and works too long. It codes every pixel with 64-long hash and joins them into one string. 
It means, that we can just split [encrypted data](encrypted.txt) to [bloks by 64 chars](encrypted_splited.txt). 
There are just 17 different pixels there.

Now we can replace them by RGB-tuples and find right image size.

```python
from PIL import Image
import numpy as np
from collections import Counter

color_hash = [
    '709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c',
    'ac205167ca956b408a925c3854fdd82ffa43672263ae7dba5a68b29d9a81fa56', 
    '2ec847d8a31a988b3117a5095dae74f490448223f035ec7eddef6768b91a9028', 
    '8ae40a3583aef6697d2c2eff57eb915ed0bda54aaa92812ad97982743ac06f37', 
    'ab5ab0fedc83e5a1a1871c427eccbcd3cf0fc1bb74a82a552adfd9b4e57f391b', 
    '2ac9a6746aca543af8dff39894cfe8173afba21eb01c6fae33d52947222855ef', 
    'f1b901847390b0ed7e374e7c1e464ec17b46a427c487a5ad6cbd2906405083d5', 
    '5ae7e6a42304dc6e4176210b83c43024f99a0bce9a870c3b6d2c95fc8ebfb74c', 
    'b9e8d0a22760b87553c0b9c55ae93058bf8d4389c87765488cea1637e94bd9b6', 
    'a30cb1d8569c5c141b2ade1caf57038b2be46c9bc4939c8f702a0ff4fcecfd77', 
    '91737e71235959a56c524997e18d6d14d6ddd714ed2a450a24f765255a2733ee', 
    '700af1feb55ab0613bdbc466815643743156af4e869120244eb05ca72c45002c', 
    '0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4', 
    '7b108f7c5c6f1507c4ffe2275dd9b8e25a71d175a5a9d3e19aeec3f27d82caf1', 
    '204164d223b35aabb54ea32b1d14d8bb5a8df56f7c81f3304987fa4193426729', 
    'c4289629b08bc4d61411aaa6d6d4a0c3c5f8c1e848e282976e29b6bed5aeedc7',
    '5ae0d5195906bfc4f70167cf171ae4d08e7376aa246977acf172187d5d384f10'
]

color_val = [
    (255,255,255),
    (127, 127, 0),
    (64, 255, 0),
    (0, 255, 255),
    (0, 64, 255),
    (255, 0, 255),
    (255, 0, 0),
    (255, 255, 255),
    (0, 0, 0),
    (204, 153, 0),
    (255, 102, 153),
    (204, 255, 102),
    (102, 153, 0),
    (102, 153, 153),
    (11,124,8),
    (18,4,128),
    (202, 183, 19)
]

colors = dict(zip(color_hash, color_val))

with open('encrypted_splited.txt', 'r') as f:
    data = [x.strip('\n') for x in f.readlines()]

data = list(map(lambda x:colors[x], data))
img = Image.new('RGB', (351,21))
img.putdata(data)
img.show()
```
