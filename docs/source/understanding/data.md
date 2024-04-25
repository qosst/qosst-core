# Data

The `qosst-core` package implements a generic data container that can be used to load and save objects in QOSST.

The data container has already implemented `load` and `save` (or `dump`) methods, that can be used as in the following example:

```{code-block} python
from qosst_core.data import BaseQOSSTData

d = BaseQOSSTData()
d.save("test.qosst")

d2 = BaseQOSSTData.load("test.qosst")
```

In general however, one wants to create a class that inherits from BaseQOSSTData, to create a custom data container with the need fields. For instance, a data container containing a list of excess noise and a data could be written as follow:

```{code-block} python
import datetime
from typing import List
from qosst_core.data import BaseQOSSTData

class MyDataContainer(BaseQOSSTData):
    excess_noises: List[float]
    date: datetime.datetime

    def __init__(self, excess_noises: List[float]):
        self.excess_noises = excess_noises
        self.date = datetime.datetime.now()

my_data = MyDataContainer([0.015, 0.012, 0.009])
my_data.save("my_data.qosst")

my_data2 = MyDataContainer.load("my_data.qosst")
print(my_data2.excess_noises)
```

This code should print `[0.015, 0.012, 0.009]`.