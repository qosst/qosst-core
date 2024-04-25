# Notifications

Notifications can be useful for long experiments. In the core module, we define an abstract {py:class}`~qosst_core.notifications.QOSSTNotifier` and a notifier based on this should implement the `send_notification` method.

This method can then be used in other code by using the following code for instance

```{code-block} python

from qosst_core.notifications import QOSSTNotifier

notifier = QOSSTNotifier()

notifier.send_notification("Experiment is finished.")
```

This is an example code but cannot be used as the QOSSTNofitifier abstract object cannot be instantiated.

## Telegram notifier

The only notifier implemented is the telegram notifier that will send message on a telegram conversation. It can be used with the following code


## Implementing a new notifier

Implementing a new notifier is an easy task:

1. Create a class inheriting from {py:class}`qosst_core.notifications.QOSSTNotifier`.
2. Implement the `__init__` method to get all the required variables
3. Implement the `send_notification` method that will use the variables passed in the `__init__` method to send the notification.
