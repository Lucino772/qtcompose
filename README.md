# qtcompose

Build Qt applications in a reactive, declarative, and composable way.

`qtcompose` lets you describe your UI as a tree of components whose properties are driven by reactive values. Update state and the UI updates automatically.

> [!WARNING]
> This project is under active development. APIs and behavior may change quickly, and documentation is still in progress. Feedback and early experimentation are welcome.


## Installation

```shell
pip install qtcompose
```

You’ll also need a Qt binding. The examples use PySide6.

```shell
pip install PySide6
```

## Quick example
A small counter app where the label updates automatically when count changes:

```python
from PySide6 import QtWidgets
from qtcompose.rx import Subject, fn
from qtcompose.ui import (
    QBoxLayoutItem,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

app = QtWidgets.QApplication()

count = Subject(0)

window = QMainWindow(
    children=Subject(
        QWidget(
            layout=Subject(
                QVBoxLayout(
                    children=Subject(
                        [
                            QBoxLayoutItem.Child(
                                QLabel(
                                    text=fn.pipe(
                                        count,
                                        fn.map_(lambda cnt: f"Count: {cnt}")
                                    )
                                )
                            ),
                            QBoxLayoutItem.Child(
                                QPushButton(
                                    text=Subject("Click Me!"),
                                    on_click=Subject(
                                        lambda _: count.push(
                                            lambda prev: prev + 1
                                        )
                                    ),
                                )
                            ),
                        ]
                    )
                )
            )
        )
    )
)()

window.show()
app.exec()
```

## Further reading

For a deeper explanation of the ideas behind this project, check out my blog post:
- [From Imperative Qt to State-Driven UI Composition](https://lucapalmi.com/articles/from-imperative-qt-to-state-driven-ui-composition)
