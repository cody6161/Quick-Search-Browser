"""Quick Search Browser: quick browser filters for Anki's card browser."""

from functools import partial

# Anki exposes UI lifecycle hooks through gui_hooks and the main window as mw.
from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.browser.table import SearchContext
from aqt.errors import show_exception
from aqt.qt import *
from aqt.qt import QCheckBox, QComboBox


class _MultiSelectMenu(QMenu):
    """QMenu that keeps checkable menu items open while the user toggles them."""

    def __init__(self, parent=None, single_selection=False, on_change=None):
        super().__init__(parent)
        # Optional special actions used by the flag menu.
        self._exclusive_action = None
        self._clear_action = None
        # single_selection makes the menu behave like a radio group, while still
        # allowing the selected item to be clicked again to clear it.
        self._single_selection = single_selection
        # Called after a filter changes so the browser search refreshes.
        self._on_change = on_change

    def mouseReleaseEvent(self, event):
        action = self.activeAction()
        if action and action.isCheckable():
            if action is self._clear_action:
                # The clear option removes every checked filter item.
                for a in self.actions():
                    a.setChecked(False)
            elif self._single_selection:
                # If the clicked action is already checked, uncheck it
                if action.isChecked():
                    action.setChecked(False)
                else:
                    # Uncheck all other actions
                    for a in self.actions():
                        if a is not action:
                            a.setChecked(False)
                    # Check the clicked action
                    action.setChecked(True)
            else:
                # Multi-select mode lets several values be checked at once.
                new_state = not action.isChecked()
                action.setChecked(new_state)
                if new_state:
                    if action is self._exclusive_action:
                        # An exclusive action such as "Any flag" clears all
                        # more specific choices.
                        for a in self.actions():
                            if a is not action:
                                a.setChecked(False)
                    elif self._exclusive_action is not None:
                        # Choosing a specific option clears the exclusive one.
                        self._exclusive_action.setChecked(False)

            if self._on_change:
                self._on_change()
        else:
            super().mouseReleaseEvent(event)


class CheckableComboBox(QPushButton):
    """Button that opens a checkable drop-down menu for quick filters."""

    def __init__(self, placeholder, parent=None, on_change=None, single_selection=False):
        super().__init__(placeholder, parent)
        # QPushButton already supports an attached menu, which works well for
        # compact toolbar-style filter controls.
        self._menu = _MultiSelectMenu(self, single_selection=single_selection, on_change=on_change)
        self.setMenu(self._menu)

    def addCheckableItem(self, text, exclusive=False):
        # Each menu row is a QAction because Qt menus are action-based.
        action = QAction(text, self._menu)
        action.setCheckable(True)
        self._menu.addAction(action)
        if exclusive:
            self._menu._exclusive_action = action

    def addClearItem(self, text):
        # The clear action is checkable so it is handled by mouseReleaseEvent,
        # but clicking it simply clears the other items.
        action = QAction(text, self._menu)
        action.setCheckable(True)
        self._menu.addAction(action)
        self._menu._clear_action = action

    def checkedItems(self):
        # Return only the labels because the search builder only needs text.
        return [action.text() for action in self._menu.actions() if action.isChecked()]


# These globals store the current browser filter widgets so the search hook can
# read their state when Anki builds a browser search.
cbSuspended: QCheckBox = None
cbDue: CheckableComboBox = None
cbStudied: CheckableComboBox = None
cbNew: QCheckBox = None
cbFlag: CheckableComboBox = None
cbRecent: QCheckBox = None

def _quick_search_row(browser: Browser) -> QHBoxLayout:
    """Create the second browser toolbar row that holds Quick Search Browser controls."""

    row = QWidget(browser)
    # Do not let this row enforce a wide minimum size on the browser/editor
    # splitter. The individual widgets may still keep their natural width.
    row.setMinimumWidth(0)
    row.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    layout = QHBoxLayout(row)
    # Keep the row visually aligned with Anki's existing browser toolbar.
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    # Avoid letting the child widgets force this layout to a fixed size.
    layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
    layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    grid = browser.form.gridLayout
    # Add the filter row below Anki's built-in search row and span all columns
    # so it can use the available width while staying left aligned.
    grid.addWidget(row, 1, 0, 1, max(grid.columnCount(), 1))
    return layout

def _prepare_filter_widget(widget: QWidget):
    """Apply shared sizing rules to each Quick Search Browser control."""

    widget.setMinimumWidth(0)
    # Maximum width keeps each control compact; Fixed height matches toolbar
    # widgets and avoids vertical resize jitter.
    widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

