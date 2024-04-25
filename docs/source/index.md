# Welcome to qosst-core's documentation!

```{image} _static/logo.png
:width: 200px
:name: landing-page-logo
:align: center
```

`qosst-core` is the module that contained the common parts of Alice and Bob.

This project is part of [QOSST](https://github.com/qosst).

`qosst-core` provides the following functionalities (more information [here](./introduction/functionalities.md)):

* [configuration module](./understanding/configuration.md);
* [control protocol](./understanding/control_protocol.md) for the classical channel;
* [authentication module](./understanding/authentication.md);
* [modulation and constellations](./understanding/modulation.md);
* [communication functions](./understanding/comm.md): filters and Zadoff-Chu sequence;
* [data containers](./understanding/data.md);
* [notifications](./understanding/notifications.md);
* some utils functions.

```{toctree}
---
maxdepth: 1
caption: Introduction
---   
introduction/getting_started.md
introduction/functionalities.md
```

```{toctree}
---
maxdepth: 1
caption: Understanding qosst-core
---   
understanding/configuration.md
understanding/comm.md
understanding/modulation.md
understanding/control_protocol.md
understanding/authentication.md
understanding/data.md
understanding/notifications.md
```

```{toctree}
---
maxdepth: 1
caption: Command Line Interface
---
cli/index.md
cli/documentation.md
cli/api.md
```

```{toctree}
---
maxdepth: 1
caption: API
---
api/general.md
api/authentication.md
api/comm.md
api/configuration.md
api/schema.md
api/control_protocol.md
api/modulation.md
```

```{toctree}
---
maxdepth: 1
caption: Community
---   
community/contributing.md
community/license.md
```