def setup_quick_search_in_browser(browser: Browser):
    """Build the Quick Search Browser UI when an Anki browser window is shown."""

    global cbSuspended, cbDue, cbNew, cbFlag, cbRecent, cbStudied
    filter_layout = _quick_search_row(browser)

    # Hidden by default: suspended cards are excluded unless this is checked.
    cbSuspended = QCheckBox("Show Suspended", browser)
    cbSuspended.setChecked(False)
    _prepare_filter_widget(cbSuspended)
    filter_layout.addWidget(cbSuspended)
    cbSuspended.toggled.connect(partial(search, browser))

    # Adds Anki's is:new search term when checked.
    cbNew = QCheckBox("New", browser)
    cbNew.setChecked(False)
    _prepare_filter_widget(cbNew)
    filter_layout.addWidget(cbNew)
    cbNew.toggled.connect(partial(search, browser))

    # Adds a configurable "added:N" search term when checked.
    cbRecent = QCheckBox("Recent Added", browser)
    cbRecent.setChecked(False)
    _prepare_filter_widget(cbRecent)
    filter_layout.addWidget(cbRecent)
    cbRecent.toggled.connect(partial(search, browser))

    # Single-select due filter: Due in 1/3/7/14/30 days.
    cbDue = CheckableComboBox("Due", browser, on_change=partial(search, browser), single_selection=True)
    for i in [1, 3, 7, 14, 30]:
        cbDue.addCheckableItem(f"Due in {i} days")
    _prepare_filter_widget(cbDue)
    filter_layout.addWidget(cbDue)

    # Single-select studied filter: rated within 1/3/7/14/30 days.
    cbStudied = CheckableComboBox("Studied", browser, on_change=partial(search, browser), single_selection=True)
    for i in [1, 3, 7, 14, 30]:
        cbStudied.addCheckableItem(f"Studied in {i} days")
    _prepare_filter_widget(cbStudied)
    filter_layout.addWidget(cbStudied)

    # Multi-select flag filter. "Any flag" is exclusive because it conflicts
    # with picking specific flag numbers.
    cbFlag = CheckableComboBox("Flag", browser, on_change=partial(search, browser))
    cbFlag.addClearItem("(no filter)")
    cbFlag.addCheckableItem("Any flag", exclusive=True)
    for label in ["flag 1", "flag 2", "flag 3", "flag 4", "flag 5", "flag 6", "flag 7"]:
        cbFlag.addCheckableItem(label)
    _prepare_filter_widget(cbFlag)
    filter_layout.addWidget(cbFlag)
    filter_layout.addStretch(1)

def search(browser: Browser):
    # Ask Anki to re-run the browser search using the current search bar text.
    browser.onSearchActivated()

def setup_quick_search(context: SearchContext):
    """Modify Anki's browser search query according to selected filters."""

    global cbSuspended, cbDue, cbNew, cbFlag, cbRecent, cbStudied

    query = context.search.strip()

    # Do not modify direct note/card id lookups; wrapping those can interfere
    # with Anki's exact id searches.
    if "nid:" in query or "cid:" in query:
        return

    # By default, hide suspended cards. Checking "Show Suspended" disables this.
    if cbSuspended is not None and not cbSuspended.isChecked():
        query = f"({query}) -is:suspended"

    if cbDue is not None:
        checked = cbDue.checkedItems()
        if checked:
            # Convert "Due in 7 days" into prop:due=0 OR ... OR prop:due=7.
            due_days_str = checked[0].split(" ")[2]
            due_days = int(due_days_str)
            due_query = " OR ".join(f"prop:due={i}" for i in range(due_days + 1))
            query = f"({query}) ({due_query})"

    if cbStudied is not None:
        checked = cbStudied.checkedItems()
        if checked:
            # Convert "Studied in 7 days" into Anki's rated:7 search term.
            studied_days_str = checked[0].split(" ")[2]
            studied_days = int(studied_days_str)
            query = f"({query}) rated:{studied_days}"

    # Restrict to new cards when the New checkbox is selected.
    if cbNew is not None and cbNew.isChecked():
        query = f"({query}) is:new"

    if cbFlag is not None:
        checked = cbFlag.checkedItems()
        if "Any flag" in checked:
            # flag:0 means no flag, so -flag:0 means any non-zero flag.
            query = f"({query}) -flag:0"
        else:
            # Specific flags are OR'd together so selecting flag 1 and flag 2
            # shows cards matching either flag.
            flag_nums = [item.split(" ")[1] for item in checked if item.startswith("flag ")]
            if flag_nums:
                flag_query = " OR ".join(f"flag:{n}" for n in flag_nums)
                query = f"({query}) ({flag_query})"

    if cbRecent is not None and cbRecent.isChecked():
        # recent_added_days comes from the addon config. If it is missing, use
        # 10 days as the default recent-added window.
        config = mw.addonManager.getConfig(__name__)
        days = config.get("recent_added_days", 10) if config else 10
        query = f"({query}) added:{days}"

    # Give the final query back to Anki before it executes the browser search.
    context.search = query

# Register hooks:
# - browser_will_show adds the Quick Search Browser UI to each browser window.
# - browser_will_search updates the search query before Anki runs it.
gui_hooks.browser_will_show.append(setup_quick_search_in_browser)
gui_hooks.browser_will_search.append(setup_quick_search)
